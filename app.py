from flask import Flask, request, jsonify
from helpers.document import DocumentManager
import yaml

app = Flask(__name__)
config = yaml.load(open("config.yml"), Loader=yaml.FullLoader)
DB = None

@app.post("/store")
def store_document() -> int:
    if "text" in set(request.json.keys()): 
        return jsonify(DB.write_document(request.json["text"])), 200
    else:
        return jsonify({"message": "bad request"}), 400

@app.get("/get_document")
def get_document() -> dict:
    if "id" in set(request.args.keys()): 
        return jsonify(DB.load_document(request.args["id"])), 200
    else:
        return jsonify({"message": "bad request"}), 400                      

@app.get("/get_summary")
def get_summary() -> dict:
    if "id" in set(request.args.keys()): 
        return jsonify(DB.load_document_summary(request.args["id"])), 200
    else:
        return jsonify({"message": "bad request"}), 400

@app.get("/get_documentIds")
def get_documentIds() -> dict:
    return jsonify(DB.load_documentIds()), 200
 
if __name__ == '__main__':
    DB = DocumentManager(host=config["host"], port=6379, config=config)
    # for secure communication enable https -> ssl_context, generate crt/pub keys
    app.run(host=config["host"], port=config["port_api"], debug=True)