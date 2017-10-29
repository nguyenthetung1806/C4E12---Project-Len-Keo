import mlab
from flask import Flask, render_template, request, redirect
from mongoengine import *
from faker import Faker

app = Flask(__name__)

#connect to mlab file
mlab.connect()


class Profile(Document):
    name = StringField()
    image = StringField()
    description = StringField()
    active-bet = ListField
    completed-bet = ListField

class Contract(Document):
    contract-term = StringField;
    contract-party-left = ListField;
    contract-party-right = ListField;









@app.route('/')
def index():
    return render_template('homepage.html')


if __name__ == '__main__':
  app.run(debug=True)
