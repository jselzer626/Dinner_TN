import os
import json
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['DEBUG'] = True
load_dotenv()

api_key = os.environ.get("api_key")

@app.route('/')
def home():
    
    