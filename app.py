from flask import Flask, request, jsonify, make_response
from flask_restplus import Api, Resource, fields
from sklearn.externals import joblib
import numpy as np

flask_app = Flask(__name__)
app = Api(app=flask_app,
          version="1.0",
          title="ML React App",
          description="Predict results using a trained model")

# @app.route("/")
# def hello():
#     return "Hello World!"


@name_space.route("/")
class MainClass(Resource):

    def options(self):
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response

    # @app.expect(model)
    # def post(self):
    #     try:
    #         formData = request.json
    #         data = [val for val in formData.values()]
    #         prediction = classifier.predict(np.array(data).reshape(1, -1))
    #         types = {0: "Iris Setosa",
    #                  1: "Iris Versicolour ", 2: "Iris Virginica"}
    #         response = jsonify({
    #             "statusCode": 200,
    #             "status": "Prediction made",
    #             "result": "The type of iris plant is: " + types[prediction[0]]
    #         })
    #         response.headers.add('Access-Control-Allow-Origin', '*')
    #         return response
    #     except Exception as error:
    #         return jsonify({
    #             "statusCode": 500,
    #             "status": "Could not make prediction",
    #             "error": str(error)
    #         })


# if __name__ == "__main__":
#     app.run(host='0.0.0.0')
