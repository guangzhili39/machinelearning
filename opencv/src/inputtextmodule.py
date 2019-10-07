# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:01:54 2019

@author: 19083
"""
def getusername():
    import tkinter as tk
    name=""
    def get():
        nonlocal name
        name = guess.get()
        root.destroy()

    root = tk.Tk()
    guess = tk.StringVar()

    tk.Entry(textvariable=guess).grid(column=1, row=0)
    tk.Button(root, text="Enter", command=get).grid(column=2, row=0)
    tk.Label(root, text="name: ").grid(column=0, row=0)

    root.mainloop()
    return name