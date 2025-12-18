from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from PIL import Image
import io
import traceback

# Import configuration from ascii_convert_detailed.py
from ascii_convert_detailed import (
    DEFAULT_COLUMNS,
    DEFAULT_CHAR_SET,
    DEFAULT_MONOCHROME,
    ENHANCE_CONTRAST
)
from ascii_magic import AsciiArt

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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
        
        # Get parameters from form (use settings from ascii_convert_detailed.py)
        columns = int(request.form.get('columns', DEFAULT_COLUMNS))
        contrast = float(request.form.get('contrast', ENHANCE_CONTRAST))
        
        print(f"Columns: {columns}, Contrast: {contrast}")
        
        # Open image with Pillow
        img = Image.open(file.stream)
        print(f"Image opened: {img.size}")
        
        # Apply contrast enhancement (using logic from ascii_convert_detailed.py)
        if contrast != 1.0:
            from PIL import ImageEnhance
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)
        
        # Convert to ASCII using your existing method
        art = AsciiArt.from_pillow_image(img)
        ascii_text = art.to_ascii(
            columns=columns,
            char=DEFAULT_CHAR_SET,
            monochrome=False
        )
        html_ascii = art.to_html(
            columns=columns,
            char=DEFAULT_CHAR_SET,
            monochrome=False
        )
        print(f"Conversion successful, {len(ascii_text)} characters")
        return jsonify({'ascii': ascii_text, 'html': html_ascii}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting ASCII Converter Server...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, host='127.0.0.1', port=5000)
