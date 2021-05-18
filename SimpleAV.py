# -*- coding: utf-8 -*-
"""
Created on Sun May  9 07:37:55 2021

"""

import pyclamd
import os
import psutil
import tkinter
from tkinter import *
from tkinter import filedialog
import sys
import threading
from queue import Queue

cd = pyclamd.ClamdAgnostic()
viruses = []

global q

def threadScan():
    t = threading.Thread(target = ScanPath)
    t.start()

def threadProcess():
    t = threading.Thread(target = ScanProcesses)
    t.start()
    
def ScanPath():
    viruses.clear()
    path = filedialog.askdirectory()
    for root, dirs, files in os.walk(path):
        for file in files:
            text = 'Scanning: ' + file + '\n'
            q.put(text)
            virus = cd.scan_file(os.path.join(root,file))
            if virus != None:
                if list(virus.values())[0][0] != 'ERROR':
                    viruses.append(virus)
    for virus in viruses:
        for key in virus:
            text = list(virus.get(key))[0] + key + '\n'
            q.put(text)
    if not virus:
        q.put("No viruses found!")

def ScanProcesses():
    viruses.clear()
    for p in psutil.process_iter():
        try:
            path = p.exe()
            if path != "":
                text = 'Scanning: ' + path + '\n'
                q.put(text)
                virus = cd.scan_file(path)
                if virus != None:
                    if list(virus.values())[0][0] != 'ERROR':
                        viruses.append(virus)
        except psutil.AccessDenied:
            text = "Access Denied for " + p.name() + '\n'
            q.put(text)
    if not virus:
            q.put("No viruses found!")
    for virus in viruses:
        for key in virus:
            text = list(virus.get(key))[0] + key + '\n'
            q.put(text)

# ScanProcesses()

def WriteToWindow():
    while not q.empty():
        t.insert(END, q.get())
        t.see("end")
    window.after(100, WriteToWindow)

window = Tk()  
window.geometry("720x480")  
window.title('Simple Antivirus')
window.configure(bg = 'black')

q = Queue()

def DeleteFiles():
    for virus in viruses:
        path = list(virus.keys())[0]
        path = path[4:]
        os.remove(path)
        t.insert(END, "Deleted: "+ path + "\n")
        t.see("end")

select = Button(window, text = "Scan Files...", command = threadScan)
select.pack(pady = 15, padx = 20, side = TOP, anchor = NW)  

process = Button(window, text = "Scan Processes", command = threadProcess)
process.pack(pady = 5, padx = 20, side = TOP, anchor = NW)  

select = Button(window, text = "Delete Files", command = DeleteFiles)
select.pack(pady = 15, padx = 20, side = TOP, anchor = NW)  

t = tkinter.Text(bg = 'black', fg = 'green', borderwidth = 0, highlightthickness = 0)
t.pack()

window.after(100, WriteToWindow)

window.mainloop()  