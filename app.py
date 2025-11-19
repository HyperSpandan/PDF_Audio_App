from flask import Flask, render_template, request, send_file
import os
import platform
import subprocess
import PyPDF2
import pyttsx3

app = Flask(__name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'pdf_file' not in request.files:
        return "No file uploaded"
    
    file = request.files['pdf_file']
    
    if file.filename == '':
        return "Please select a valid PDF file"

    pdf_filename = "source_document.pdf"
    pdf_path = os.path.join('uploads', pdf_filename)
    file.save(pdf_path)

    text_string = ""

    try:
        pdf_obj = open(pdf_path, 'rb')
        pdf_reader = PyPDF2.PdfReader(pdf_obj)
        for i in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[i]
            extracted = page.extract_text()
            
            if extracted:
                cleaned = extracted.replace('\n', ' ')
                text_string += cleaned + " "
        
        pdf_obj.close()

        current_os = platform.system()
        
        output_filename = ""
        output_path = ""

        if current_os == "Darwin":
            output_filename = "audiobook.m4a"
            output_path = os.path.join('uploads', output_filename)
            
            txt_path = os.path.join('uploads', "temp_text.txt")
            f = open(txt_path, "w")
            f.write(text_string)
            f.close()
            subprocess.run(["say", "-v", "Samantha", "-f", txt_path, "-o", output_path])
            
        else:
            output_filename = "audiobook.mp3"
            output_path = os.path.join('uploads', output_filename)
            
            engine = pyttsx3.init()
            engine.save_to_file(text_string, output_path)
            engine.runAndWait()

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("Error occurred:", e)
        return "Something went wrong. Please check if the PDF is valid."

if __name__ == '__main__':
    app.run(debug=True, port=5001)