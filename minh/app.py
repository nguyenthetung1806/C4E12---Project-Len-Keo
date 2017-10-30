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

<<<<<<< HEAD
=======
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="GET":
        return render_template('login.html')
    elif request.method=="POST":
        form=request.form
        username=form['username']
        password=form['password']
        try:
            account=Account.objects.get(username=username)
        except Account.DoesNotExist:
            account=None
        if account is None:
            return "Sai tài khoản"
        else:
            if password==account.password:
                return "Đăng nhập thành công!"
            else:
                return "Sai mật khẩu"

>>>>>>> 81ed240fec783af41c37285637bb9fdb63d654c2
if __name__ == '__main__':
  app.run(debug=True)
