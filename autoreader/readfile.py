# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 09:43:30 2019

@author: 19083
"""
import pyttsx3
import os,sys
import re

def say(engine,str):
    engine.say(str)
    engine.runAndWait()

def read():
   filepath = sys.argv[1]

   if not os.path.isfile(filepath):
       print("File path {} does not exist. Exiting...".format(filepath))
       sys.exit()
       
   engine = pyttsx3.init() 
   with open(filepath) as fp:
       
       text = fp.read().rstrip()
       text = text.replace("\n","")
       pattern = re.compile(r"[;,?!.] ")
       sentences = pattern.split(text)
       
       for sentence in sentences:
           say(engine,sentence)


def webpagehighlight(url):
    from bs4 import BeautifulSoup
    import requests

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, features="lxml")
    for bold in soup.findAll('b'):
        print(bold.contents)
       
if __name__ == '__main__':
#    read()
     webpagehighlight("https://stackoverflow.com/questions/52119710/extract-highlight-text-on-webpage")  
     