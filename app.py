from flask import Flask, render_template, request, redirect, send_file
from lsb import hide_message, extract_message
from helper import generate_time_based_name
from werkzeug.utils import secure_filename
import io
from os import path

app = Flask(__name__)
app.config['O_IMAGE_DIR'] = 'static/o_images'
app.config['e_IMAGE_DIR'] = 'static/encoded_images'

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/decode-view')
def decode_vew():
    return render_template('decode.html')

@app.route('/encode-msg', methods=['POST'])
def encode_message():
    global BASE_DIR
    if request.method == 'POST':
        image = request.files['o-image']
        message = request.form['message']
        filename = generate_time_based_name('original') + secure_filename(image.filename)
        if(image and message):
            image.save(path.join(app.config['O_IMAGE_DIR'], filename))
            encoded_image = path.join(app.config['e_IMAGE_DIR'],generate_time_based_name("encoded_") + '.png')
            hide_message(
                path.join(app.config['O_IMAGE_DIR'], filename),
                message,
                encoded_image)
        return send_file(
        encoded_image,
        as_attachment=True,
        download_name=generate_time_based_name('encoded_') + '.png',
        mimetype='image/png'
    )

@app.route('/decode-msg', methods=['POST'])
def decode_message():
    global BASE_DIR
    if request.method == 'POST':
        image = request.files['encoded-image']
        if image.filename:
            return render_template('index.html', decoded_message = extract_message(image))
        return render_template('index.html', err = 'Please select an image first.')