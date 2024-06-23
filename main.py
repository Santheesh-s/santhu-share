import os
import http.server
import threading
import socketserver
import logging
import cgi

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Constants
PORT = 8080
UPLOAD_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "Download")
LOG_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "santhusshare")

# Ensure directories exist and set permissions
try:
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    os.chmod(UPLOAD_DIR, 0o755)  # Ensure correct permissions
    os.chmod(LOG_DIR, 0o755)     # Ensure correct permissions
except OSError as e:
    logging.error(f"Error creating directories: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename=os.path.join(LOG_DIR, 'server.log'))

# HTML form for file upload
html_form = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload</title>
</head>
<body>
    <h2>Upload Files</h2>
    <form id="upload-form" action="/" method="post" enctype="multipart/form-data">
        <input type="file" name="file" multiple>
        <input type="submit" value="Upload">
    </form>
    <div id="progress-bar-container" style="display:none;">
        <progress id="upload-progress" max="100" value="0"></progress>
        <div id="progress-label"></div>
    </div>

    <script>
        var form = document.getElementById('upload-form');
        var progressBarContainer = document.getElementById('progress-bar-container');
        var progressBar = document.getElementById('upload-progress');
        var progressLabel = document.getElementById('progress-label');

        form.addEventListener('submit', function(event) {
            event.preventDefault();
            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();

            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    var percentComplete = (event.loaded / event.total) * 100;
                    progressBar.value = percentComplete;
                    progressLabel.textContent = percentComplete.toFixed(2) + '%';
                    progressBarContainer.style.display = 'block';
                }
            };

            xhr.onload = function() {
                progressBarContainer.style.display = 'none';
                if (xhr.status === 200) {
                    alert('Files uploaded successfully!');
                } else {
                    alert('Failed to upload files. Please try again.');
                }
            };

            xhr.open('POST', '/');
            xhr.send(formData);
        });
    </script>
</body>
</html>
"""

class FileUploadHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_form)
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
                )

                if 'file' not in form:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"No files provided")
                    return

                file_items = form['file']
                if not isinstance(file_items, list):
                    file_items = [file_items]

                for file_item in file_items:
                    file_data = file_item.file.read()
                    file_name = file_item.filename
                    file_path = os.path.join(UPLOAD_DIR, file_name)

                    try:
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        logging.info(f"Uploaded file: {file_name}")
                    except Exception as e:
                        logging.error(f"Failed to write file {file_name}: {e}")
                        self.send_response(500)
                        self.end_headers()
                        self.wfile.write(b"Failed to upload file")
                        return

                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Files uploaded successfully!")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid form submission")
        except Exception as e:
            logging.error(f"Error processing POST request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")

class ServerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.httpd = None

    def run(self):
        try:
            local_ip = get_local_ip()
            self.httpd = socketserver.TCPServer((local_ip, PORT), FileUploadHandler)
            logging.info(f"Server is listening on {local_ip}:{PORT}")
            self.httpd.serve_forever()
        except Exception as e:
            logging.error(f"Server error: {e}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()

def get_local_ip():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

class SanthuShareApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Server status label
        self.server_status_label = Label(text='Server is stopped')
        layout.add_widget(self.server_status_label)

        # Start server button
        start_button = Button(text='Start Server', on_press=self.start_server)
        layout.add_widget(start_button)

        # Stop server button
        stop_button = Button(text='Stop Server', on_press=self.stop_server)
        layout.add_widget(stop_button)

        return layout

    def start_server(self, instance):
        try:
            self.server_thread = ServerThread()
            self.server_thread.start()
            self.server_status_label.text = f"Server is listening on {get_local_ip()}:{PORT}"
            logging.info("Server started")
        except Exception as e:
            logging.error(f"Error starting server: {e}")

    def stop_server(self, instance):
        try:
            if self.server_thread:
                self.server_thread.stop()
                self.server_thread.join()
                self.server_thread = None
                self.server_status_label.text = "Server is stopped"
                logging.info("Server stopped")
        except Exception as e:
            logging.error(f"Error stopping server: {e}")

if __name__ == '__main__':
    SanthuShareApp().run()
