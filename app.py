import os
import platform
import subprocess
import uuid
from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import PyPDF2
import pyttsx3

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    """Check if the file has a valid PDF extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(pdf_path):
    """
    Reads a PDF file and returns the cleaned text content.
    Using a list to collect text parts is more efficient than string concatenation.
    """
    text_parts = []
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            
            
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    
                    cleaned_text = content.replace('\n', ' ')
                    text_parts.append(cleaned_text)
                    
        return " ".join(text_parts)
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return None

def generate_audio(text, output_path):
    """
    Generates audio file based on OS. 
    MacOS uses native 'say', others use pyttsx3.
    """
    system_os = platform.system()
    
    if system_os == "Darwin":
        
        temp_txt_path = output_path.replace('.m4a', '.txt')
        
        with open(temp_txt_path, "w", encoding='utf-8') as f:
            f.write(text)
            
        
        subprocess.run(["say", "-v", "Samantha", "-f", temp_txt_path, "-o", output_path])
        
        
        if os.path.exists(temp_txt_path):
            os.remove(temp_txt_path)
            
    else:
        
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    
    if 'pdf_file' not in request.files:
        return "No file part", 400
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return "No selected file", 400

    if file and allowed_file(file.filename):
        
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        saved_pdf_name = f"{unique_id}_{filename}"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], saved_pdf_name)
        
        file.save(pdf_path)

        try:
            
            full_text = extract_text_from_pdf(pdf_path)
            
            if not full_text or len(full_text.strip()) == 0:
                return "Could not extract text from this PDF. It might be an image-only PDF."

            
            is_mac = platform.system() == "Darwin"
            output_ext = "m4a" if is_mac else "mp3"
            output_filename = f"audiobook_{unique_id}.{output_ext}"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            
            generate_audio(full_text, output_path)

            
            @after_this_request
            def cleanup(response):
                try:
                    if os.path.exists(pdf_path):
                        os.remove(pdf_path)
                    
                except Exception as e:
                    print(f"Error cleaning up files: {e}")
                return response

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            print(f"Conversion Error: {e}")
            return "An error occurred during conversion.", 500
            
    return "Invalid file type. Please upload a PDF."

if __name__ == '__main__':
   
    app.run(debug=True, port=5001)
