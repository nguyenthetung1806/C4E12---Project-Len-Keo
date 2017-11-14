from flask import Flask, render_template, request, redirect
import mlab
from mongoengine import * #Document,StringField,FloatField

app = Flask(__name__)
mlab.connect()


class Datetime(Document):
    dates = StringField()
    times = StringField()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/timer')
def timer():
    date_time = Datetime.objects()
    return render_template('timer.html')

@app.route('/input_time', methods = ['GET','POST'])
def input_time():
    if request.method =="GET" :
        return render_template('input_time.html')
    elif request.method  == "POST" :
        form = request.form
        dates = form['dates']
        times = form['times']
        datetime = Datetime(dates = dates, times = times)
        datetime.save()
        return "Da cap nhat"

if __name__ == '__main__':
  app.run( debug=True)
