from flask import Flask, request, jsonify
from api.dataset import create_dataset

app = Flask(__name__)

@app.route('/')
def index(): 
    return "ML Image Transformation App", 200

@app.route('/dataset', methods=["POST"])
def create_new_dataset(): 
    
    response = {}

    dataset_name = request.get_json()['name']

    if dataset_name is None: 
        response["error"] = "Please provide a dataset name"
        return jsonify(response), 400

    try:
        dataset_id = create_dataset(dataset_name)
        response["name"] = dataset_name
        response["dataset_id"] = dataset_id
        return jsonify(response), 200
    except: 
        response["error"] = "Unable to create new dataset"
        return jsonify(response), 500

