from tkinter import *
from tkinter import ttk
import threading 
import queue

import Source.Scripts.HashedPassword_Attack as HashedPassword_Attack


class BruteforceHash(Frame):
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
		PasswordHash_label = ttk.Label(framebruteforce, text="Targeted Hash* :")
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

		ToHash_label = ttk.Label(framebruteforce, text="\n \n Want to hash something? Fill in text and select the hash method up there")
		ToHash_label.pack()
		

		ToHash_entry = ttk.Entry(framebruteforce, textvariable=ToHash)
		ToHash_entry.pack()
		HashedPass_label = Text(framebruteforce, height=2, borderwidth=0)

		def HashThishandler():
			i= list_algo.curselection()
			HashedPass = HashedPassword_Attack.HashThis(ToHash.get(),str(list_algo.get(i)))

			HashedPass_label.configure(state="normal")
			HashedPass_label.delete(1.0, END)
			HashedPass_label.insert(1.0, HashedPass)
			HashedPass_label.configure(state="disabled")
			HashedPass_label.pack()


		StartHash = ttk.Button(framebruteforce, text="Hash", command=HashThishandler)
		StartHash.pack()
	