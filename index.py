import Tkinter
import tkMessageBox
import subprocess

top = Tkinter.Tk()

def helloCallBack():
   cmd = 'scrapy crawl dataspider'
   p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()