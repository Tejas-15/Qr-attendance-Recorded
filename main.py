from tkinter import *
import qrcode
import sqlite3
import time
import random
import cv2 
import pyzbar.pyzbar as pyzbar
import numpy
import tkinter.messagebox as messagebox

# object of TK()
root= Tk()
root.title("Attendance Detector")
root.geometry("1920x1080")

#icon

p1 = PhotoImage(file = 'logo.png')
root.iconphoto(True, p1)


#******************************************* raise funtion logic *******************************************************

def raise_frame(frame):
	frame.tkraise()

Main_frame = LabelFrame(root, text = "HOME",fg="White",bg="black")
Register_frame = LabelFrame(root, text = "HOME",fg="White",bg="black")


for frame in (Main_frame,Register_frame):
	frame.grid(row=0, column=0, sticky='news')

date = time.strftime("%b%d")

random = random.randint(1,99)
# print(random)
id_no = str(date)+"_"+str(random)
# print(id_no)

def gentrate_id():
	My_canvas2.itemconfig(id_take,text = id_no)

def insert_db():
	conn = sqlite3.connect('Employee_data.db')
	c = conn.cursor()
	c.execute("INSERT INTO User_data (Idno,first_name,user_name,email_id,department) VALUES (?,?,?,?,?)",[id_no,Entry_reg_name.get(),Entry_reg_u_name.get(),Entry_reg_email.get(),Entry_reg_department.get()])
	conn.commit()

def scan():	
	go = True
	cap= cv2.VideoCapture(0)
	while go:
		_,frame = cap.read()
		decodedObjects = pyzbar.decode(frame)
		for obj in decodedObjects:
			k = ((obj.data).decode("utf-8"))
			cv2.destroyWindow("frame")
			cap.release()
			go = False
			break   
		cv2.imshow("QrCode",frame)
		key = cv2.waitKey(1)
		root.withdraw()

	x = k.split()
	global p
	p=(x[0])

scan()

#******************************************* Check logic ****************************************************************
def Check():#sign in logic
	scan()
	conn = sqlite3.connect('Employee_data.db')
	c = conn.cursor()
	
	c.execute("SELECT * FROM User_data WHERE Idno =?",[p])
	f=c.fetchall()
	global fetchid
	fetchid=(f[0][0])
	global fetchname
	fetchname=(f[0][1])
	print(fetchname)
	global fetchuname
	fetchuname=(f[0][2])
	print(fetchuname)
	global fetchemailid
	fetchemailid=(f[0][3])
	print(fetchemailid)
	global fetchdep
	fetchdep=(f[0][4])
	print(fetchdep)
	# print(fetchid)

	if fetchid == p :
		messagebox.showinfo("Scan Succesfully", "Your Attendance Has Been Mark Present")
	else :
		messagebox.showwarning("Error", "Some Error in QrCode")		

Check()

# #****************************************Update Records if Present****************************************************
def Present_update():
	conn = sqlite3.connect('Employee_data.db')
	c = conn.cursor()

	c.execute("INSERT INTO Present_table VALUES (?,?,?,?,?)", [fetchid,fetchname,fetchuname,fetchemailid,fetchdep])

	c.execute("SELECT rowid, * FROM Present_table")

	conn.commit()
	conn.close()
Present_update()	


#********************************************* Home PAGE ***************************************************************

# Define image

bg = PhotoImage(file="background.png")

# Create a canvas home frame
My_canvas = Canvas(Main_frame, width=1920, height=1080)
My_canvas.pack(fill="both", expand=True)

# Set image in canvas
My_canvas.create_image(0,0, image=bg ,anchor="nw")

scan=Button(Main_frame,text="SCAN",fg="white" ,bg="black",command=scan)
scan.place(x=760 ,y=470,height=40,width=100)


Confirm=Button(Main_frame,text="New Joinee",fg="white" ,bg="green",command=lambda:[raise_frame(Register_frame),gentrate_id()])
Confirm.place(x=900 ,y=470,height=40,width=100)

root.deiconify()


#********************************************* Register PAGE ***************************************************************


# Define image
bg1 = PhotoImage(file="background.png")
white = PhotoImage (file="white.png")

# Create a canvas home frame
My_canvas2 = Canvas(Register_frame, width=1920, height=1080)
My_canvas2.pack(fill="both", expand=True)

# Set image in canvas
My_canvas2.create_image(0,0, image=bg1 ,anchor="nw")
My_canvas2.create_image(950,440,image=white)

main_Label = My_canvas2.create_text(950,200,
				 text="Registion Page",
				 font=("Times", 35, "bold")
				 )

idno = My_canvas2.create_text(550,250, text="Id No. :",font=("Times", 20))

id_take=My_canvas2.create_text(650,250 ,text="id take",font=("Times", 20))

register_name = My_canvas2.create_text(840,290, text="Name : ", font=("Times", 20))
Entry_reg_name = Entry(Register_frame, width=30, borderwidth=3)
Entry_reg_name.place(x=900,y=285)

register_U_name = My_canvas2.create_text(815,340, text="User Name : ", font=("Times", 20))
Entry_reg_u_name = Entry(Register_frame, width=30, borderwidth=3)
Entry_reg_u_name.place(x=900,y=335)

register_email = My_canvas2.create_text(830,390, text="Email Id : ", font=("Times", 20))
Entry_reg_email = Entry(Register_frame, width=40, borderwidth=3)
Entry_reg_email.place(x=900,y=385)

register_email = My_canvas2.create_text(810,440, text="Department : ", font=("Times", 20))
Entry_reg_department = Entry(Register_frame, width=30, borderwidth=3)
Entry_reg_department.place(x=900,y=430)

submit=Button(Register_frame,text="Register",fg="White" ,bg="green" ,font=("calibri",20,"bold"),command=insert_db)
submit.place(x=950,y=490,height=40,width=100) 

#which frame to show first 
raise_frame(Main_frame)

root.mainloop()