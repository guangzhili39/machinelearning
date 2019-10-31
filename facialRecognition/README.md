# this project uses face recognition for access control.
There are two versions: consumer version for PC/Laptop use only, which means the facial model is stored at local only. Enterprice
version uses client-server model. The facial model is generated and stored at the server side, which means a user can login from
any machine as long as it can access the server. It is for fun, but it would have many applications.

Consumer version is more mature: it has three buttons in a window: facial sign-in, facial login, password login.
For facial sign-in, user is required to input username, password. Click sign-in, the webcam will turn on few seconds, capture your facail 
images, generate model, save your password.
For facial login, you need to input username, click facial login, the webcom will turn on, ask one challege action to detect live face. If your 
face is not recognized, it returns unknow, if you did not perform the asked action in a random interval, it returns fake, otherwise return success.
For password login, in some special cases, such as dark, webcam will fail to recognize your face, you may still use password to login.
If python 3 was installed in your machine, your can go to the consumer directory, and run python GLIF.py, if not, can you ran dist\GLIF\GLIF.exe

For enterprise version, we need one server.py and one client.py. Server.py runs as a demon with its IP address, and listen on a specific 
port, all clients connect to the IP address and port using sockets. It is still in a very early stage. 
