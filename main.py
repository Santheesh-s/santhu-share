import os
import cgi
import socket
import threading
import logging
import sys
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE])

import http.server
import socketserver

# Constants
PORT = 8080
DOWNLOAD_DIR = "/storage/emulated/0/Download/"
OBB_DIR = "/storage/emulated/0/santhusshare"
LOG_FILE = os.path.join(OBB_DIR, "server.log")

# Ensure directories exist
os.makedirs(OBB_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_local_ip():
    """Get the local IP address of the machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.254.254.254', 1))
        ip_address = s.getsockname()[0]
    except Exception as e:
        logging.error(f"Failed to get local IP: {e}")
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

# HTML form for file upload
html_form = b"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Upload</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        h2 {
            margin-top: 0;
        }
        input[type="file"] {
            margin-bottom: 10px;
        }
        #progress-bar {
            width: 100%;
            background-color: #f3f3f3;
            border-radius: 13px;
            overflow: hidden;
        }
        #progress-bar-fill {
            height: 20px;
            background-color: #4CAF50;
            width: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Upload Files</h2>
        <form id="upload-form" action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" multiple>
            <input type="submit" value="Upload">
        </form>
        <div id="progress-bar">
            <div id="progress-bar-fill"></div>
        </div>
    </div>
    <script>
        document.getElementById('upload-form').onsubmit = function(e) {
            e.preventDefault();
            var form = e.target;
            var formData = new FormData(form);
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/', true);

            xhr.upload.onprogress = function(event) {
                if (event.lengthComputable) {
                    var percentComplete = (event.loaded / event.total) * 100;
                    document.getElementById('progress-bar-fill').style.width = percentComplete + '%';
                }
            };

            xhr.onload = function() {
                if (xhr.status == 200) {
                    alert('Files uploaded successfully!');
                } else {
                    alert('Failed to upload files.');
                }
                document.getElementById('progress-bar-fill').style.width = '0%';
            };

            xhr.send(formData);
        };
    </script>
</body>
</html>
"""

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for file upload requests."""
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_form)
        except Exception as e:
            logging.error(f"Error handling GET request: {e}")
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        try:
            ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
            if ctype == 'multipart/form-data':
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST',
                             'CONTENT_TYPE': self.headers['Content-Type']}
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
                    file_path = os.path.join(DOWNLOAD_DIR, file_name)

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
            logging.error(f"Error handling POST request: {e}")
            self.send_response(500)
            self.end_headers()

class ServerThread(threading.Thread):
    """Thread class to run the server."""
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
        logging.info("Server has stopped.")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()

class SanthusShareApp(App):
    def build(self):
        self.server_thread = None
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.server_status = Label(text="Server is stopped", font_size='20sp')
        layout.add_widget(self.server_status)

        start_button = Button(text="Start Server", size_hint=(1, None), height=50, background_color=(0.29, 0.63, 0.22, 1))
        start_button.bind(on_press=self.start_server)
        layout.add_widget(start_button)

        stop_button = Button(text="Stop Server", size_hint=(1, None), height=50, background_color=(0.95, 0.26, 0.21, 1))
        stop_button.bind(on_press=self.stop_server)
        layout.add_widget(stop_button)

        return layout

    def start_server(self, instance):
        try:
            if self.server_thread is None or not self.server_thread.is_alive():
                self.server_thread = ServerThread()
                self.server_thread.start()
                self.server_status.text = f"Server is listening on http://{get_local_ip()}:{PORT}"
                logging.info("Server started")
            else:
                logging.warning("Server is already running")
        except Exception as e:
            logging.error(f"Error starting server: {e}")

    def stop_server(self, instance):
        try:
            if self.server_thread is not None and self.server_thread.is_alive():
                self.server_thread.stop()
                self.server_thread.join()
                self.server_thread = None
                self.server_status.text = "Server is stopped"
                logging.info("Server stopped")
            else:
                logging.warning("Server is not running")
        except Exception as e:
            logging.error(f"Error stopping server: {e}")

if __name__ == '__main__':
    SanthusShareApp().run()
