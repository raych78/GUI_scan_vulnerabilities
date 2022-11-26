from tkinter import *
from tkinter import ttk
import tkinter
import xss_scanner
import dos_attack

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
		frameCnt = 17
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
		frameSQL.place(x=1700,y=30,height=250,width=500)
		

		frameBruteForceLogin = LabelFrame(self, text = "Analyse des failles du login")
		frameBruteForceLogin.place(x=30,y=400,height=250,width=500)


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

		dos_frame = ttk.Frame(self, width=10000, height=100000,)
		dos_frame.pack(side ="top",padx=30, pady=30, anchor="w")

		
# Enrengistrement des IP src et dest 
		IP_Source = tkinter.StringVar()
		IP_Destination = tkinter.StringVar()

# @IP SOURCE
		ip_source_label = ttk.Label(dos_frame, text="@IP SOURCE:")
		ip_source_label.pack()

		ip_source_entry = ttk.Entry(dos_frame, textvariable=IP_Source)
		ip_source_entry.pack()
		ip_source_entry.focus()

# @IP DESTINATION

		ip_destination_label = ttk.Label(dos_frame, text="@IP SOURCE:")
		ip_destination_label.pack()

		ip_destination_entry = ttk.Entry(dos_frame, textvariable=IP_Destination)
		ip_destination_entry.pack()
		ip_destination_entry.focus()

#Definition de la fonction appelé par le bouton 

		def OnClick_DOS():
				result_label.config(text="")
			

# Lancer et stopper l'attaque DOS avec le boutton
		dos_button_start = ttk.Button(dos_frame, text="Lancer l'attaque DOS", command=OnClick_DOS)
		dos_button_start.pack()

		dos_button_stop = ttk.Button(dos_frame, text="Stopper l'attaque DOS", command=OnClick_DOS)
		dos_button_stop.pack()

#Affiche les résultats ici
		result_label = ttk.Label(dos_frame, text="Vos resultats apparaîssent ici...")
		result_label.pack()



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