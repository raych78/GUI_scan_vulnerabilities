
from tkinter import *

from Source.Pages.PentestOWASP import PentestOWASP
from Source.Pages.PentestReseau import PentestReseau
from Source.Pages.BruteforceHash import BruteforceHash 
from Source.Pages.DicoHash import DicoHash

class StartPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		label = Label(self, foreground= 'red' ,text=
		"Avertissement juridique: Utiliser cet outil pour attaquer des cibles sans consentement mutuel préalable est illégale."
		+"\n"+
		"Il incombe à celui qui l'utilise de respecter toutes les lois locales, étatiques et fédérales applicables."
		+"\n"+
		"Les développeurs ne vont assumer aucune responsabilité et ne sont pas responsables de tout abus ou dommage causé par ce programme"
		)
		label.pack(padx=10, pady=10)
		self.configure(background='black')
		

		#Gif 
		frameCnt = 17
		frames = [PhotoImage(file="./Source/Images/hacker-pc.gif", format = 'gif -index %i' %(i)) for i in range(frameCnt)]
		def update(ind):
			frame = frames[ind]
			ind += 1
			if ind == frameCnt:
				ind = 0
			label.configure(image=frame)
			self.after(100, update, ind)
		label = Label(self, background="black")
		label.pack()
		self.after(0, update, 0)
		page_one = Button(self, text="Pentest des vulnérabilités OWASP", command=lambda:controller.show_frame(PentestOWASP))
		page_one.pack()
		page_two = Button(self, text="Pentest réseau ", command=lambda:controller.show_frame(PentestReseau))
		page_two.pack()
		page_three = Button(self,text="Pentest ingénierie social", command=lambda:controller.show_frame(PageThree))
		page_three.pack()
		page_four = Button(self,text="Password cracker Bruteforce", command=lambda:controller.show_frame(BruteforceHash))
		page_four.pack()
		page_five = Button(self,text="Password cracker Dictionary", command=lambda:controller.show_frame(DicoHash))
		page_five.pack()