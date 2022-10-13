from flask import Flask, render_template
import os

app = Flask(__name__)
PHOTOFOLDER = os.path.join('static','photos')
app.config['UPLOAD_FOLDER'] = PHOTOFOLDER

@app.route('/')
def image_maker():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'output.png')
    return render_template("index.html", user_image = full_filename)



        
