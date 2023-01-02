from tkinter import *
from tkinter import ttk
import tkinter
import threading 
import queue

import requests
import xss_scanner
import dos_attack
import tkinter.filedialog
import HashedPassword_Attack


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
		for F in (StartPage, PageOne, PageTwo, PageFour,PageFive):
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
		frames = [PhotoImage(file="./hacker-pc.gif", format = 'gif -index %i' %(i)) for i in range(frameCnt)]
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
		page_four = Button(self,text="Password cracker Bruteforce", command=lambda:controller.show_frame(PageFour))
		page_four.pack()
		page_five = Button(self,text="Password cracker Dictionary", command=lambda:controller.show_frame(PageFive))
		page_five.pack()

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
		frameBruteForceLogin.place(x=30,y=350,height=550,width=500)

		Label_password_found= Label(frameBruteForceLogin, bg='#fff',text = "Le mdp trouvé sera affiché ici")
		Label_password_found.pack()

		#Entrer le lien de la page de login

		Label_login_url = Label(frameBruteForceLogin, text = "Entre le lien de l'url de la requête post du login !")
		Label_login_url.pack()

		login_url = StringVar()
		login_entry = ttk.Entry(frameBruteForceLogin, textvariable=login_url)
		login_entry.pack(fill=X)


		#Specifier le mail/username

		Label_login_username = Label(frameBruteForceLogin, text = "Entre le mail/username connu")
		Label_login_username.pack()

		login_username = StringVar()
		username_entry= ttk.Entry(frameBruteForceLogin, textvariable=login_username)
		username_entry.pack(fill=X)

		#Donner la possibilité de choisir le fichier dictionnaire

		Label_choose_dico = Label(frameBruteForceLogin, text = "Choisis le dictionnaire !")
		Label_choose_dico.pack()

		dictionary_choices = ["top 100 pwd", "rockYou", "LeakedPwd2022"]
		choicesvar = StringVar(value=dictionary_choices)
		l_dico = Listbox(frameBruteForceLogin, listvariable=choicesvar)
		l_dico.pack()

		#Donner la possibilité à l'user d'ajouter un dico 

		def open_file():
			f_types = [('*.txt')]
			file_path = tkinter.filedialog.askopenfilename()
			with open(file_path, 'r') as f:
				contents = f.read()
				print(contents)

# Create a button that will trigger the file dialog when clicked
		button_add_dico = Button(frameBruteForceLogin,text="Open File", command=open_file)
		button_add_dico.pack()

		#Implémentation du boutton pour lancer l'attaque par dictionaire

		def dico_attack():
			Label_password_found.configure(text ='Recherche du mdp en cours')

			data_null = {'email':'email', 'password':'password'}
			response_null = requests.post(login_url.get(),data =data_null)
			len_null = len(response_null.text)

			with open('Dictionaries/default-passwords.txt','r') as f:
				for word in f.readlines():
					password = word.replace("\n","")

					data = {'email':login_username.get(), 'password':password}
					response = requests.post(login_url.get(),data = data)
					if len_null != len(response.text):
						Label_password_found.configure(text ='MDP TROUVE !!!: ' + password)
						return data
						
			Label_password_found.configure(text ='Aucun mdp trouvé :( ')
			return "end of function"

		
		button_launch_dico_attack = Button(frameBruteForceLogin,text="Lancer l'attaque", command=dico_attack)
		button_launch_dico_attack.pack()


		labelXSS = Label(frameXSS, text = "les resultats des failles xss apparaissent ici...")
		labelXSS.pack()
		
		def onClick():
			labelStartSCan = Label(self, text="Lancement du scan  en cours... ")
			labelStartSCan.pack()
			if xss_scanner.scan_xss(inputUrl.get()):
				labelXSS.config(text = "Faille XSS non permanente trouvé !" + "\n" + "Risque elevé" +"\n" + "Attaque utilisé : "+ "<Script>alert('hi')</script>")
				labelStartSCan = Label(self, text="Fin du scan !")
				button.pack(fill=y)


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

class PageFour(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		#dos_frame = ttk.Frame(self, width=10000, height=100000,)
		#dos_frame.pack(side ="top",padx=30, pady=30, anchor="w")

		framebruteforce = LabelFrame(self, text = "Bruteforce hash (* are mandatory, others are optionnal)")
		framebruteforce.place(x=30,y=30,height=610,width=870)
#Base
		PasswordHash = StringVar()
		StartWith = StringVar()
		EndWith = StringVar()
		PasswordLength = IntVar()
		ToHash = StringVar()


#Hash
		PasswordHash_label = ttk.Label(framebruteforce, text="Hash cible* :")
		PasswordHash_label.pack()


		PasswordHash_entry = ttk.Entry(framebruteforce, textvariable=PasswordHash)
		PasswordHash_entry.pack(fill=X)
		PasswordHash_entry.focus()

#Start and End with
		StartWith_label = ttk.Label(framebruteforce, text="Password starts with :")
		StartWith_label.pack()

		StartWith_entry = ttk.Entry(framebruteforce, textvariable=StartWith)
		StartWith_entry.pack()
		StartWith_entry.focus()


		EndWith_label = ttk.Label(framebruteforce, text="Password ends with :")
		EndWith_label.pack()

		EndWith_entry = ttk.Entry(framebruteforce, textvariable=EndWith)
		EndWith_entry.pack()
		EndWith_entry.focus()

#Password length
		PasswordLength_label = ttk.Label(framebruteforce, text="Total password length (0 if unknown)")
		PasswordLength_label.pack()


		PasswordLength_entry = ttk.Entry(framebruteforce, textvariable=PasswordLength)
		PasswordLength_entry.pack()
		PasswordLength_entry.focus()

#Hash Algorithm
		Label_choose_algo = Label(framebruteforce, text = "Select an algorythm*")
		Label_choose_algo.pack()

		Algorithms_choices = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s','sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128','shake_256']
		Algo = StringVar(value=Algorithms_choices)
		list_algo = Listbox(framebruteforce, listvariable=Algo, selectmode=SINGLE)
		list_algo.pack()
#Definition de la fonction appelé par le bouton 
		killing_queue = queue.Queue()
		return_queue = queue.Queue()

		threadBF = threading.Thread()
		threadOut = threading.Thread()

		def startBF():
			i= list_algo.curselection()
			killing_queue.put(False)

			Arguments = [str(PasswordHash.get()),killing_queue,return_queue, int(PasswordLength.get()), str(StartWith.get()), str(EndWith.get()), str(list_algo.get(i))]
			if Arguments[3]==0 : Arguments[3]=1
			threadBF = threading.Thread(target=HashedPassword_Attack.bruteForce_Hash, args=Arguments, daemon=True)
			threadBF.start()

			threadOut = threading.Thread(target=DisplayOut, daemon=True)
			threadOut.start()
			return threadBF.name

		
		def stopBF():

			killing_queue.put(True)
			
# Launch and stop
		Bruteforce_Start = ttk.Button(framebruteforce, text="Find Password", command=startBF)
		Bruteforce_Start.pack()

		Bruteforce_Stop = ttk.Button(framebruteforce, text="Stop", command=stopBF)
		Bruteforce_Stop.pack()

		global LabelOut

		LabelOut = Label(framebruteforce, text="Waiting for orders")
		LabelOut.pack()
		def DisplayOut():
			global LabelOut
			while True:
				try:
					textOut = return_queue.get(timeout=5)
					LabelOut.configure(text=textOut)
					if textOut.startswith("Password"):
						break

				except queue.Empty:
					pass

		ToHash_label = ttk.Label(framebruteforce, text="\n \n \n Want to hash something? Fill in text and select the hash method up there")
		ToHash_label.pack()
		

		ToHash_entry = ttk.Entry(framebruteforce, textvariable=ToHash)
		ToHash_entry.pack()

		def HashThishandler():
			i= list_algo.curselection()
			HashedPass = HashedPassword_Attack.HashThis(ToHash.get(),str(list_algo.get(i)))
			HashedPass_label = Text(framebruteforce, height=1, borderwidth=0)
			HashedPass_label.insert(1.0, HashedPass)
			HashedPass_label.pack()
			HashedPass_label.configure(state="disabled")

		StartHash = ttk.Button(framebruteforce, text="Hash", command=HashThishandler)
		StartHash.pack()
	#TODO add have I been pawned, Dico, Wifi, hasher


class PageFive(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		#dos_frame = ttk.Frame(self, width=10000, height=100000,)
		#dos_frame.pack(side ="top",padx=30, pady=30, anchor="w")

		framebruteforceDico = LabelFrame(self, text = "Bruteforce hash (* are mandatory, others are optionnal)")
		framebruteforceDico.place(x=30,y=30,height=610,width=870)
#Base
		PasswordHash = StringVar()


#Hash
		PasswordHash_label = ttk.Label(framebruteforceDico, text="Hash cible* :")
		PasswordHash_label.pack()


		PasswordHash_entry = ttk.Entry(framebruteforceDico, textvariable=PasswordHash)
		PasswordHash_entry.pack(fill=X)
		PasswordHash_entry.focus()


#Hash Algorithm
		Label_choose_algo = Label(framebruteforceDico, text = "Select an algorythm*")
		Label_choose_algo.pack()

		Algorithms_choices = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s','sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128','shake_256']
		Algo = StringVar(value=Algorithms_choices)
		list_algo = Listbox(framebruteforceDico, listvariable=Algo, selectmode=SINGLE, exportselection=False)
		list_algo.pack()

		Label_choose_dico = Label(framebruteforceDico, text = "Select a dictionnary or open a file")
		Label_choose_dico.pack()

		dictionary_choices = ["2020-200_most_used_passwords", "default-passwords", "NordVPN"]
		choicesvar = StringVar(value=dictionary_choices)
		l_dico = Listbox(framebruteforceDico, listvariable=choicesvar, exportselection=False)
		l_dico.pack()
		global file_path

		def open_file():
			global file_path
			file_path = tkinter.filedialog.askopenfilename()
				

		button_add_dico = Button(framebruteforceDico,text="Open File", command=open_file)
		button_add_dico.pack()

		def HashedDico():
			j= l_dico.curselection()
			if not "file_path" in locals() or l_dico.get(j) != file_path[13:len(file_path)-4]:
				file_path=l_dico.get(j)
				file_path="Dictionaries/"+file_path+".txt"
				print("heu")	
			i= list_algo.curselection()
			HashedPassword_Attack.Dictionary_Hash(PasswordHash.get(), file_path, str(list_algo.get(i)))

		button_see = Button(framebruteforceDico,text="test", command=HashedDico)
		button_see.pack()


class MainMenu:
	def __init__(self, master):
		global controller
		menubar = Menu(master)
		filemenu = Menu(menubar, tearoff=0)
		filemenu.add_command(label="Exit", command=master.quit)
		menubar.add_cascade(label="File", menu=filemenu)
		menubar.add_command(label="StartPage", command=lambda:controller.show_frame(StartPage))
		master.config(menu=menubar)


app = App()
app.mainloop()