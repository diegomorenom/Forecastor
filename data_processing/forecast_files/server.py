from http.server import SimpleHTTPRequestHandler, HTTPServer

# Set the directory containing your CSV file
DIRECTORY = 'C:\\Users\\diego\\OneDrive\\Documentos\\SoftwareProjects\\Forecastor\\data_processing\\forecast_files'

# Set the port number for the server
PORT = 8000

class CSVFileHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
        super().end_headers()

# Create the server
httpd = HTTPServer(('localhost', PORT), CSVFileHandler)

# Start the server
print(f'Server is running on port {PORT}')
httpd.serve_forever()
