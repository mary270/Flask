
import traceback
from flask import Flask
from flask import request

class ML:
    def __init__(self):
        self.avaliable_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection"
           
        }
        self.loaded_models = {}
        self.model_request_count = {model: 0 for model in self.avaliable_models}

    def load_model(self, model):
        print(f"Loading model: {model}")
        # Replace the model that has been requested the least
        least_requested_model = min(self.model_request_count, key=self.model_request_count.get)
        if least_requested_model in self.loaded_models:
            del self.loaded_models[least_requested_model]
        self.loaded_models[model] = self.avaliable_models[model]
        print(f"Loaded model: {model}")

    def process_request(self, model, data):
        try:
            if model not in self.avaliable_models:
                return {"error": "Model not found."}, 400

            if model not in self.loaded_models:
                self.load_model(model)

            self.model_request_count[model] += 1

            # Dummy processing for demonstration purposes
            result = f"Processed request using {model}. Data: {data}"

            return {"result": result}, 200

        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500

app = Flask(__name__)
ml = ML()

@app.route('/get_loaded_models')
def get_loaded_models():
    return {"loaded_models": list(ml.loaded_models.keys())}

@app.route('/process_request')
def process_request():
    try:
        model = request.args.get("model")
        data = request.args.get("data")

        return ml.process_request(model, data)

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}, 500

