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

        messageSuccess = True
        destination = request.form['number']
        recipe = request.form['recipe']
        ingredients = request.form['ingredients']

    # twilio 
    # twilio has a 1600 character limit so splitting into two messages
        try:
            ingredientsMessage = client.messages.create(
                body=f"Ingredients: {ingredients}",
                from_=origin_number,
                to=f"+1{destination}"
                )
            recipeMessage = client.messages.create(
                body=f"Directions: {recipe}",
                from_=origin_number,
                to=f"+1{destination}"    
            )
        except Exception:
            messageSuccess = False 

        response = jsonify(messageSuccess)
        # CORS
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
    return 'hello world'


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)