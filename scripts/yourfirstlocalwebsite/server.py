from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

# Allow all origins by default 
# ### IN PRODUCTION NEEDS TO BE CHANGED TO OWN DOMAIN CORS(app, origins=['https://yourdomain.com', 'https://anotherdomain.com']) 
## Can also restrict: , methods=['GET', 'POST', 'PUT'])

## Or even more specific CORS(app, 
     #origins=['https://yourdomain.com'],
     #methods=['GET', 'POST'],
     #allow_headers=['Content-Type'],
     #max_age=3600,
     #supports_credentials=True):

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"message": "Hello from Python!"})

if __name__ == '__main__':
    app.run(debug=True, thread=True)
