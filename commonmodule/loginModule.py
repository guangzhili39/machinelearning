# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:01:54 2019

@author: 19083
"""
def getusername():
    import tkinter as tk
    name=""
    action=""
    def get1():
        nonlocal name
        name = guess.get()
        nonlocal action
        action = "signin"
        root.destroy()
    def get2():
        nonlocal name
        name = guess.get()
        nonlocal action
        action = "login"
        root.destroy()
        
    root = tk.Tk()
    guess = tk.StringVar()

    tk.Entry(textvariable=guess).grid(column=1, row=0)
    tk.Button(root, text="Sign-In", command=get1).grid(column=1, row=1)
    tk.Button(root, text="Log-In", command=get2).grid(column=2, row=1)
    tk.Label(root, text="name: ").grid(column=0, row=0)

    root.mainloop()
    return action,name