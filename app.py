import os
import json
import requests
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

        # twilio has a 1600 character limit so checking values before creating request
        if len(recipe) > 1600 or len(ingredients) > 1600:
            messageSuccess = False

    # twilio 
        if messageSuccess:
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


@app.route('/searchRecipes', methods=['GET'])
def searchRecipes():

    if request.method == "GET":

        response = ''
        searchParams = request.args.get('query')
        requestParams = {
            'query':searchParams,
            'instructionsRequired': True,
            'apiKey':os.environ.get("SPOONACULAR_KEY"),
            'number':100
        }
        url = "https://api.spoonacular.com/recipes/search"

        try:
            r = requests.get(url, requestParams)
            response = jsonify(r.json())
        except Exception:
            response = jsonify('error')

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

@app.route('/getRecipeDetails/<int:recipeId>', methods=['GET'])
def getRecipeDetails(recipeId):

    if request.method == 'GET':

        response = ''
        requestParams = {
            'includeNutrition':False,
            'apiKey':os.environ.get("SPOONACULAR_KEY")
        }
        url = f"https://api.spoonacular.com/recipes/{recipeId}/information"

        try:
            r = requests.get(url, requestParams)
            response = jsonify(r.json())
        except Exception:
            response = jsonify('error')

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
        
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)