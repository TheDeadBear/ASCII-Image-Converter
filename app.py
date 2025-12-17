from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ascii_magic import AsciiArt
from PIL import Image, ImageEnhance
import io
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Settings from existing Python scripts
DEFAULT_COLUMNS = 120
DEFAULT_CHAR_SET = " .'`^\",:;Il!i~+_-?][}{1)(|\\/*tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
DEFAULT_MONOCHROME = True

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/convert', methods=['POST'])
def convert():
    try:
        print("Received convert request")  # Debug
        
        if 'image' not in request.files:
            print("No image in request")
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        if file.filename == '':
            print("Empty filename")
            return jsonify({'error': 'No file selected'}), 400

        print(f"Processing file: {file.filename}")
        
        # Get parameters from form
        columns = int(request.form.get('columns', DEFAULT_COLUMNS))
        contrast = float(request.form.get('contrast', 1.5))
        
        print(f"Columns: {columns}, Contrast: {contrast}")
        
        # Open image with Pillow
        img = Image.open(file.stream)
        print(f"Image opened: {img.size}")
        
        # Apply contrast if needed
        if contrast != 1.0:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        # Convert to ASCII using your existing method
        art = AsciiArt.from_pillow_image(img)
        ascii_text = art.to_ascii(
            columns=columns,
            char=DEFAULT_CHAR_SET,
            monochrome=DEFAULT_MONOCHROME
        )
        
        print(f"Conversion successful, {len(ascii_text)} characters")
        return jsonify({'ascii': ascii_text}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting ASCII Converter Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='127.0.0.1', port=5000)
