# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /producer

# copy the dependencies file to the working directory
COPY requirements.txt handler.py example.replay ./
COPY src ./src

# install dependencies
RUN pip install -r requirements.txt

# # command to run on container start
# CMD [ "python", "./handler.py" ]