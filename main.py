from flask import Flask, request
from flask_cors import CORS
import requests
import json
import os

# only  for development
# import configparser
#
# config = configparser.ConfigParser()
# config.read("config.ini")

app = Flask(__name__)
# CORS config for development
# CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# CORS config for production
CORS(app, resources={r"/*": {"origins": os.environ.get('APP_URL')}})

def air_get(full_name, email, message):
    try:
        body = {"records": [{"fields": {"Full Name": full_name, "Email": email,
                                        "Message": message}}]}
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Bearer {os.environ.get('API_KEY')}"}
        response = requests.post(os.environ.get('API_ENDPOINT'),
                                 headers=headers, data=json.dumps(body))
        response.raise_for_status()

    except requests.exceptions.ConnectionError as con_error:
        return json.dumps(con_error)
    except requests.HTTPError as h_error:
        return json.dumps(h_error)
    else:
        return response.json()

@app.route("/", methods=['POST'])
def post_inquiry():
    inquiry_data = request.json
    full_name = inquiry_data['name']
    email = inquiry_data['email']
    message = inquiry_data['message']
    answer = air_get(full_name, email, message)
    return answer

if __name__ == '__main__':
    app.run(debug=True)
