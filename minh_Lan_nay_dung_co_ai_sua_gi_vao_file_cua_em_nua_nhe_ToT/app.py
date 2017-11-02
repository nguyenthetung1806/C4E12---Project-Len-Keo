from flask import Flask, render_template,request
import mlab
from base64 import b64encode
from mongoengine import *

app = Flask(__name__)

mlab.connect()

class Account(Document):
    name=StringField()
    image=StringField()
    username=StringField()
    password=StringField()
    email=EmailField()
    phone=FloatField()

class Keo(Document):
    license=StringField()
    hour1=FloatField()
    minute1=FloatField()
    day1=FloatField()
    month1=FloatField()
    year1=FloatField()
    hour2=FloatField()
    minute2=FloatField()
    day2=FloatField()
    month2=FloatField()
    year2=FloatField()
    join=FloatField()
    up=StringField()
    down=StringField()
    guest=StringField()
    id1=StringField()

class Keo2(Document):
    license=StringField()
    hour1=FloatField()
    minute1=FloatField()
    day1=FloatField()
    month1=FloatField()
    year1=FloatField()
    hour2=FloatField()
    minute2=FloatField()
    day2=FloatField()
    month2=FloatField()
    year2=FloatField()
    join=FloatField()
    joinlist=StringField()
    guest=StringField()
    id1=StringField()

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
        email=form['email']
        phone=form['phone']
        image = request.files['image']
        image = b64encode(image.read())
        try:
            account=Account.objects.get(username=username)
        except Account.DoesNotExist:
            account=None
        if account is None:
            account=Account(name=name,password=password,image=image,username=username,email=email,phone=phone)
            account.save()
            return "Done!"
        else:
            return "Tên đăng nhập đã tồn tại"


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

@app.route('/lenkeo', methods=['GET','POST'])
def lenkeo():
    if request.method=="GET":
        return render_template('lenkeo.html')
    elif request.method=="POST":
        form=request.form
        license=form['license']
        hour1=form['hour1']
        minute1=form['minute1']
        day1=form['day1']
        month1=form['month1']
        year1=form['year1']
        hour2=form['hour2']
        minute2=form['minute2']
        day2=form['day2']
        month2=form['month2']
        year2=form['year2']
        join=form['join']
        up=form['up']
        down=form['dowm']
        guest=form['guest']
        id1=form['id1']
        keo=Keo(license=license,hour1=hour1,minute1=minute1,day1=day1,month1=month1,year1=year1,hour2=hour2,minute2=minute2,day2=day2,month2=month2,year2=year2,join=join,up=up,down=down,guest=guest,id1=id1)
        keo.save()
        return "Done!!!"

@app.route('/lenkeo2', methods=['GET','POST'])
def lenkeo2():
    if request.method=="GET":
        return render_template('lenkeo2.html')
    elif request.method=="POST":
        form=request.form
        license=form['license']
        hour1=form['hour1']
        minute1=form['minute1']
        day1=form['day1']
        month1=form['month1']
        year1=form['year1']
        hour2=form['hour2']
        minute2=form['minute2']
        day2=form['day2']
        month2=form['month2']
        year2=form['year2']
        join=form['join']
        joinlist=form['joinlist']
        guest=form['guest']
        id1=form['id1']
        keo2=Keo2(license=license,hour1=hour1,minute1=minute1,day1=day1,month1=month1,year1=year1,hour2=hour2,minute2=minute2,day2=day2,month2=month2,year2=year2,join=join,joinlist=joinlist,guest=guest,id1=id1)
        keo2.save()
        return "Done!!!"

if __name__ == '__main__':
  app.run(debug=True)
