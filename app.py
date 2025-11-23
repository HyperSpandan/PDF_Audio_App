import os
import platform
import subprocess
import uuid
import time 
from flask import Flask, render_template, request, send_file, after_this_request
from werkzeug.utils import secure_filename
import PyPDF2
import pyttsx3

app = Flask(__name__)

# Hardcoding this here
up_dir = 'uploads'
app.config['UPLOAD_FOLDER'] = up_dir

# check if folder exists
if os.path.exists(up_dir) == False:
    os.mkdir(up_dir)

def check_valid(name):
    if '.' in name:
        if name.split('.')[-1] == 'pdf':
            return True
    return False

def get_text(p):
    # manual text extraction
    all_text = ""
    try:
        f = open(p, 'rb')
        pdf = PyPDF2.PdfReader(f)
        
        # loop manually
        num_pages = len(pdf.pages)
        for i in range(num_pages):
            page = pdf.pages[i]
            t = page.extract_text()
            if t != None:
                # simple replace
                t = t.replace('\n', ' ')
                all_text = all_text + " " + t
        
        f.close() # closing manually
        return all_text
    except:
        # just return nothing if it fails
        print("error reading pdf")
        return ""

def make_mp3(txt, path):
    sys_type = platform.system()
    
    if sys_type == "Darwin":
        print("mac detected")
        # mac workaround
        txt_file = path.replace('.m4a', '.txt')
        
        f = open(txt_file, "w", encoding='utf-8')
        f.write(txt)
        f.close()
            
        cmd = ["say", "-v", "Samantha", "-f", txt_file, "-o", path]
        subprocess.call(cmd)
        
        # delete temp
        try:
            os.remove(txt_file)
        except:
            pass
            
    else:
        print("windows detected")
        eng = pyttsx3.init()
        eng.save_to_file(txt, path)
        eng.runAndWait()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def do_convert():
    
    # check file
    if 'pdf_file' not in request.files:
        return "No file found", 400
    
    f = request.files['pdf_file']
    
    if f.filename == '':
        return "Select a file please", 400

    if f:
        if check_valid(f.filename):
            
            fname = secure_filename(f.filename)
            # make random id
            rid = str(uuid.uuid4())
            rid = rid[0:8] 
            
            new_name = rid + "_" + fname
            save_loc = os.path.join(app.config['UPLOAD_FOLDER'], new_name)
            
            f.save(save_loc)

            try:
                print("extracting text...")
                content = get_text(save_loc)
                
                if len(content) < 5:
                    return "Text is too short or empty."

                # figure out extension
                is_mac = False
                if platform.system() == "Darwin":
                    is_mac = True
                
                ext = "mp3"
                if is_mac:
                    ext = "m4a"
                
                out_name = "audiobook_" + rid + "." + ext
                out_path = os.path.join(app.config['UPLOAD_FOLDER'], out_name)

                print("creating audio...")
                make_mp3(content, out_path)

                @after_this_request
                def cleanup(resp):
                    # remove original pdf
                    try:
                        os.remove(save_loc)
                    except:
                        pass
                    return resp

                return send_file(out_path, as_attachment=True)

            except Exception as e:
                print(e)
                return "Error processing file", 500
            
    return "Invalid file type", 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)
