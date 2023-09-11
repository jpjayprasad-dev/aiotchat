# use python version 3 docker image as base image
FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1

# copy the requirements.txt file in to the pwd of docker image.
COPY requirements.txt ./requirements.txt

# now run the command to install dependencies from requirements file
RUN pip install -r requirements.txt

# copy the contents of controllers in to the pwd of docker image.
COPY controllers/ controllers/

# copy the aiotchat.py file in to the pwd of docker image.
COPY aiotchat.py aiotchat.py

# expose the port 7860
EXPOSE 7860

# everytime container is started, run this command
ENTRYPOINT ["python", "aiotchat.py"]