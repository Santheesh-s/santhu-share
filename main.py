import os
import cgi
import socket
import threading
import http.server
import socketserver
import logging
import tkinter as tk
from tkinter import filedialog, messagebox

# Constants
PORT = 8080


from kivy.utils import platform
if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.INTERNET, Permission.WRITE_EXTERNAL_STORAGE])
    
# Directories setup
UPLOAD_DIR = "./Download/"
LOG_DIR = "./santhusshare/"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
LOG_FILE = os.path.join(LOG_DIR, "server.log")
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_form)

    def do_POST(self):
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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Using Google's public DNS server to get the local IP
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address

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

class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.server_thread = None

        self.server_status_label = tk.Label(root, text="Server is stopped", font=("Arial", 7))
        self.server_status_label.pack(pady=10)

        start_button = tk.Button(root, text="Start Server", command=self.start_server, width=20, height=2, bg="#1ABC9C", fg="white", font=("Arial", 5))
        start_button.pack(pady=10)

        stop_button = tk.Button(root, text="Stop Server", command=self.stop_server, width=20, height=2, bg="#E74C3C", fg="white", font=("Arial", 5))
        stop_button.pack(pady=10)

    def start_server(self):
        try:
            if self.server_thread is None or not self.server_thread.is_alive():
                self.server_thread = ServerThread()
                self.server_thread.start()
                self.server_status_label.config(text=f"Server is listening on http://{get_local_ip()}:{PORT}")
                logging.info("Server started")
        except Exception as e:
            logging.error(f"Error starting server: {e}")
            messagebox.showerror("Error", f"Error starting server: {e}")

    def stop_server(self):
        try:
            if self.server_thread is not None and self.server_thread.is_alive():
                self.server_thread.stop()
                self.server_thread.join()
                self.server_thread = None
                self.server_status_label.config(text="Server is stopped")
                logging.info("Server stopped")
        except Exception as e:
            logging.error(f"Error stopping server: {e}")
            messagebox.showerror("Error", f"Error stopping server: {e}")

def main():
    root = tk.Tk()
    root.title("Tkinter File Upload Server")
    root.geometry("400x300")
    app = TkinterApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()