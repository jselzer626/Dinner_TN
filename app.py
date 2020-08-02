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
    try:
    if request.method == "POST":

        destination = request.form['number']
        recipe = request.form['recipe']
        ingredients = request.form['ingredients']

        print(destination, recipe, ingredients)

        message = client.messages.create(
            body=recipe,
            from_=origin_number,
            to=f"+1{destination}"
        )

        return jsonify(message.status)

    except HTTPError:
        return "error"


    
    return 'hello world'