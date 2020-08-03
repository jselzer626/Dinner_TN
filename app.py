import os
import json
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from twilio.rest import Client

app = Flask(__name__)
app.config['DEBUG'] = True
load_dotenv()

client = Client(os.environ.get("ACCOUNT_SID"), os.environ.get("AUTH_TOKEN"))
origin_number = '+12057829884'

@app.route('/', methods=['GET', 'POST'])
def sendSMS():
    if request.method == "POST":

        destination = request.form['number']
        recipe = request.form['recipe']
        ingredients = request.form['ingredients']

    # twilio 
        try:
            message = client.messages.create(
                body=recipe,
                from_=origin_number,
                to=f"+1{destination}"
            )
        except Exception: 
            return jsonify("Invalid number")

        return jsonify(message.status)

    return 'hello world'

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)