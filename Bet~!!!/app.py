from flask import Flask, render_template, request, redirect
from passlib.hash import sha256_crypt
import mlab
from bson.objectid import ObjectId
from mongoengine import *

app = Flask(__name__)

mlab.connect()

class Account(Document):
    name = StringField()
    image = FileField()
    username = StringField()
    password = StringField()
    email = EmailField()
    phone = FloatField()


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        form = request.form
        name = form['name']
        password = sha256_crypt.encrypt(form['password'])

        username = form['username']
        image = form['image']
        email = form['email']
        phone = form['phone']
        account=Account(name=name,password=password,username=username,email=email,phone=phone)
        account.save()
        return redirect('/login')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = form['password']
        
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            account = None
        if account is None:
            message = "Tài khoản không tồn tại"
            return render_template('message.html', message = message)
        else:
            if sha256_crypt.verify(password, account.password) == True:
                return render_template('profile.html', account = account)
            else:
                message = "Sai mật khẩu"
                return render_template('message.html', message = message)



@app.route('/lenkeo', methods=['GET','POST'])
def lenkeo():
    if request.method=="GET":
        return render_template('lenkeo.html')
    # elif request.method=="POST":
    #     form=request.form

@app.route('/lenkeo2', methods=['GET','POST'])
def lenkeo2():
    if request.method=="GET":
        return render_template('lenkeo2.html')
    # elif request.method=="POST":
    #     form=request.form



if __name__ == '__main__':
  app.run(debug=True)
