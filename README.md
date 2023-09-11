# AIOT Chat

The python chat bot application setup on top of OpenAI's LLM to interact with IoT sensors/devices within their room through Text.
The system also stores the chat history between users and chat bot to the ElasticSearch DB.

## Setup

1. Install docker
2. Clone this git repo.
```
git clone https://github.com/jpjayprasad-dev/aiotchat/ .
```

## Build Image
```
docker build -t aiotchat:latest .
```

## Application Specs

1. The following environment variables determines the running configuration of the app
```
PORTAL_HOST = AIOT portal host:port
ES_HOST = ElasticSearch DB host:port
```
2. Copy your Open AI key to the file ./open_ai_key.txt

## Run Service
```
docker run --rm -d -p 7860:7860 -e PORTAL_HOST=<aiot_portal_host:port> -e ES_HOST=<elastic_search_host:port> -v ./open_ai_key.txt:/open_ai_key.txt --name aiot-chat aiotchat:latest

```

## Examples [Screenshots]
Run the chatbot app
<img width="1003" alt="image" src="https://github.com/jpjayprasad-dev/aiotchat/assets/73153441/9e4e2d32-7cee-45c4-b569-1b2fd943cd73">


Access the chatbot through browser at http://<host_ip>:7860/
<img width="1378" alt="image" src="https://github.com/jpjayprasad-dev/aiotchat/assets/73153441/009d0523-341d-478c-9b6e-fcc905d77099">





