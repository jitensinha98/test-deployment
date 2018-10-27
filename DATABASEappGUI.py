#importing necessary packages
import tkinter as tk
from tkinter import messagebox
import sqlite3

#connecting the database with the localhost server
conn=sqlite3.connect('EMPLOYEE.db')

#creating cursor to execute SQL commands
c=conn.cursor()

#main window class
class Main_window:
	def __init__(self, master):
		self.master = master
		self.bottom_frame = tk.Frame(self.master)
		self.middle_frame=tk.Frame(self.master)
		self.middlelast_frame=tk.Frame(self.master)
		self.last_frame=tk.Frame(self.master)
		self.master.title("IT SECTOR DATABASE MANAGEMENT SOFTWARE")
		self.top_frame=tk.Frame(self.master)
		self.master.geometry("520x430")
		self.message_scrollbar=tk.Scrollbar(self.top_frame)
		main_heading="{:^100}".format("DATABASE ENTRY LIST")
		self.labelheading=tk.Label(self.top_frame,text=main_heading,fg='white',bg='grey')
		self.labelheading.pack(side=tk.TOP)
		self.readformalbutton=tk.Button(self.middlelast_frame,text="DISPLAY FORMAL DETAILS",width=28,fg='white',bg='grey',command=self.read_formal_entry)
		self.readpersonalbutton=tk.Button(self.middlelast_frame,text="DISPLAY PERSONAL DETAILS",width=28,fg='white',bg='grey',command=self.read_personal_entry)
		self.createbutton = tk.Button(self.last_frame,text="CREATE DATABASE",width=28,fg='white',bg='grey',command=self.create_table)
		self.exitbutton = tk.Button(self.last_frame,text="EXIT",width=28,fg='white',bg='grey',command=self.close_windows)
		self.readbutton = tk.Button(self.bottom_frame, text = 'READ & SAVE DATABASE', width = 28,fg='white',bg='grey',command=self.read_all)
		self.readbutton.pack(side=tk.LEFT)
		self.updatebutton = tk.Button(self.bottom_frame, text = 'UPDATE EMPLOYEE DATABASE', width = 28,fg='white',bg='grey',command= self.updatedb_window)
		self.readformalbutton.pack(side=tk.LEFT)
		self.readpersonalbutton.pack(side=tk.LEFT)
		self.updatebutton.pack(side=tk.LEFT)
		self.addbutton=tk.Button(self.middle_frame,text='ADD NEW EMPLOYEE DETAILS',width = 28,fg='white',bg='grey',command = self.adddb_window)
		self.addbutton.pack(side=tk.LEFT)
		self.deletebutton = tk.Button(self.middle_frame, text = 'DELETE EMPLOYEE DETAILS', width = 28,fg='white',bg='grey',command=self.deletedb_window)
		self.deletebutton.pack()
		self.data_list = tk.Listbox(self.top_frame,width=62,height=20)
		self.data_list.pack(side=tk.LEFT,fill=tk.Y)
		self.message_scrollbar.pack(side=tk.LEFT,fill=tk.Y)
		self.createbutton.pack(side=tk.LEFT)
		self.exitbutton.pack()
		self.top_frame.pack(side=tk.TOP)
		self.middle_frame.pack(side=tk.TOP)
		self.middlelast_frame.pack(side=tk.TOP)
		self.bottom_frame.pack(side=tk.TOP)
		self.last_frame.pack()
	
	#calling classes for respective button events
	def create_table(self):
		#creating table named employee in database EMPLOYEE
		c.execute('CREATE TABLE IF NOT EXISTS employee_formal_details(Id TEXT,Name TEXT,Designation TEXT,Department TEXT,Salary TEXT)')
		c.execute('CREATE TABLE IF NOT EXISTS employee_personal_details(Id TEXT,Name TEXT,Gender TEXT,Age TEXT,Contact_no TEXT,Address TEXT)')
		self.msg=messagebox.showinfo("CONFIRMATION","DATABASE CREATED SUCCESSFULLY.")
	def adddb_window(self):
        	self.newWindow = tk.Toplevel(self.master)
        	self.app = Add_window(self.newWindow)
	def deletedb_window(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = Delete_window(self.newWindow)
	def updatedb_window(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = Update_window(self.newWindow)
	def read_formal_entry(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = Read_formal_window(self.newWindow)
	def read_personal_entry(self):
		self.newWindow = tk.Toplevel(self.master)
		self.app = Read_personal_window(self.newWindow)
	def read_all(self):
		self.data_list.delete(0,tk.END)
		c.execute("SELECT * FROM employee_formal_details")
		
		#string formatting parameters to be displayed
		intro="{:^10}{:^25}{:^25}{:^15}{:^25}".format("ID","NAME","DESIGNATION","DEPARTMENT","SALARY")
		design="-"*130

		self.data_list.insert(tk.END," ")
		self.data_list.insert(tk.END,"                        ****************FORMAL DETAILS******************")
		self.data_list.insert(tk.END," ")
		self.data_list.insert(tk.END,intro)
		self.data_list.insert(tk.END,design)
	
		#creating a .txt file named EMPLOYEE-DATABASE
		file=open("EMPLOYEE-FORMAL-TABLE.txt","w+")
		#writing to that file
		file.write(intro+"\n")
		file.write(design+"\n")

		for row in c.fetchall():
			show="{:^10}{:^25}{:^32}{:^15}{:^25}".format(row[0],row[1],row[2],row[3],row[4])
			self.data_list.insert(tk.END,show)
			file.write(show+"\n")
		#closing file control
		file.close()
		c.execute("SELECT * FROM employee_personal_details")
	
		#string formatting parameters to be displayed
		intro="{:^10}{:^25}{:^10}{:^10}{:^25}{:^15}".format("ID","NAME","GENDER","AGE","CONTACT","ADDRESS")
		design="-"*130
		self.data_list.insert(tk.END," ")
		self.data_list.insert(tk.END,"                        ****************PERSONAL DETAILS******************")
		self.data_list.insert(tk.END," ")
		self.data_list.insert(tk.END,intro)
		self.data_list.insert(tk.END,design)

		#creating a .txt file named EMPLOYEE-DATABASE
		file=open("EMPLOYEE-PERSONAL-TABLE.txt","w+")
		#writing to that file
		file.write(intro+"\n")
		file.write(design+"\n")

		for row in c.fetchall():
			show="{:^10}{:^25}{:^10}{:^10}{:^18}{:^22}".format(row[0],row[1],row[2],row[3],row[4],row[5])
			self.data_list.insert(tk.END,show)
			file.write(show+"\n")
		#closing file control
		file.close()


	def close_windows(self):
		#closing the cursor to stop executing commands
		c.close()
		#closing connection to the localhost server
		conn.close()

		self.master.destroy()
	
#add window class
class Add_window:
	def __init__(self, master):
		self.master = master
		
		#locks the old window when new window in open
		self.master.grab_set()

		self.master.title("ADD WIZARD")
		self.master.geometry("360x280")		
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")
		self.label_name=tk.Label(self.master,text="NAME :")
		self.label_id=tk.Label(self.master,text="ID :")
		self.label_designation=tk.Label(self.master,text="DESIGNATION :")
		self.label_salary=tk.Label(self.master,text="SALARY :")
		self.label_dept=tk.Label(self.master,text="DEPARTMENT :")
		self.label_age=tk.Label(self.master,text="AGE :")
		self.label_gender=tk.Label(self.master,text="GENDER :")
		self.label_contactno=tk.Label(self.master,text="CONTACT NO :")
		self.label_address=tk.Label(self.master,text="ADDRESS :")


		self.idEntry = tk.Entry(self.master, width=30)
		self.nameEntry = tk.Entry(self.master,width=30)
		self.salaryEntry = tk.Entry(self.master, width=30)
		self.deptEntry = tk.Entry(self.master, width=30)
		self.designationEntry = tk.Entry(self.master, width=30)
		self.ageEntry = Entry = tk.Entry(self.master, width=30)
		self.genderEntry = tk.Entry(self.master, width=30)
		self.contactnoEntry = tk.Entry(self.master, width=30)
		self.addressEntry = tk.Entry(self.master, width=30)


		self.Add_button=tk.Button(self.master,text="ADD",width=28,fg="white",bg="grey",command=self.data_entry)
		self.Exit_button=tk.Button(self.master,text="EXIT",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_2.grid(row=0)

		self.label_id.grid(row=1,sticky=tk.E)
		self.idEntry.grid(row=1,column=1)
	
		self.label_name.grid(row=2,sticky=tk.E)
		self.nameEntry.grid(row=2,column=1)
		
		self.label_designation.grid(row=3,sticky=tk.E)
		self.designationEntry.grid(row=3,column=1)

		self.label_dept.grid(row=4,sticky=tk.E)
		self.deptEntry.grid(row=4,column=1)
		
		self.label_salary.grid(row=5,sticky=tk.E)
		self.salaryEntry.grid(row=5,column=1)

		self.label_age.grid(row=6,sticky=tk.E)
		self.ageEntry.grid(row=6,column=1)

		self.label_gender.grid(row=7,sticky=tk.E)
		self.genderEntry.grid(row=7,column=1)

		self.label_contactno.grid(row=8,sticky=tk.E)
		self.contactnoEntry.grid(row=8,column=1)

		self.label_address.grid(row=9,sticky=tk.E)
		self.addressEntry.grid(row=9,column=1)
      
		self.blanklabel_1.grid(row=10,column=1)
		self.Add_button.grid(row=11,column=1)
		self.Exit_button.grid(row=12,column=1)
	
	def data_entry(self):
		id=self.idEntry.get()
		name=self.nameEntry.get()
		designation=self.designationEntry.get()
		department=self.deptEntry.get()
		salary=self.salaryEntry.get()
		gender=self.genderEntry.get()
		age=self.ageEntry.get()
		contactno=self.contactnoEntry.get()
		address=self.addressEntry.get()
		#add entries to the table in database after taking user input
		c.execute("INSERT INTO employee_formal_details(Id,Name,Designation,Department,Salary) VALUES(?,?,?,?,?)",(id,name,designation,department,salary))
		c.execute("INSERT INTO employee_personal_details(Id,Name,Gender,Age,Contact_no,Address) VALUES(?,?,?,?,?,?)",(id,name,gender,age,contactno,address))
		self.msg=messagebox.showinfo("CONFIRMATION","ENTRY ADDED SUCCESSFULLY.")
		self.idEntry.delete(0,'end')
		self.nameEntry.delete(0,'end')
		self.designationEntry.delete(0,'end')
		self.deptEntry.delete(0,'end')
		self.salaryEntry.delete(0,'end')
		self.ageEntry.delete(0,'end')
		self.genderEntry.delete(0,'end')
		self.contactnoEntry.delete(0,'end')
		self.addressEntry.delete(0,'end')
		conn.commit()

	def close_windows(self):
		
		#releases the control of old window 
		self.master.grab_release()
		#destroys window
		self.master.destroy()

#delete window class
class Delete_window:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("DELETE WIZARD")
		self.master.geometry("310x180")		
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")
		self.label_name=tk.Label(self.master,text="NAME :")
		self.label_id=tk.Label(self.master,text="ID :")
		self.idEntry = tk.Entry(self.master, width=30)
		self.nameEntry = tk.Entry(self.master,width=30)

		self.Delete_button=tk.Button(self.master,text="DELETE ENTRY",width=28,fg="white",bg="grey",command=self.clear_entry)
		self.Exit_button=tk.Button(self.master,text="EXIT",width=28,fg="white",bg="grey",command=self.close_windows)
		self.Delete_all=tk.Button(self.master,text="CLEAR DATABASE",width=28,fg="white",bg="grey",command=self.clear_database)
		
		self.blanklabel_2.grid(row=0)

		self.label_id.grid(row=1,sticky=tk.E)
		self.idEntry.grid(row=1,column=1)
	
		self.label_name.grid(row=2,sticky=tk.E)
		self.nameEntry.grid(row=2,column=1)
		
		self.blanklabel_1.grid(row=6,column=1)
		self.Delete_button.grid(row=7,column=1)
		self.Delete_all.grid(row=8,column=1)
		self.Exit_button.grid(row=9,column=1)

	def clear_database(self):
		#clears entries from the entire table
		c.execute('DELETE FROM employee_formal_details');
		c.execute('DELETE FROM employee_personal_details');
		conn.commit()
		self.msg=messagebox.showinfo("CONFIRMATION","ENTIRE DATABASE CLEARED SUCCESSFULLY.")
		self.idEntry.delete(0,'end')
		self.nameEntry.delete(0,'end')

	def clear_entry(self):
		id=self.idEntry.get()
		name=self.nameEntry.get()
		#deletes entries from the table after taking name and id as key from the user
		c.execute('DELETE FROM employee_formal_details WHERE Id=? AND Name=?',(id,name,))
		c.execute('DELETE FROM employee_personal_details WHERE Id=? AND Name=?',(id,name,))
		conn.commit()
		self.msg=messagebox.showinfo("CONFIRMATION","ENTRY DELETED SUCCESSFULLY")
		self.idEntry.delete(0,'end')
		self.nameEntry.delete(0,'end')		
				
	def close_windows(self):
		self.master.grab_release()
		self.master.destroy()
#read window class
class Read_formal_window:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("READ ENTRY WIZARD")
		self.master.geometry("325x120")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_read=tk.Label(self.master,text="Enter ID :")
		self.readEntry = tk.Entry(self.master, width=30)
		self.read_button=tk.Button(self.master,text="READ ENTRY",width=28,fg="white",bg="grey",command=self.read_entry)
		self.exit_button=tk.Button(self.master,text="EXIT",width=28,fg="white",bg="grey",command=self.close_windows)
		self.blanklabel_1.grid(row=0)
		self.label_read.grid(row=1,sticky=tk.E)
		self.readEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.read_button.grid(row=3,column=1)
		self.exit_button.grid(row=4,column=1)
	
	def read_entry(self):
		Id=self.readEntry.get()
		#shows entry of a single individual after taking id as input from the user
		c.execute("SELECT * FROM employee_formal_details WHERE Id=?",(Id,))
		#fetching table information
		for row in c.fetchall():
			message="EMPLOYEE DETAILS : \n\n"+"Id : "+row[0]+"\nName : "+row[1]+"\nDesignation : "+row[2]+"\nDepartment : "+row[3]+"\nSalary : "+row[4];		
		self.msg=messagebox.showinfo("READ WINDOW",message)
		self.readEntry.delete(0,'end')
	def close_windows(self):
		self.master.grab_release()
		self.master.destroy()


class Read_personal_window:

	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("READ ENTRY WIZARD")
		self.master.geometry("325x120")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_read=tk.Label(self.master,text="Enter ID :")
		self.readEntry = tk.Entry(self.master, width=30)
		self.read_button=tk.Button(self.master,text="READ ENTRY",width=28,fg="white",bg="grey",command=self.read_entry)
		self.exit_button=tk.Button(self.master,text="EXIT",width=28,fg="white",bg="grey",command=self.close_windows)
		self.blanklabel_1.grid(row=0)
		self.label_read.grid(row=1,sticky=tk.E)
		self.readEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.read_button.grid(row=3,column=1)
		self.exit_button.grid(row=4,column=1)
	
	def read_entry(self):
		Id=self.readEntry.get()
		#shows entry of a single individual after taking id as input from the user
		c.execute("SELECT * FROM employee_personal_details WHERE Id=?",(Id,))
		#fetching table information
		for row in c.fetchall():
			message="EMPLOYEE DETAILS : \n\n"+"Id : "+row[0]+"\nName : "+row[1]+"\nGender : "+row[2]+"\nAge : "+row[3]+"\nContact no : "+row[4]+"\nAddress : "+row[5];		
		self.msg=messagebox.showinfo("READ WINDOW",message)
		self.readEntry.delete(0,'end')
	def close_windows(self):
		self.master.grab_release()
		self.master.destroy()

#update window class
class Update_window():

	def __init__(self, update):
		self.update = update
		self.update.grab_set()
		self.update.title("UPDATE WIZARD")
		self.update.geometry("380x345")		
		
		self.blanklabel_1=tk.Label(self.update,text=" ")
		self.blanklabel_2=tk.Label(self.update,text=" ")
		self.label_id=tk.Label(self.update,text="Enter existing ID :")
		self.id_Entry = tk.Entry(self.update, width=30)
		
		self.Updateid_button=tk.Button(self.update,text="UPDATE ID",width=28,fg="white",bg="grey",command=self.iddb)
		self.Updatename_button=tk.Button(self.update,text="UPDATE NAME",width=28,fg="white",bg="grey",command=self.namedb)
		self.Updatesalary_button=tk.Button(self.update,text="UPDATE SALARY",width=28,fg="white",bg="grey",command=self.salarydb)
		self.Updatedept_button=tk.Button(self.update,text="UPDATE DEPARTMENT",width=28,fg="white",bg="grey",command=self.deptdb)
		self.Exit_button=tk.Button(self.update,text="EXIT",width=28,fg="white",bg="grey",command=self.close_windows)
		self.Updatedesignation_button=tk.Button(self.update,text="UPDATE DESIGNATION",width=28,fg="white",bg="grey",command=self.desigdb)
		self.Updategender_button=tk.Button(self.update,text="UPDATE GENDER",width=28,fg="white",bg="grey",command=self.genderdb)
		self.Updateage_button=tk.Button(self.update,text="UPDATE AGE",width=28,fg="white",bg="grey",command=self.agedb)	
		self.Updatecontactno_button=tk.Button(self.update,text="UPDATE CONTACT NO.",width=28,fg="white",bg="grey",command=self.contactdb)
		self.Updateaddress_button=tk.Button(self.update,text="UPDATE ADDRESS",width=28,fg="white",bg="grey",command=self.addressdb)	

		self.blanklabel_2.grid(row=0)

		self.label_id.grid(row=1,sticky=tk.E)
		self.id_Entry.grid(row=1,column=1)
		
		self.blanklabel_1.grid(row=6,column=1)
		self.Updateid_button.grid(row=7,column=1)
		self.Updatename_button.grid(row=8,column=1)
		self.Updatedesignation_button.grid(row=9,column=1)
		self.Updatesalary_button.grid(row=10,column=1)
		self.Updatedept_button.grid(row=11,column=1)
		self.Updategender_button.grid(row=12,column=1)
		self.Updateage_button.grid(row=13,column=1)
		self.Updatecontactno_button.grid(row=14,column=1)
		self.Updateaddress_button.grid(row=15,column=1)
		self.Exit_button.grid(row=16,column=1)
	
	def iddb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_id(self.newWindow)	
	def namedb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_name(self.newWindow)
	def salarydb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_salary(self.newWindow)
	def desigdb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_desig(self.newWindow)
	def deptdb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_dept(self.newWindow)
	def genderdb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_gender(self.newWindow)
	def agedb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_age(self.newWindow)
	def contactdb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_contact(self.newWindow)
	def addressdb(self):
		global id_get
		id_get=self.id_Entry.get()
		self.newWindow = tk.Toplevel(self.update)
		self.app = Update_address(self.newWindow)
	def close_windows(self):
		self.update.destroy()
		self.update.grab_release()

#update id button event class
class Update_id:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE ID WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_id=tk.Label(self.master,text="Enter New ID :")
		self.idEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_id.grid(row=1,sticky=tk.E)
		self.idEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newid=self.idEntry.get()
		#updating old id by taking it as key
		c.execute('UPDATE employee_formal_details SET ID=? WHERE Id=?',(newid,id_get))
		c.execute('UPDATE employee_personal_details SET ID=? WHERE Id=?',(newid,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","ID SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

#update name button event class
class Update_name:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE NAME WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_name=tk.Label(self.master,text="Enter New Name :")
		self.nameEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_name.grid(row=1,sticky=tk.E)
		self.nameEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newname=self.nameEntry.get()
		#updating name by taking id as key
		c.execute('UPDATE employee_formal_details SET Name=? WHERE Id=?',(newname,id_get))
		c.execute('UPDATE employee_personal_details SET Name=? WHERE Id=?',(newname,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","NAME SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

#update salary button event class
class Update_salary:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE SALARY WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_salary=tk.Label(self.master,text="Enter New Salary :")
		self.salaryEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_salary.grid(row=1,sticky=tk.E)
		self.salaryEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newsalary=self.salaryEntry.get()
		#updating salary by taking id as key
		c.execute('UPDATE employee_formal_details SET Salary=? WHERE Id=?',(newsalary,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","SALARY SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

#update designation button event class
class Update_desig:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE DESIGNATION WIZARD")
		self.master.geometry("410x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_desig=tk.Label(self.master,text="Enter New Designation :")
		self.desigEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_desig.grid(row=1,sticky=tk.E)
		self.desigEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newdesig=self.desigEntry.get()
		#updating designation by taking id as key
		c.execute('UPDATE employee_formal_details SET Designation=? WHERE Id=?',(newdesig,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","DESIGNATION SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

#update days button event class
class Update_dept:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE DEPARTMENT WIZARD")
		self.master.geometry("420x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_dept=tk.Label(self.master,text="Enter New Department :")
		self.deptEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_dept.grid(row=1,sticky=tk.E)
		self.deptEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newdept=self.deptEntry.get()
		#updating days by taking id as key
		c.execute('UPDATE employee_formal_details SET Department=? WHERE Id=?',(newdept,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","DAYS SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

class Update_gender:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE GENDER WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_gender=tk.Label(self.master,text="Enter New Gender :")
		self.genderEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_gender.grid(row=1,sticky=tk.E)
		self.genderEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newgender=self.genderEntry.get()
		#updating days by taking id as key
		c.execute('UPDATE employee_personal_details SET Gender=? WHERE Id=?',(newgender,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","GENDER SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

class Update_age:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE AGE WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_age=tk.Label(self.master,text="Enter New Age :")
		self.ageEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_age.grid(row=1,sticky=tk.E)
		self.ageEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newage=self.ageEntry.get()
		#updating days by taking id as key
		c.execute('UPDATE employee_personal_details SET Age=? WHERE Id=?',(newage,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","AGE SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

class Update_contact:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE CONTACT NUMBER WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_contact=tk.Label(self.master,text="Enter New Contact :")
		self.contactEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_contact.grid(row=1,sticky=tk.E)
		self.contactEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newcontact=self.contactEntry.get()
		#updating days by taking id as key
		c.execute('UPDATE employee_personal_details SET Contact_no=? WHERE Id=?',(newcontact,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","CONTACT NUMBER SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()

class Update_address:
	def __init__(self, master):
		self.master = master
		self.master.grab_set()
		self.master.title("UPDATE ADDRESS WIZARD")
		self.master.geometry("380x110")
		
		self.blanklabel_1=tk.Label(self.master,text=" ")
		self.blanklabel_2=tk.Label(self.master,text=" ")

		self.label_address=tk.Label(self.master,text="Enter New Address :")
		self.addressEntry = tk.Entry(self.master, width=30)
		self.done_button=tk.Button(self.master,text="DONE",width=28,fg="white",bg="grey",command=self.close_windows)
		
		self.blanklabel_1.grid(row=0)
		self.label_address.grid(row=1,sticky=tk.E)
		self.addressEntry.grid(row=1,column=1)

		self.blanklabel_2.grid(row=2)
		self.done_button.grid(row=3,column=1)
	
	def close_windows(self):
		newaddress=self.addressEntry.get()
		#updating days by taking id as key
		c.execute('UPDATE employee_personal_details SET Address=? WHERE Id=?',(newaddress,id_get))
		conn.commit()
		self.msg=messagebox.showinfo("UPDATE WINDOW","ADDRESS SUCCESSFULLY UPDATED.")
		self.master.grab_release()
		self.master.destroy()
def main(): 
    	root = tk.Tk()
    	app = Main_window(root)

	#creating an infinite loop to display the index window
    	root.mainloop()

if __name__ == '__main__':
    	main()
