from flask import Flask, render_template,request
import mlab
from mongoengine import *

app = Flask(__name__)

mlab.connect()

class Account(Document):
    name=StringField()
    image=FileField()
    username=StringField()
    password=StringField()
    email=EmailField()
    phone=FloatField()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=="GET":
        return render_template('signup.html')
    elif request.method=="POST":
        form=request.form
        name=form['name']
        password=form['password']
        username=form['username']
        image=form['image']
        email=form['email']
        phone=form['phone']
        account=Account(name=name,password=password,username=username,email=email,phone=phone)
        account.save()
        return "Done!"

if __name__ == '__main__':
  app.run(debug=True)
