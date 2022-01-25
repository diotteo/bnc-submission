FROM python:3.9.7

# Setting working directory. All the path will be relative to WORKDIR
WORKDIR /usr/src/app

# Copy files
COPY . .

# Installing dependencies
RUN pip install -r requirements.txt