from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Separator
import tkinter.messagebox
import sqlite3
import re

#connecting to database
conn = sqlite3.connect('database.db')
c = conn.cursor()
ids = []

class Application:

	def __init__(self, window):

		self.window = window
		self.v = IntVar()
		c.execute('SELECT * FROM APPOINTMENTS')
		self.alldata = c.fetchall()

		# creating the frames in the window

		self.main = Frame(window, width=500, height=500, bg='wheat2')
		self.showdetailsframe = Frame(self.window)
		self.updateframe = Frame(self.window)
		self.deleteframe = Frame(self.window)

	# start page (page diaplayed after login)
	def startPage(self):
		self.heading = Label(
			self.main,
			text='NU Appointments',
			font='Centaur 20 bold',
			fg='black',
			bg='misty rose',
			relief=SUNKEN,
			)
		self.heading.place(x=12, y=20)

		#name
		self.name = Label(self.main, text='Patients Name: ', font='arial 12 bold', bg='lightblue', padx=20)
		self.name.place(x=0, y=110)

		# age
		self.age = Label(self.main, text='Age: ', font='arial 12 bold', bg='lightblue', padx=20)
		self.age.place(x=0, y=155)

		# gender
		Label(self.main, text='Gender: ', font='arial 12 bold', bg='lightblue', padx=20).place(x=0, y=210)
		a = Radiobutton( self.main, text='Male', padx=20, font='ariel 10 bold', variable=self.v, value=1).place(x=190, y=210)
		b = Radiobutton( self.main, text='Female', padx=20, font='ariel 10 bold', variable=self.v, value=2).place(x=280, y=210)

		# location
		self.time = Label(self.main, text='Location: ', font='arial 12 bold', bg='lightblue', padx=20)
		self.time.place(x=0, y=255)

		# phone
		self.phone = Label(self.main, text='Contact Number: ', font='arial 12 bold', bg='lightblue', padx=20)
		self.phone.place(x=0, y=300)

		# text box for lables
		self.name_ent = Entry(self.main, width=30)
		self.name_ent.place(x=190, y=115)

		self.age_ent = Entry(self.main, width=30)
		self.age_ent.place(x=190, y=160)

		self.location_ent = Entry(self.main, width=30)
		self.location_ent.place(x=190, y=258)

		self.phone_ent = Entry(self.main, width=30)
		self.phone_ent.place(x=190, y=305)

		# button to perform a command
		self.submit = Button( self.main, text='Add Appointment', font='aried 12 bold', width=15, height=2, bg='lightgreen', command=self.add_appointment)
		self.submit.place(x=140, y=370)

		sql2 = 'SELECT CID FROM APPOINTMENTS '
		self.result = c.execute(sql2)

		ids=[]

		for self.row in self.result:
			self.id = self.row[0]
			ids.append(self.id)

		# ordering the ids
		self.new = sorted(ids)
		self.final_id = self.new[len(ids) - 1]

		#  display the logs in our frame
		self.logs = Label(self.main, text='Total\n Appointments: ', font='arial 10 bold', fg='black', bg='lightblue')
		self.logs.place(x=340, y=360)
		self.logs = Label(self.main, text=' ' + str(len(ids)), width=8, height=1, relief=SUNKEN).place(x=360, y=400)

		self.main.pack()

	# function to add a new appointment
	def add_appointment(self):

		self.val1 = self.name_ent.get()
		self.val2 = self.age_ent.get()

		if self.v.get() == 1:
			self.val3 = 'Male'
		elif self.v.get() == 2:
			self.val3 = 'Female'
		else:
			self.val3 = 'Not Specified'

		self.val4 = self.location_ent.get()
		self.val5 = self.phone_ent.get()

		if re.match(r"^[A-za-z]+$", str(self.val1)) is None :
			tkinter.messagebox.showinfo('Warning', 'Name not in correct format')
		elif re.match(r"^\d+$", str(self.val2)) is None :
			tkinter.messagebox.showinfo('Warning', 'Age not in correct format')
		elif re.match(r"^[789]{1}\d{9}$", str(self.val5)) is None :
			tkinter.messagebox.showinfo('Warning', 'Mobile no not in correct format')
		elif self.val1 == '' or self.val2 == '' or self.val3 == '' or self.val4 == '' or self.val5 == '':
			tkinter.messagebox.showinfo('Warning', 'Please Fill Up All Boxes')
		else:
			sql = "INSERT INTO 'appointments' (name, age, gender, location, phone) VALUES(?, ?, ?, ?, ? )"
			c.execute(sql, (self.val1, self.val2, self.val3, self.val4, self.val5))
			conn.commit()
			tkinter.messagebox.showinfo('Success', '\n Appointment for ' + str(self.val1) + ' has been created')

		self.main.destroy()
		self.__init__(self.window)
		self.startPage()

	# to return to the start page
	def homee(self):
		self.main.destroy()
		self.showdetailsframe.destroy()
		self.updateframe.destroy()
		self.deleteframe.destroy()
		self.__init__(self.window)
		self.startPage()

	#function to display details of all the appointments
	def showdetails(self):
		self.main.destroy()
		self.showdetailsframe.destroy()
		self.updateframe.destroy()
		self.deleteframe.destroy()
		self.__init__(self.window)
		count1 = 0
		count2 = 0

		clmnname = [
			'App. no',
			'Name',
			'Age',
			'Gender',
			'Location',
			'Contact no.',
			]
		for i in range(len(clmnname)):
			Label(self.showdetailsframe, text=clmnname[i], font='ariel 12 bold').grid(row=0, column=i * 2,padx=5)
			Separator(self.showdetailsframe, orient=VERTICAL).grid(row=0, column=i * 2 + 1, sticky='ns')
		for i in range(len(self.alldata)):
			for j in range(6):
				Label(self.showdetailsframe, text=self.alldata[i][j], font='ariel 10').grid(row=count1 + 2, column=count2 * 2,padx=5)
				Separator(self.showdetailsframe,orient=VERTICAL).grid(row=count1 + 2, column=count2 * 2 + 1, sticky='ns')
				count2 += 1
			count2 = 0
			count1 += 1
		self.showdetailsframe.pack()

	# update a cuurent appointment
	def updatee(self):
		self.main.destroy()
		self.showdetailsframe.destroy()
		self.updateframe.destroy()
		self.deleteframe.destroy()
		self.__init__(self.window)

		self.id = Label(self.updateframe, text='Search Appoinment Number To Update: ', font='arial 12 bold', fg='red')
		self.id.place(x=0, y=12)
		self.idnet = Entry(self.updateframe, width=10)
		self.idnet.place(x=320, y=18)
		self.search = Button(self.updateframe, text='Search', font='aried 12 bold', width=10, height=1, bg='lightgreen', command=self.update1)
		self.search.place(x=160, y=50)
		self.updateframe.pack(fill='both', expand=True)

	def update1(self):
		self.input = self.idnet.get()

		# execute sql

		sql = 'SELECT * FROM appointments WHERE CID LIKE ?'
		self.res = c.execute(sql, (self.input,))

		# if entry is not present in database
		if len(self.res.fetchall())==0 :
			tkinter.messagebox.showinfo('Error', 'No Entry Found')
		else:
			self.res = c.execute(sql, (self.input,))
			for self.row in self.res:
				self.name1 = self.row[1]
				self.age = self.row[2]
				self.gender = self.row[3]
				self.location = self.row[4]
				self.phone = self.row[5]

			# creating the update form

			self.uname = Label(self.updateframe, text="Patient's Name: ", font='arial 14 bold')
			self.uname.place(x=0, y=140)

			self.uage = Label(self.updateframe, text='Age: ',   font='arial 14 bold')
			self.uage.place(x=0, y=180)

			self.ugender = Label(self.updateframe, text='Gender: ', font='arial 14 bold')
			self.ugender.place(x=0, y=220)

			self.ulocation = Label(self.updateframe, text='Location: ', font='arial 14 bold')
			self.ulocation.place(x=0, y=260)

			self.uphone = Label(self.updateframe, text='Phone Number: ', font='arial 14 bold')
			self.uphone.place(x=0, y=300)

			# entrys
			self.ent1 = Entry(self.updateframe, width=30)
			self.ent1.place(x=180, y=140)
			self.ent1.insert(0, str(self.name1))

			self.ent2 = Entry(self.updateframe, width=30)
			self.ent2.place(x=180, y=180)
			self.ent2.insert(END, str(self.age))

			self.ent3 = Entry(self.updateframe, width=30)
			self.ent3.place(x=180, y=220)
			self.ent3.insert(END, str(self.gender))

			self.ent4 = Entry(self.updateframe, width=30)
			self.ent4.place(x=180, y=260)
			self.ent4.insert(END, str(self.location))

			self.ent5 = Entry(self.updateframe, width=30)
			self.ent5.place(x=180, y=300)
			self.ent5.insert(END, str(self.phone))

			# buttons for update and delete
			self.update = Button(self.updateframe, text='Update', font='aried 12 bold', width=10, height=1, bg='lightgreen', command=self.update2)
			self.update.place(x=25, y=340)
			self.updateframe.pack()

	def update2(self):

		# declaring the variables to update
		self.var1 = self.ent1.get()
		self.var2 = self.ent2.get()
		self.var3 = self.ent3.get()
		self.var4 = self.ent4.get()
		self.var5 = self.ent5.get()

		query = 'UPDATE appointments SET name=?, age=?, gender=?, location=?, phone=? WHERE CID LIKE ?'
		c.execute(query, (self.var1, self.var2, self.var3, self.var4, self.var5, self.idnet.get()))
		conn.commit()
		tkinter.messagebox.showinfo('Updated', 'Successfully Updated.')
		self.updateframe.destroy()
		self.__init__(self.window)
		self.updatee()
		self.updateframe.pack()

	# funtion to delete an appointment
	def deletee(self):

		self.main.destroy()
		self.showdetailsframe.destroy()
		self.updateframe.destroy()
		self.deleteframe.destroy()
		self.__init__(self.window)

		self.id = Label(self.deleteframe, text='Search Appoinment Number To Delete: ', font='arial 12 bold', fg='red')
		self.id.place(x=0, y=12)
		self.idnet = Entry(self.deleteframe, width=10)
		self.idnet.place(x=320, y=18)
		self.search = Button( self.deleteframe, text='Search', font='aried 12 bold', width=10, height=1, bg='lightgreen', command=self.delete1)
		self.search.place(x=160, y=50)
		self.deleteframe.pack(fill='both', expand=True)

	def delete1(self):
		self.input = self.idnet.get()

		# execute sql

		sql = 'SELECT * FROM appointments WHERE CID LIKE ?'
		self.res = c.execute(sql, (self.input, ))

		#if no entry found in database
		if len(self.res.fetchall())==0 :
			tkinter.messagebox.showinfo('Error', 'No Entry Found')

		else :
			self.res = c.execute(sql, (self.input, ))
			for self.row in self.res:
				self.name1 = self.row[1]
				self.age = self.row[2]
				self.gender = self.row[3]
				self.location = self.row[4]
				self.phone = self.row[5]

			# creating the update form

			self.uname = Label(self.deleteframe, text="Patient's Name: ", font='arial 14 bold')
			self.uname.place(x=0, y=140)

			self.uage = Label(self.deleteframe, text='Age: ', font='arial 14 bold')
			self.uage.place(x=0, y=180)

			self.ugender = Label(self.deleteframe, text='Gender: ', font='arial 14 bold')
			self.ugender.place(x=0, y=220)

			self.ulocation = Label(self.deleteframe, text='Location: ', font='arial 14 bold')
			self.ulocation.place(x=0, y=260)

			self.uphone = Label(self.deleteframe, text='Phone Number: ', font='arial 14 bold')
			self.uphone.place(x=0, y=300)

			# entrys
			self.ent1 = Label(self.deleteframe, text=str(self.name1),width=30)
			self.ent1.place(x=180, y=140)

			# self.ent1 = Text(str(self.name1), state='disabled', width=44, height=5)

			self.ent2 = Label(self.deleteframe, text=str(self.age), width=30)
			self.ent2.place(x=180, y=180)

			self.ent3 = Label(self.deleteframe,text=str(self.gender), width=30)
			self.ent3.place(x=180, y=220)

			self.ent4 = Label(self.deleteframe,text=str(self.location), width=30)
			self.ent4.place(x=180, y=260)

			self.ent5 = Label(self.deleteframe,text=str(self.phone), width=30)
			self.ent5.place(x=180, y=300)

			# buttons for update and delete

			self.update = Button(
				self.deleteframe,
				text='Delete',
				font='aried 12 bold',
				width=10,
				height=1,
				bg='lightgreen',
				command=self.delete2,
			)
			self.update.place(x=25, y=340)
			self.deleteframe.pack()

	def delete2(self):
		sql2 = 'DELETE FROM appointments WHERE CID LIKE ?'
		c.execute(sql2, (self.idnet.get(), ))
		conn.commit()
		tkinter.messagebox.showinfo('Success', 'Deleted Successfully')
		self.ent1.destroy()
		self.ent2.destroy()
		self.ent3.destroy()
		self.ent4.destroy()
		self.ent5.destroy()
		self.deleteframe.destroy()
		self.__init__(self.window)
		self.deletee()
		self.deleteframe.pack()

# Top menubar for navigation
def menubar():
	main_menu = Menu()
	window.config(menu=main_menu)
	file_menu = Menu(main_menu, tearoff=False)
	main_menu.add_cascade(label='Menu', menu=file_menu)
	file_menu.add_command(label='Home', command=b.homee)
	file_menu.add_command(label='Show details', command=b.showdetails)
	file_menu.add_command(label='Update', command=b.updatee)
	file_menu.add_command(label='Delete', command=b.deletee)
	file_menu.add_separator()
	file_menu.add_command(label='Exit', command=window.quit)


# main page redirected from login page
def redirectt():
	global window, b
	window = tkinter.Tk()
	b = Application(window)
	b.startPage()
	window.config(menu=menubar())
	window.title('Hospital Management System')
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	x = (ws/2) - 250
	y = (hs/2) - 250
	window.geometry('%dx%d+%d+%d' % (ws, hs, x, y))
	window.geometry('500x500')
	window.resizable(False, False)

	window.mainloop()
