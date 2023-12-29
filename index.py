from __future__ import print_function, unicode_literals, absolute_import, division
from flask import Flask, Response, request, jsonify
from io import BytesIO
from flask_cors import CORS
import numpy as np
import matplotlib.pyplot as plt
import json
import cv2
from PIL import Image
from csbdeep.utils import normalize
from stardist import random_label_cmap
from stardist.models import StarDist2D
from stardist import _draw_polygons
import base64

app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])

@app.route('/segmentation', methods=['POST'])
def get_image():
    # Open image from request:
    imageUpload = request.files['image']
    modelType = request.form['type']
    modelColorMap = request.form['colorMap']

    # Open image by pilow and normalize image 
    axis_norm = (0,1)
    image = Image.open(imageUpload)
    image = image.convert('L')
    image = np.array(image)
    image = normalize(image,1,99.8,axis=axis_norm)

    # Open trained model
    modelName = 'stardist'
    if modelType == "bubble":
        modelName = "bubble2"
    if modelType == '2D_versatile_fluo':
        model = StarDist2D.from_pretrained('2D_versatile_fluo')
    else:
        model = StarDist2D(None, name = modelName, basedir = 'models')

    # Predict the image
    y_test = model.predict_instances(image, n_tiles=model._guess_n_tiles(image), show_tile_progress=False)

    # Define a colormap
    cmap = random_label_cmap()
    if modelColorMap != "random_label_cmap":
        cmap = plt.get_cmap(modelColorMap)

    # Normalize the grayscale image values to the range [0, 1]
    normalized_image = (y_test[0] - y_test[0].min()) / (y_test[0].max() - y_test[0].min())

    # Apply the colormap to the normalized image
    image = (cmap(normalized_image) * 255).astype(np.uint8)
    image = Image.fromarray(image)
    # image.save('output.png')

    # Save the image to a BytesIO object
    image_bytes = BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    # Return the image as a response with the appropriate content type
    # return Response(image_bytes, content_type='image/png')
    image_base64 = base64.b64encode(image_bytes.getvalue()).decode('utf-8')

    # Create a dictionary to hold the image and text data
    response_data = {
        'imageBytes': image_base64,
        'objectsCount': len(y_test[1]['points']),
        'points': y_test[1]['points'].tolist(),
        'coord': y_test[1]['coord'].tolist(),
    }

    # Return the response as JSON with image and text data
    return jsonify(response_data)

@app.route('/convert', methods=['POST'])
def convert_tiff_to_png():
    tiff_file = request.files['tiff_file'] 
    tiff_image = Image.open(tiff_file)
    if tiff_file and (tiff_file.filename.endswith('.tif') or tiff_file.filename.endswith('.tiff')) :
        tiff_image = tiff_image.convert('RGB')
    output_buffer = BytesIO()
    tiff_image.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    return Response(output_buffer, content_type='image/png')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
