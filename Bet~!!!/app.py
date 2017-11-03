from flask import Flask, render_template, request, redirect, session
from passlib.hash import sha256_crypt
import mlab
from bson.objectid import ObjectId
from mongoengine import *


app = Flask(__name__)
app.config["SECRET_KEY"] = "piudfpasudfpa7wr09 21y"

mlab.connect()

class Account(Document):
    username = StringField()
    name = StringField()
    image = FileField()
    password = StringField()
    email = EmailField()
    phone = FloatField()
    #friend system
    friendlist = ListField()
    friend_request_sent = ListField()
    friend_accept_pending = ListField()
    #
    #bet system
    active_bet = ListField()
    win_bet = ListField()
    lost_bet = ListField()







@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        form = request.form
        username = form['username']
        password = sha256_crypt.encrypt(form['password'])
        name = form['name']
        image = form['image']
        email = form['email']
        phone = form['phone']
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            account = None
        if account is None:
            account = Account(name=name,password=password,username=username,email=email,phone=phone)
            account.save()
            return redirect('/login')
        else:
            message = "Tên đăng nhập đã tồn tại, vui lòng chọn tên khác"
            return render_template('message.html', message = message)



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
                session["username"] = account.username
                url = "/profile/" + account.username
                return redirect(url)
            else:
                message = "Sai mật khẩu"
                return render_template('message.html', message = message)




@app.route('/profile/<username_url>', methods=['GET','POST'])
def profile(username_url):
    username = session['username']
    username_url = username_url
    account = Account.objects.get(username = username)
    account_other = Account.objects.get(username = username_url)
    return render_template('profile.html', account = account, account_other = account_other, username = username, username_url = username_url)







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






@app.route('/edit.profile/<username_url>', methods=['GET','POST'])
def edit_profile(username_url):
    account = Account.objects.get(username = username_url)
    if request.method == "GET":
        return render_template('edit_profile.html', account = account)
    elif request.method == "POST":
        form = request.form
        name = form['name']
        image = form['image']
        email = form['email']
        phone = form['phone']
        account.update(name = name, image = image, email = email, phone = phone)
        url = '/profile/' + username_url
        return redirect(url)




@app.route('/friend.request/<method>/<username_url>', methods=['GET','POST'])
def friend_request_method(method, username_url):
    username = session['username']
    account = Account.objects.get(username = username)
    account_other = Account.objects.get(username = username_url)
    url = '/profile/' + username_url
    if method == "delete.friend":
        account.update(pull__friendlist=account_other.username)
        account_other.update(pull__friendlist=account.username)
    elif method == "cancel":
        account.update(pull__friend_request_sent = account_other.username)
        account_other.update(pull__friend_accept_pending = account.username)
    elif method == "accept":
        account.update(add_to_set__friendlist = account_other.username)
        account_other.update(add_to_set__friendlist = account.username)
    elif method == "send.request":
        account.update(add_to_set__friend_request_sent = account_other.username)
        account_other.update(add_to_set__friend_accept_pending = account.username)
    return redirect(url)





    # friendlist = ListField()
    # friend_request_sent = ListField()
    # friend_accept_pending = ListField()













@app.route('/logout', methods = ['GET'])
def logout():
    del session['username']
    return redirect('/login')

if __name__ == '__main__':
  app.run(debug=True)
