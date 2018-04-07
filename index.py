import Tkinter
import tkMessageBox
import subprocess

top = Tkinter.Tk()

top.title("Fenster 1")
top.geometry("100x100")

def helloCallBack():
   cmd = 'scrapy crawl dataspider'
   p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

B = Tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
top.mainloop()