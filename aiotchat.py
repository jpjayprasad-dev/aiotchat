import gradio as gr
import openai
import json
import requests
import os

from controllers import sensor_controller, device_controller, general_logger


sc = sensor_controller.SensorController(os.getenv('PORTAL_HOST'))
dc = device_controller.DeviceController(os.getenv('PORTAL_HOST'))
gl = general_logger.GeneralLogger(os.getenv('ES_HOST'))
openai.api_key = os.getenv('OPENAI_KEY') if os.getenv('OPENAI_KEY') else open("open_ai_key.txt", "r").read().strip("\n")

message_history = [{"role": "user", "content": f"You are a room assistant. I will specify the hotel name, room number, name of the room sensor which i want to read data, name of the device which i want to send controls in my messages and you will reply with a function call. If i specify timespan in days then convert it to hours. If you understand, say OK."},
                   {"role": "assistant", "content": f"OK"}
                  ]

def predict(input):
    # tokenize the new input sentence
    message_history.append({"role": "user", "content": f"{input}"})

    # log user response to generall logger 
    gl.log('user', input)

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=message_history,
      functions=[
        {
            "name": "get_room_sensor_data",
            "description": "Get the room data from sensors",
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_name": {
                        "type": "string",
                        "description": "The name of the hotel, e.g. ibis, novotel",
                    },
                    "room_number": {
                        "type": "string",
                        "description": "The number of the room, e.g. 101A, 202",
                    },
                    "room_sensor": {
                        "type": "string",
                        "description": "The name of the sensor in which the data to be read, e.g. life_being, iaq"
                    },
                    "timespan": {
                        "type": "number",
                        "description": "The time span of the data to be retrieved in hours, e.g. 20 hours, 1 day, 5 days"
                    },
                },
                "required": ["hotel_name", "room_number", "room_sensor"],
            },
        },
        {
            "name": "send_room_device_control",
            "description": "Send the control to the room devices",
            "parameters": {
                "type": "object",
                "properties": {
                    "hotel_name": {
                        "type": "string",
                        "description": "The name of the hotel, e.g. ibis, novotel",
                    },
                    "room_number": {
                        "type": "string",
                        "description": "The number of the room, e.g. 101A, 202",
                    },
                    "room_device": {
                        "type": "string",
                        "description": "The name of the device in which the control to be send, e.g. aircon, tv"
                    },
                    "room_device_param": {
                        "type": "string",
                        "description": "The name of the control parameter belong to the device, e.g. temperature, fan_speed, power"
                    },
                    "room_device_value": {
                        "type": "string",
                        "description": "The value against the control parameter belong to the device, e.g. 23, low, on/off"
                    },

                },
                "required": ["hotel_name", "room_number", "room_device", "room_device_param", "room_device_value"],
            },
        }
        ],
        function_call="auto",
    )

    message_response = completion.choices[0].message
    print(completion)

    function_call_response = ""

    if 'function_call' in message_response.to_dict():
        function_name = message_response.to_dict()['function_call']['name']
        function_args = json.loads(message_response.to_dict()['function_call']['arguments'])
        print(function_name)
        print(function_args)
        print(message_response.to_dict())
        if function_name == "get_room_sensor_data":
            function_call_response = sc.get_room_sensor_data(function_args)
        if function_name == "send_room_device_control":
            function_call_response = dc.send_room_device_control(function_args)

    if function_call_response:
        reply_content = function_call_response.replace("\n", "</br>")
    else:
        reply_content = message_response.content#.replace('```python', '<pre>').replace('```', '</pre>')

    print(reply_content)
    message_history.append({"role": "assistant", "content": f"{reply_content}"})

    # log assistant response to generall logger 
    gl.log('assistant', reply_content)
    
    # get pairs of msg["content"] from message history, skipping the pre-prompt:              here.
    response = [(message_history[i]["content"], message_history[i+1]["content"]) for i in range(2, len(message_history)-1, 2)]  # convert to tuples of list
    return response

# creates a new Blocks app and assigns it to the variable demo.
with gr.Blocks() as demo: 

    # creates a new Chatbot instance and assigns it to the variable chatbot.
    chatbot = gr.Chatbot() 

    # creates a new Row component, which is a container for other components.
    with gr.Row(): 
        '''creates a new Textbox component, which is used to collect user input. 
        The show_label parameter is set to False to hide the label, 
        and the placeholder parameter is set'''
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter").style(container=False)
    '''
    sets the submit action of the Textbox to the predict function, 
    which takes the input from the Textbox, the chatbot instance, 
    and the state instance as arguments. 
    This function processes the input and generates a response from the chatbot, 
    which is displayed in the output area.'''
    txt.submit(predict, txt, chatbot) # submit(function, input, output)
    #txt.submit(lambda :"", None, txt)  #Sets submit action to lambda function that returns empty string 

    '''
    sets the submit action of the Textbox to a JavaScript function that returns an empty string. 
    This line is equivalent to the commented out line above, but uses a different implementation. 
    The _js parameter is used to pass a JavaScript function to the submit method.'''
    txt.submit(None, None, txt, _js="() => {''}") # No function, no input to that function, submit action to textbox is a js function that returns empty string, so it clears immediately.
         
demo.launch(server_name="0.0.0.0")

