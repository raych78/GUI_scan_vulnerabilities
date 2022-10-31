from cmath import log
from sqlite3 import Row
from tkinter import *
from tkinter.tix import ROW

from xss_scanner import scan_xss


root = Tk()

root.title('Scanner vulnerability')
icone = PhotoImage(file='/home/kali/GUI_scanner/MrRobot.gif')

root.iconphoto(True,icone)

inputUrl = Entry(root,width=50)
inputUrl.pack()

labelTitle  = Label(root,text="Scanne les vulnérabilités de ton site !")
frameXSS = LabelFrame(root, text = "Analyse des injections xss")
frameXSS.place(x=30,y=30,height=250,width=500)

#blabal

frameSQL = LabelFrame(root, text = "Analyse des injections sql")
frameSQL.place(x=1100,y=30,height=250,width=500)



labelXSS = Label(frameXSS, text = "les resultats des failles xss apparaissent ici...")
labelXSS.pack()

def onClick():
    labelStartSCan = Label(root, text="Lancement du scan  en cours... ")
    labelStartSCan.pack()
    if scan_xss(inputUrl.get()):
        labelXSS.config(text = "Faille XSS trouvé !" + "\n" + "Risque elevé" +"\n" + "Attaque utilisé : "+ "<Script>alert('hi')</script>")
    else : 
        labelXSS.config(text = "Faille XSS non trouvé !")



    




button = Button(root, text = "Lancer le scan !", command=onClick, bg = "red" , fg = "white")
button.pack()


root.mainloop()

