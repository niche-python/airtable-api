from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
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

def create_response(data, status, message, code):
    response = {
        "status":status,
        "data": data if data is not None else {},
        "message": message if message is not None else "Operation successful"
    }
    return make_response(jsonify(response), code)

def send_message(full_name, email, message):
    if(full_name == "" or email == "" or message == ""):
        return create_response(None, 'error', 'All fields are required', 400)

    account_sid = os.environ.get('TWILIO_SID')
    auth_token  = os.environ.get('TWILIO_TOKEN')
    number_to = os.environ.get('TWILIO_MY_NUMBER')
    number_from = os.environ.get('TWILIO_SEND')

    client = Client(account_sid, auth_token)

    try:
        message =client.messages.create(
            to=number_to,
            from_=number_from,
            body=f"""Full Name: {full_name}
            Email: {email}
            Message: {message}""")

        return create_response(message.body, 'success', 'Message sent successfully', 200)

    except TwilioRestException as e:
        return create_response(None, 'error', str(e), 501)


        

@app.route("/", methods=['POST'])
def post_inquiry():
    inquiry_data = request.json
    full_name = inquiry_data['name']
    email = inquiry_data['email']
    message = inquiry_data['message']
    answer = send_message(full_name, email, message)
    return answer

if __name__ == '__main__':
    app.run(debug=True)
