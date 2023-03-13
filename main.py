import uuid

from main2 import app


if __name__ == '__main__':
    #do Flask-HTTPAuth
    # app.run( ssl_context=('host.crt', 'host.key'))
    app.run( debug=True, port=5000)