from waitress import serve
from app import app
import socket

current_ip = socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    # or use waitress-serve --host 127.0.0.1 --port 5555 --call app:app --verbose
    serve(app, host=current_ip,port=5555,ident=True)