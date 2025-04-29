from flask import Flask, request, send_file
from PIL import Image
from io import BytesIO
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask Backend is Running!"

@app.route('/remove_exif', methods=['POST'])
def remove_exif():
    if 'image' not in request.files:
        return 'No image uploaded', 400

    file = request.files['image']
    unique_filename = os.path.join('uploads', f"{uuid.uuid4().hex}.jpg")
    file.save(unique_filename)

    image = Image.open(unique_filename)
    data = list(image.getdata())
    image_no_exif = Image.new(image.mode, image.size)
    image_no_exif.putdata(data)

    buffer = BytesIO()
    image_no_exif.save(buffer, format='JPEG')
    buffer.seek(0)

    os.remove(unique_filename)

    return send_file(buffer, as_attachment=True, download_name='cleaned_image.jpg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
