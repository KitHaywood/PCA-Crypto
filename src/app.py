from flask import Flask, render_template, request
import os,sys
import io
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
sys.path.insert(0,os.getcwd())
from main import *

matplotlib.pyplot.switch_backend('Agg') 
app = Flask(__name__)
PHOTOFOLDER = os.path.join('static','photos')
app.config['UPLOAD_FOLDER'] = PHOTOFOLDER

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/image',methods=["POST","GET"])
def make_image():
    if request.method == "POST":
        cryptos = request.form.getlist('cryptos')
        numpca = request.form['pcas']
        params = load_model_params('model.yaml')
        params['instruments'] = cryptos
        params['numPC'] = int(numpca)
        fig = make_pca_analysis(**params)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
        return Response(output.getvalue(), mimetype='image/png')
    else:
        return render_template('index.html')





        
