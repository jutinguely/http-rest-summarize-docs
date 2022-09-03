# Large texts summarization Rest API

The goal of the project is to implement a simple Rest API to publish text document and summarize them using NLP transfered models.
The following endpoints: `HTTP/POST store`, `HTTP/GET get_document`, `HTTP/GET get_summary`, `HTTP/GET get_documentIds` are exposed in the postman.json collection.

## Architecture

*app.py* implements a flask api defining the four routes from above and instansiates a class called *DocumentManager* which takes care of storing and processing the documents.

Each document is mapped to an hashed key to faciliate its storage in a key-value storage solution. Here we use python dictionary locally and redis for production.

Besides the standard storing funcitonalities, the *DocumentManager* spawns four processes that are responsible to pull *SummarizationTask* from a queue and summarize the texts using transformers pulled from hugging. When a process is done summarizing it publish the summary into a result queue which is then stored in the database.  

## Installation

### Without data persistence (default)

The solution uses python dictionaries.

### With data persistence

on MacOS:
- install Redis: `brew install redis`
- start redis: `redis-server`
- set `persist: True` in config.yml

## Commands

#### Shell 1: start the Rest API
```pyt
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py 
```

#### Shell 2: test the Rest API
```pyt
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python -m tests.endpoints 
```

or with curl

`curl -v -H "Content-Type: application/json" -X POST -d "@payload.json" http://0.0.0.0:5001/store -k`

and 

`curl -v -H "Content-Type: application/json -X GET http://http://0.0.0.0:5001/get_document?id=<returned_id>`

## Further Work
- secure the API with OAuth2 access token and use https or mTLS
- test heavy workloads and consider using Pools for better performance
- implement a global logging solution
- define rules, is the user allowed to enter a book?
- deploy solution on cloud with automatic helm deployment