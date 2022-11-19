from tkinter import *
import xss_scanner

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

		for F in (StartPage, PageOne, PageTwo):
			frame = F(container, self)
			self.frames[F] = frame
			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(StartPage)	
	def show_frame(self, context):
		frame = self.frames[context]
		frame.tkraise()

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
		frameCnt = 12
		frames = [PhotoImage(file="GUI_scan_vulnerabilities/CompleteFrenchBluejay-size_restricted.gif", format = 'gif -index %i' %(i)) for i in range(frameCnt)]
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




		page_one = Button(self, text="Pentest des vulnérabilités OWASP", command=lambda:controller.show_frame(PageOne))
		page_one.pack()
		page_two = Button(self, text="Pentest réseau ", command=lambda:controller.show_frame(PageTwo))
		page_two.pack()
		page_three = Button(self,text="Pentest ingénierie social", command=lambda:controller.show_frame(PageThree))
		page_three.pack()	

class PageOne(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		inputUrl = Entry(self,text = "Lien du site",width=50)
		inputUrl.pack()
	
		label = Label(self, text="Scan des vulnerabilités OWASP")
		label.pack(padx=10, pady=10)
		frameXSS = LabelFrame(self, text = "Analyse des injections xss")
		frameXSS.place(x=30,y=30,height=250,width=500)
		
		frameSQL = LabelFrame(self, text = "Analyse des injections sql")
		frameSQL.place(x=1100,y=30,height=250,width=500)
		
		labelXSS = Label(frameXSS, text = "les resultats des failles xss apparaissent ici...")
		labelXSS.pack()
		
		def onClick():
			labelStartSCan = Label(self, text="Lancement du scan  en cours... ")
			labelStartSCan.pack()
			if xss_scanner.scan_xss(inputUrl.get()):
				labelXSS.config(text = "Faille XSS non permanente trouvé !" + "\n" + "Risque elevé" +"\n" + "Attaque utilisé : "+ "<Script>alert('hi')</script>")
				labelStartSCan = Label(self, text="Fin du scan !")
				button.pack()


		button = Button(self, text = "Lancer le scan !", command=onClick, bg = "red" , fg = "white")
		button.pack()

		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack()
		page_two = Button(self, text="Page Two", command=lambda:controller.show_frame(PageTwo))
		page_two.pack()

class PageTwo(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		label = Label(self, text="Page Two")
		label.pack(padx=10, pady=10)
		start_page = Button(self, text="Start Page", command=lambda:controller.show_frame(StartPage))
		start_page.pack()
		page_one = Button(self, text="Page One", command=lambda:controller.show_frame(PageOne))
		page_one.pack()


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


class MainMenu:
	def __init__(self, master):
		menubar = Menu(master)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		master.config(menu=menubar)


app = App()
app.mainloop()