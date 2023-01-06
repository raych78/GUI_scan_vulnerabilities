from tkinter import *

#import Source.Scripts.dos_attack as dos_attack
from Source.Pages.StartPage import StartPage

from Source.Pages.PentestOWASP import PentestOWASP
from Source.Pages.PentestReseau import PentestReseau
from Source.Pages.BruteforceHash import BruteforceHash 
from Source.Pages.DicoHash import DicoHash


class App(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		#Setup Menu
		MainMenu(self)
		#Setup Frame
		container = Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)

		self.frames = {}
		global controller
		controller = self
		for F in (StartPage, PentestOWASP, PentestReseau, BruteforceHash ,DicoHash):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)	
	def show_frame(self, context):
		frame = self.frames[context]
		frame.tkraise()



'''
class PageThree(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		label = Label(self, text="Page Two")
		label.pack(padx=10, pady=10)
		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack()
		page_one = Button(self, text="Page One", command=lambda:controller.show_frame(PageOne))
		page_one.pack()
'''

	#TODO add Wifi



		


class MainMenu:
	def __init__(self, master):
		global controller
		menubar = Menu(master)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_command(label="StartPage", command=lambda:controller.show_frame(StartPage))
		master.config(menu=menubar)


