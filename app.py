from flask import Flask


app = Flask(__name__)

@app.get("/hello")
def index():
    return {"message": "Hello World"}