# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:01:54 2019

@author: 19083
"""
def getusername(message=""):
    import tkinter as tk
    
    name=""
    action=""
    pwd=""
    def get1():
        nonlocal name
        name = guess.get()
        nonlocal action
        action = "signin"
        nonlocal pwd
        pwd = passw.get()
        root.destroy()
    def get2():
        nonlocal name
        name = guess.get()
        nonlocal action
        action = "login"
        root.destroy()

    def get3():
        nonlocal name
        name = guess.get()
        nonlocal action
        action = "pwdlogin"
        nonlocal pwd
        pwd = passw.get()
        root.destroy()
        
    root = tk.Tk()
    root.title("Facial Recognition")
    root.geometry('400x100')
    guess = tk.StringVar()
    passw = tk.StringVar()
    
    tk.Label(root, text="User Name:").grid(column=0, row= 0)
    tk.Label(root, text="Password:").grid(column=0, row= 1)
    
    tk.Entry(textvariable=guess).grid(column=1,columnspan=2,row=0)
    tk.Entry(textvariable=passw,show="*").grid(column=1,columnspan=2,row=1)

    tk.Button(root, text="Facial Sign-In", bg='orange',command=get1).grid(column=0, row=2)
    tk.Button(root, text="Facial Log-In", bg='orange', command=get2).grid(column=1, row=2)
    tk.Button(root, text="Password Log-In", bg='orange',command=get3).grid(column=2, row=2)
    
    tk.Entry(textvariable=guess).grid(column=1, row=0)
    tk.Label(root, text="Result:").grid(column=0,row = 3)
    tk.Label(root, text=message).grid(column=1,row = 3)
    
    root.mainloop()
    return action,name,pwd

if __name__ == '__main__':
    action,name,pwd = getusername("fake")
    print(action,name,pwd)