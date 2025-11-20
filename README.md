PDF to Audiobook Converter

Overview:
  The PDF to Audiobook Converter is a Python-based web application designed to assist users in consuming written content through audio. By         leveraging text-to-speech (TTS) technologies, this tool converts standard PDF documents into downloadable audio files (MP3 or M4A). The          application features an intelligent operating system detection system that optimizes the audio generation process based on whether the host      machine is running macOS or Windows.

Features:
  -Web-Based Interface: Simple, user-friendly drag-and-drop interface built with HTML and CSS.

  -Smart OS Detection:
    macOS: Utilizes the native say command for high-quality, efficient synthesis and outputs .m4a files.
    Windows: Utilizes the pyttsx3 library for offline conversion and outputs .mp3 files.

  -Text Pre-processing: automatically cleans text artifacts (such as line breaks within sentences) to ensure smooth, natural-sounding audio         playback.

  -Local Processing: All file conversion happens locally on the machine, ensuring data privacy and offline functionality.


Technologies & Tools Used:

  Language: Python 3.x

  Web Framework: Flask

  PDF Processing: PyPDF2

  Audio Synthesis:
  pyttsx3 (Windows)
  subprocess / Native say command (macOS)

  Frontend: HTML5, CSS3


Steps to Install & Run:

  Prerequisites:
  Ensure you have Python 3 installed on your system.

  Installation:
  Clone the repository to your local machine:

  git clone <your-repository-url>
  cd <your-repository-folder>


  Install the required Python dependencies:
  pip install flask PyPDF2 pyttsx3


(Note: macOS users may need to run pip3 install ... depending on their configuration).

  Run the application:
  python app.py


  Open your web browser and navigate to:
  [http://127.0.0.1:5001](http://127.0.0.1:5001)


Instructions for Testing:
  Prepare a PDF: Locate a PDF file containing selectable text (scanned images without OCR will not work).

  Upload: On the homepage, click "Choose File" and select your PDF.

  Convert: Click the "Convert to Audio" button.

  Download: * If on Mac, the browser will download an audiobook.m4a file.

  If on Windows, the browser will download an audiobook.mp3 file.

  Playback: Open the downloaded file in your preferred media player to verify the audio content matches the PDF text.
