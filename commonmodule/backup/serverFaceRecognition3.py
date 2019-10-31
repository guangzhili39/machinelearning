# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 16:57:46 2019

@author: 19083
"""
import sys
sys.path.append(r"c:\users\19083\anaconda3\lib\site-packages")    

from flask import Flask, render_template

#import faceRecognition as fr
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('template.html')
@app.route('/my_login/')
def login():
    import faceVerify2 as fv
    name = fv.faceVerify()
            
    return render_template('template.html', name=name)

@app.route('/my_signin/')
def signin():
    import faceRegistration as fr
    
    ret,name = fr.faceRegistration()
    if ret==0:
        import faceModelBuild as model
        model.faceModelBuild(name)
        return render_template('template.html',result="registered successfully!")
    return render_template('template.html',result="already registered!")

if __name__=='__main__':
#    app.run(debug=True)
# construct the argument parser and parse command line arguments
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", type=str, required=True,
		help="ip address of the device")
    ap.add_argument("-o", "--port", type=int, default=5000,
		help="ephemeral port number of the server (1024 to 65535)")
    args = vars(ap.parse_args())

	# start a thread that will perform motion detection
#    t = threading.Thread(target=detect_motion, args=(
#		args["frame_count"],))
#    t.daemon = True
#    t.start()

	# start the flask app
    app.run(host=args["ip"], port=args["port"], debug=True)
#		threaded=True, use_reloader=False)

# release the video stream pointer
# vs.stop()