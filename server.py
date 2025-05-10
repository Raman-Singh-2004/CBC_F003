import http.server
import socketserver
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the port
PORT = 8000

# Change directory to the current directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create a simple HTTP server
Handler = http.server.SimpleHTTPRequestHandler
Handler.extensions_map.update({
    '.html': 'text/html',
    '.js': 'application/javascript',
    '.css': 'text/css',
})

# Create the server
httpd = socketserver.TCPServer(("", PORT), Handler)

# Print server information
logging.info(f"Serving at http://localhost:{PORT}")
logging.info(f"Open http://localhost:{PORT}/index.html in your browser")

# Start the server
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    logging.info("Server stopped by user")
    httpd.server_close()
