import sqlite3 as sql
import tkinter
from main import redirectt
from time import sleep
from tkinter import messagebox  

con = sql.connect("database.db")
cur = con.cursor()
statement = "SELECT * FROM USERS"
cur.execute(statement)
lst = cur.fetchall()

#variables
root=None
userbox=None
passbox=None
topframe=None
bottomframe=None
frame3=None
login=None

def GET():
	global userbox,passbox,error
	user_name=userbox.get()
	user_pwd=passbox.get()

	flag=False
	for i in lst:
		if (user_name == i[0] and user_pwd == str(i[1])):
			root.destroy()
			redirectt()
			flag = True
			exit(0)

	if len(user_name) == 0 or len(user_pwd) == 0:
		messagebox.showinfo("Error","Field cannot be empty.")  
		flag = True
	if flag==False:
		messagebox.showinfo("Error","Wrong Id / Password \n TRY AGAIN.") 

def Entry():
	global userbox,passbox,login,topframe,bottomframe,image_1
	global root
	root = tkinter.Tk()
	topframe = tkinter.Frame(root)
	topframe.pack()
	bottomframe=tkinter.Frame(root)
	bottomframe.pack()
	heading = tkinter.Label(topframe, text="WELCOME TO NU HMS",bg='white',fg='orange',font='Times 20 bold italic',padx=10,pady=10)
	username=tkinter.Label(topframe,text="USERNAME",font="arial 12",padx=10,pady=10)
	userbox = tkinter.Entry(topframe,font="12")
	password=tkinter.Label(bottomframe,text="PASSWORD",font="arial 12",padx=10,pady=10)
	passbox = tkinter.Entry(bottomframe,show="*",font="12")
	login = tkinter.Button(bottomframe, text="LOGIN", command=GET,font="arial 14 bold",padx=10,pady=10)
	heading.pack()
	username.pack()
	userbox.pack()
	password.pack()
	passbox.pack()
	login.pack(pady=20)
	root.title("DATABASE LOGIN")
	root.resizable(False, False)
	hs = root.winfo_screenheight()
	ws = root.winfo_screenwidth()
	x = (ws/2) - 250
	y = (hs/2) - 250
	root.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
	root.geometry('500x500')
	root.mainloop()

Entry()
