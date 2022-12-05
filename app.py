import os

from flask import Flask, url_for
from flask import render_template

app = Flask(__name__)

@app.route('/')
def home():
    return '<a href="/spaceTracker">Enter Site</a>'
# @app.route('/hello/<name>')
@app.route('/spaceTracker')
def hello():
    # return '<p>Insert space tracker here</p>'
    return render_template('hello.html')

if __name__ == '__main__':
    # try:
        # motionDetectorProcess = Process(target=md)
        # motionDetectorProcess.start()
    # except:
        # print('Failed to start motion detector')
    # run() method of Flask class runs the application
	# on the local development server.
    app.run()
    # motionDetectorProcess.terminate()