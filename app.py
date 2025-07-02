from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import webbrowser
import threading

app = Flask(__name__)
model = load_model('rice_model.h5')

# Rice class labels
class_names = ['Basmati', 'Jasmine', 'Arborio', 'Ipsala', 'Karacadag']

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    filename = None

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']
        if file.filename == '':
            return 'No selected file'

        if file:
            filename = file.filename
            filepath = os.path.join('static', filename)
            file.save(filepath)

            # Load and preprocess image
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Predict
            preds = model.predict(img_array)
            predicted_class = class_names[np.argmax(preds)]

            prediction = predicted_class

    return render_template('index.html', prediction=prediction, filename=filename)


def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")

if __name__ == '__main__':
    threading.Timer(1.25, open_browser).start()
    app.run(debug=True)
