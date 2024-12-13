import http.server
import socketserver
import subprocess

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/start-user-gui":
            try:
                # Terminate any previous Streamlit session
                subprocess.call(["taskkill", "/F", "/IM", "streamlit.exe"], shell=True)

                # Run user_gui.py
                subprocess.Popen(["streamlit", "run", "user_gui.py"])
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"User GUI started successfully.")
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
        else:
            self.send_response(404)
            self.end_headers()

# Start the HTTP server
PORT = 8000
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
