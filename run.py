from gevent.pywsgi import WSGIServer
from api.app import app

# Use WSGIServer to serve a production grade flask app
if __name__ == '__main__':  
    app.run(host="localhost", port=8080, debug=True)
    #WSGIServer(('0.0.0.0', 8000), app).serve_forever()