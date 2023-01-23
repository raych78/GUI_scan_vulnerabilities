from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import queue
from os import listdir
from os.path import isfile, join

import Source.Scripts.HashedPassword_Attack as HashedPassword_Attack

class DicoHash(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self, parent)
		self.configure(background='black')

		#dos_frame = ttk.Frame(self, width=10000, height=100000,)
		#dos_frame.pack(side ="top",padx=30, pady=30, anchor="w")

		framebruteforceDico = LabelFrame(self, text = "Dictionary hash")
		framebruteforceDico.place(x=30,y=30,height=610,width=870)
#Base
		PasswordHash = StringVar()
		HaveIbeenPawned = StringVar()


#Hash
		PasswordHash_label = ttk.Label(framebruteforceDico, text="Targeted Hash :")
		PasswordHash_label.grid()


		PasswordHash_entry = ttk.Entry(framebruteforceDico, textvariable=PasswordHash)
		PasswordHash_entry.grid()
		PasswordHash_entry.focus()


#Hash Algorithm
		Label_choose_algo = Label(framebruteforceDico, text = "Select an algorythm")
		Label_choose_algo.grid()

		Algorithms_choices = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s','sha3_224', 'sha3_256', 'sha3_384', 'sha3_512', 'shake_128','shake_256']
		Algo = StringVar(value=Algorithms_choices)
		list_algo = Listbox(framebruteforceDico, listvariable=Algo, selectmode=SINGLE, exportselection=False)
		list_algo.grid(column=0)

		Label_choose_dico = Label(framebruteforceDico, text = "Select a dictionnary or open a file")
		Label_choose_dico.grid(column=1, row=2)

		Files = [f for f in listdir("Dictionaries/") if isfile(join("Dictionaries/", f))]
		Files.append("Custom...")
		dictionary_choices = Files
		#dictionary_choices = ["2020-200_most_used_passwords", "default-passwords", "NordVPN", "Custom..."]
		choicesvar = StringVar(value=dictionary_choices)
		l_dico = Listbox(framebruteforceDico, listvariable=choicesvar, exportselection=False)
		l_dico.grid(column=1, row=3)
		def open_file():
			global file_path
			file_path = filedialog.askopenfilename()

		return_queue_Dico = queue.Queue()	

		global LabelOutDico

		LabelOutDico = Label(framebruteforceDico, text="Waiting for orders")
		LabelOutDico.grid()

		button_add_dico = Button(framebruteforceDico,text="Open File", command=open_file)
		button_add_dico.grid(column=1)

		def HashedDico():
			global file_path
			j= l_dico.curselection()
			if not "file_path" in locals() or l_dico.get(j) != file_path[13:len(file_path)]:
				if l_dico.get(j) != "Custom...":
					file_path=l_dico.get(j)
					file_path="Dictionaries/"+file_path
			i= list_algo.curselection()
			HashedPassword_Attack.Dictionary_Hash(PasswordHash.get(), file_path, return_queue_Dico, str(list_algo.get(i)))
			global LabelOutDico
			while True:
				try:
					textOut = return_queue_Dico.get(timeout=5)
					LabelOutDico.configure(text=textOut)
					break
				except queue.Empty:
					pass



		button_Find = Button(framebruteforceDico,text="Search hash", command=HashedDico)
		button_Find.grid(row=5)


		HaveIbeenPawned_label = ttk.Label(framebruteforceDico, text="\n Check if your password is in the dictionary :")
		HaveIbeenPawned_label.grid()


		HaveIbeenPawned_entry = ttk.Entry(framebruteforceDico, textvariable=HaveIbeenPawned)
		HaveIbeenPawned_entry.grid()
		HaveIbeenPawned_entry.focus()

		def TestPawned():
			global file_path
			j= l_dico.curselection()
			if not "file_path" in locals() or l_dico.get(j) != file_path[13:len(file_path)]:
				if l_dico.get(j) != "Custom...":
					file_path=l_dico.get(j)
					file_path="Dictionaries/"+file_path
			
			with open(file_path,'r') as f:
				for p in f.readlines():
					p = p[:len(p)-1]
					if p == HaveIbeenPawned.get():
						Pawned_label.configure(text="Password in "+file_path, fg='red')
						return None
				Pawned_label.configure(text="Password not in "+file_path, fg='green')	




		button_Pawned = Button(framebruteforceDico,text="Pawned ?", command=TestPawned)
		button_Pawned.grid()

		Pawned_label = Label(framebruteforceDico)
		Pawned_label.grid()
