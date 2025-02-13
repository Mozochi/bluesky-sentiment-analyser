from tkinter import *
import time
from tkinter import ttk

class GUI:

    def __init__ (self):
        self.window = Tk()
        self.window.geometry("600x600")
        self.topLabel = Label(self.window, text='Facebook sentiment analyser')
        self.buttonText = 'Please enter a key word'
        self.buttonLabel = Label(self.window, text=self.buttonText)
        self.button = Button(self.window, text='submit', width=25)
        self.var = IntVar()
        self.radioButton1 = Radiobutton(self.window, text='keyword input', variable=self.var, value=0)
        self.radioButton2 = Radiobutton(self.window, text='profile input', variable=self.var, value=1)
        self.progressBar = ttk.Progressbar(self.window, orient="horizontal", length=300, mode="determinate")
        self.enter = Entry(self.window)
        self.topLabel.grid(row=0, column=0)
        self.buttonLabel.grid(row=2, column=0)
        self.enter.grid(row=2, column=1)
        self.button.grid(row=3, column=0)
        self.progressBar.grid(row=4, column=0)
        self.radioButton1.grid(row=1, column=0)
        self.radioButton2.grid(row=1, column=1)

    def startProgress(self):
        self.progressBar.start()

        # Simulate a task that takes time to complete
        for i in range(101):
          # Simulate some work
            time.sleep(0.05)
            self.progressBar['value'] = i
            # Update the GUI
            self.window.update_idletasks()
        self.progressBar.stop()

    def getData(self):
        return

    def analyse(self):
        return

    def submit(self):
        self.startProgress()
        self.getData()
        self.analyse()

    def changeButtonText(self):
        if (self.var.get() == 0):
            self.buttonText = 'Please enter a key word'

        else:
            self.buttonText = 'Please enter a profile name'
