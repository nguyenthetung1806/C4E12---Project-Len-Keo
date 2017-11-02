from flask import *
from base64 import b64encode
app = Flask(__name__)


@app.route('/signup', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('signup.html')
    elif request.method == "POST":
        form = request.form
        name = form['name']
        image = request.files['image']

        b64_image = b64encode(image.read())

        return b64_image

if __name__ == '__main__':
  app.run(debug=True)
