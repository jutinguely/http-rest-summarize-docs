from multiprocessing.dummy import freeze_support
from flask import Flask, request
from helpers.database import Database 
import yaml

app = Flask(__name__)
config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
DB = None

@app.post("/store")
def store_document() -> int:
    if "text" in set(request.json.keys()): # -d {text: values}
        return DB.write_document(request.json["text"])
    else:
        return {"message": "bad request"}

@app.get("/get_document")
def get_document() -> dict:
    if "id" in set(request.args.keys()): # {id: value}
        return DB.load_document(request.args["id"])
    else:
        return {"message": "bad request"}

@app.get("/get_summary")
def get_summary() -> dict:
    if "id" in set(request.args.keys()): # {id: value}
        return DB.load_document_summary(request.args["id"])
    else:
        return {"message": "bad request"}

@app.get("/get_documentIds")
def get_documentIds() -> dict:
    return DB.load_documentIds()
 
if __name__ == '__main__':
    DB = Database(host=config["host"], port=6379, db=0, persist=config["persist_data"])
    app.run(host=config["host"], port=config["port_api"], debug=True)