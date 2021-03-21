# Rocket League Stats Producer

## Purpose

A web-scale stats producer deployed on AWS Lambda which analyzes Rocket League replays for stats and outputs them in a file format usable by the MNRL Stats Platform.

## Getting Started

### Install Stuff

Make sure you have some version of python installed

Install [node](https://nodejs.org/en/download/)

Install [yarn](https://classic.yarnpkg.com/en/docs/install/#mac-stable)

Install serverless with `npm i -g serverless`

Create virtual environment in this directory
`virtualenv venv --python=python3.7.6`

Activate it
`source venv/bin/activate`

### Deploy

Deploy with serverless

`sls deploy`

## Notes:

Save requirements (this spec's everything, you only need the top-level packages as pip will auto-install the rest)
`pip freeze > requirements.txt`

Install whatever is in requirements.txt
`pip install -r requirements.txt`