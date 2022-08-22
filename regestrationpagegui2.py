import tkinter as tk

from tkinter import *
from tkinter import messagebox
import mysql.connector
import re
import webbrowser
import base64

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="WeCare")
cursor = mydb.cursor()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
base = Tk()
base.title("WeCare - Registration")
base.geometry("500x600")
base.resizable(width=FALSE, height=FALSE)

reg = Label(base, text="Create/Register Your Account:", font=('Verdana', 10, 'bold', 'underline'), fg='black')
reg.place(x=128, y=20)

fname = Label(base, text="First Name:", font=('Verdana', 10))
fname.place(x=35, y=70)

lname = Label(base, text="Last Name:", font=('Verdana', 10))
lname.place(x=260, y=70)

email = Label(base, text="Email ID:", font=('Verdana', 10))
email.place(x=35, y=150)

ageinp = Label(base, text="Age (in years):", font=('Verdana', 10))
ageinp.place(x=220, y=220)

contno = Label(base, text="Contact No.:", font=('Verdana', 10))
contno.place(x=233.5, y=265)

genorsex = Label(base, text="Gender/Sex:", font=('Verdana', 10))
genorsex.place(x=35, y=200)

otgenorsex = Label(base, text="if other, please specify:", font=('Verdana', 10))
otgenorsex.place(x=35, y=315)

uqusername = Label(base, text="Create a Unique Username for Your Account:", font=('Verdana', 10))
uqusername.place(x=35, y=370)

stpass = Label(base, text="Create a Strong Password for Your Account:", font=('Verdana', 10))
stpass.place(x=35, y=430)


def descmd():
    otgen_input.delete("1.0", tk.END)
    otgen_input.config(state=DISABLED)


def enbcmd():
    otgen_input.config(state=NORMAL)
    otgen_input.get(1.0, "end-1c")


v0 = IntVar()
v0.set(0)
r1 = Radiobutton(base, text="Male", variable=v0, value=1, command=descmd)
r1.place(x=40, y=225)
r2 = Radiobutton(base, text="Female", variable=v0, value=2, command=descmd)
r2.place(x=40, y=250)
r3 = Radiobutton(base, text="Other", variable=v0, value=3, command=enbcmd)
r3.place(x=40, y=275)

ftname = Text(base, height=2, width=25)
# ftname.insert(END,"Enter First name")
ftname.pack()
ftname.place(x=35, y=95)

ltname = Text(base, height=2, width=25)
# ltname.insert(END,"Enter Last name")
ltname.pack()
ltname.place(x=260, y=95)

emailid = Text(base, height=2, width=45)
# emailid.insert(END,"Enter a valid email address")
emailid.pack()
emailid.place(x=101, y=145)


def Validate(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isdigit():
            return False
    return True


Age_Inpt = tk.StringVar()

age_input = Entry(base, validate="key", textvariable=Age_Inpt)
age_input.place(x=333, y=220, width=133, height=25)
age_input['validatecommand'] = (age_input.register(Validate), '%P', '%d')

# age_input = Text(base, height=2, width=16)
# ageinpinyr.insert(END,"(only numbers)")
# age_input.pack()
# age_input.place(x=333, y=215)

Phn_Inpt = tk.StringVar()
contact_input = Entry(base, validate="key", textvariable=Phn_Inpt)
contact_input.place(x=333, y=265, width=133, height=25)
contact_input['validatecommand'] = (contact_input.register(Validate), '%P', '%d')

# contact_input.insert(END,"(only numbers)")
# contact_input.pack()
# reg = base.register(Validate_contact())
# contact_input.config(validate ="key", validatecommand =(reg, '% d'))


otgen_input = Text(base, height=2, width=32)
# otgen_input.insert(END,"wrixte here..")
otgen_input.pack()
otgen_input.place(x=206.5, y=310)
otgen_input.config(state=DISABLED)

username_input = Text(base, height=1, width=38)
# username_input.insert(END,"create your username..")
username_input.pack()
username_input.place(x=35, y=395)

stpass_input = Entry(base, show="*")
stpass_input.place(x=35, y=455, width=435, height=20)


def showpassfun():
    if var.get() == 1:
        stpass_input.configure(show="")
    elif var.get() == 0:
        stpass_input.configure(show="*")


var = IntVar()

bt = Checkbutton(base, command=showpassfun, offvalue=0, onvalue=1, variable=var)
bt.place(x=451, y=430)

def checkusername():
    Uname = username_input.get(1.0, "end-1c")
    loadname = """SELECT * FROM user WHERE username = %s"""
    cursor.execute(loadname, (Uname,))
    # cursor.execute('SELECT username FROM user WHERE username=?', (Uname,))
    cursor.fetchall()

    #print(cursor.rowcount)

    if((len(Uname) == 0)):
        messagebox.showerror("error", "Empty Username.")
    elif cursor.rowcount > 0:
        # print("edit username")
        wrongusrname = Label(base, text="!! Username already exists.", fg='red', font=('Verdana', 7))
        wrongusrname.place(x=345, y=395)
        base.after(2000, wrongusrname.destroy)
    else:
        validusrname = Label(base, text="✔ Unique Username.", fg='green', font=('Verdana', 7))
        validusrname.place(x=345, y=395)
        base.after(2000, validusrname.destroy)

chkusrnmbtn = Button(base, text="Check!", fg='black', bg='light blue', command=checkusername)
chkusrnmbtn.place(x=383, y=365)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def error():
    # messagebox.showerror("error", "try again")
    # messagebox.showinfo("my message","this is an example of showinfo\nmessagebox")
    messagebox.showwarning("warning", "Please Enter a valid email address")


def error1():
    messagebox.showinfo("Popup", "Registered successfully")


def error2():
    messagebox.showwarning("warning", "Please fill all inputs")


def error3():
    # messagebox.showerror("error", "try again")
    # messagebox.showinfo("my message","this is an example of showinfo\nmessagebox")
    messagebox.showwarning("warning", "Please Enter a 10 Digits integer value in contacts")


def error4():
    messagebox.showerror("error", "Username exist")
    # messagebox.showinfo("my message","this is an example of showinfo\nmessagebox")
    # messagebox.showwarning("warning", "Please Enter a 10 Digits integer value in contacts" )

def gotologin():
    base.destroy()
    import Login_Page


def Input():
    # inp = ftname.get(1.0, "end-1c")
    gender = ""
    radio = v0.get()
    if radio == 1:
        gender = "male"
        otgen_input.delete("1.0", tk.END)
        otgen_input.insert(END, "")
        # otgen_input.config(state=DISABLED)
    elif radio == 2:
        gender = "female"
        otgen_input.delete("1.0", tk.END)
        otgen_input.insert(END, "")
        # otgen_input.config(state=DISABLED)
    elif radio == 3:
        gender = otgen_input.get(1.0, "end-1c")

    Fname = ftname.get(1.0, "end-1c")
    Lname = ltname.get(1.0, "end-1c")
    Email = emailid.get(1.0, "end-1c")
    # print("Plz enter a valid email")
    # gender = input("enter the Gender :   ")

    Uname = username_input.get(1.0, "end-1c")

    passwd = stpass_input.get()
    sample_string_bytes = passwd.encode("ascii")
    base64_passwd = base64.b64encode(sample_string_bytes)
    # print(base64_passwd)

    age = age_input.get()
    contact = Phn_Inpt.get()

    # loadpass = ("SELECT Password FFROM users WHERE Password = %s")
    sql = (
        "INSERT into user" "(first_name,last_name,email,gender,username,password,age,phone_number)" "VALUES (%s,%s,%s,%s,%s,%s,%s,%s)")
    variables = (Fname, Lname, Email, gender, Uname, base64_passwd, age, contact)

    # cursor.execute("""INSERT into login (username,password,ID) VALUES (%s,%s,%d) """,(Uname,paswd,uID))

    # cursor.fetchall()
    # first=cursor.rowcount
    # data = sql.sqlExec("select * from user")
    # print(len(data))
    if ((len(Fname) == 0) or (len(Lname) == 0) or (len(Email) == 0) or (len(Uname) == 0) or (len(passwd) == 0) or (
            len(age) == 0) or (len(str(contact)) == 0) or (len(gender) == 0) or (radio == 0)):
        error2()
    else:

        if (re.search(regex, Email)):
            # print(type(contact))
            if (len(contact) == 10):

                # print("check sucessful")
                loadname = """SELECT * FROM user WHERE username = %s"""
                cursor.execute(loadname,(Uname,))
                #cursor.execute('SELECT username FROM user WHERE username=?', (Uname,))
                cursor.fetchall()

                print(cursor.rowcount)

                if cursor.rowcount > 0:
                    #print("edit username")
                    error4()


                else:
                    cursor.execute(sql, variables)
                    mydb.commit()
                    error1()
                    gotologin()

                    """print(cursor.rowcount)
                    print(cursor.fetchall())
                    print(loadname)
                    print(Uname)"""

            else:
                error3()
        else:
            error()


regbtn = Button(base, text="Register  ", fg='white', bg='red', width=60, command=Input)
regbtn.place(x=35, y=530)


# Define a callback function
def callback(url):
    webbrowser.open_new_tab(url)


refbtn = Button(base, text="Need help to generate a strong password?\nClick here..", fg='blue', borderwidth=0,
                cursor="hand2")
refbtn.place(x=133, y=485)
refbtn.bind("<Button-1>", lambda e: callback("https://github.com/madhavsingh31/Java_Project-Password_Generator"))

mtlgpagebtn = Button(base, text="-->>> Move to Login Page by clicking here <<<--", borderwidth=0, command=gotologin)
mtlgpagebtn.place(x=106, y=563)

base.mainloop()
