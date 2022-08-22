from tkinter import *
from tkinter.ttk import *
from tkinter import *
from tkinter import messagebox

import mysql.connector
import base64

mydb=mysql.connector.connect( host="localhost",user="root",password="",database="WeCare")
cursor = mydb.cursor()

base1 = Tk()
base1.title("WeCare - Login")
base1.geometry("300x300")
base1.resizable(width=FALSE, height=FALSE)

login = Label(base1, text="Login to your account:", font=('Verdana', 10, 'bold', 'underline'))
login.place(x=65, y=20)

logincredid = Label(base1, text="User Name:", font=('Verdana', 10))
logincredid.place(x=27, y=60)

logincredpass = Label(base1, text="Password:", font=('Verdana', 10))
logincredpass.place(x=27, y=120)

orlbl = Label(base1, text="or", font=('Verdana', 8))
orlbl.place(x=138, y=223)

username = Text(base1, height=1, width=30)
#username.insert(END,"Enter your username ")
username.pack()
username.place(x=27, y=85)

def error_box1():
    messagebox.showwarning("warning", "Please fill all inputs" )

def error_box2():
    messagebox.showwarning("warning", "Enter valid Credentials" )

def Chat_Page():
    base1.destroy()
    import chatguitest

def CheckInput():

    Uname=username.get(1.0,'end-1c')
    #Passwd=userpass.get()
    passwd = userpass.get()

    sample_string_bytes = passwd.encode("ascii")
    base64_passwd = base64.b64encode(sample_string_bytes)
    #print(base64_passwd)
   #base64.
    #sample_string_bytes = Passwd.encode("ascii")
    #base64_passwd = base64.b64decode(sample_string_bytes)
    #Decoded_passwd=base64_passwd.decode("ascii")
    #sql=("SELECT EXISTS(SELECT * FROM login_details WHERE username = Uname AND password = Passwd)")

    sql= ('SELECT * FROM user WHERE username = %s AND password = %s')
    cursor.execute(sql,(Uname, base64_passwd))
    cursor.fetchall()

    if((len(Uname)==0) or (len(passwd)==0)):
        error_box1()
    else:
        if cursor.rowcount == 1:
            base1.destroy()
            print("successfully Logged In")

            # BELOW CODE IS TO PRINT THE USER's DATA IN THE CHATBOT
            sql1 = 'SELECT first_name,last_name,age,phone_number,gender FROM user WHERE username = %s'
            cursor.execute(sql1, (Uname,))
            Raw_output = cursor.fetchall()
            Final_list = []
            for x in Raw_output:
                for i in range(5):
                    Final_list.append(x[i])

            import train_chatbot

            import nltk
            from nltk.stem import WordNetLemmatizer
            lemmatizer = WordNetLemmatizer()
            import pickle
            import numpy as np
            from tkinter.filedialog import askopenfile, asksaveasfilename

            from keras.models import load_model
            model = load_model('chatbot_model.h5')
            import json
            import random
            intents = json.loads(open('intents.json').read())
            words = pickle.load(open('words.pkl', 'rb'))
            classes = pickle.load(open('classes.pkl', 'rb'))

            def clean_up_sentence(sentence):
                sentence_words = nltk.word_tokenize(sentence)
                sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
                return sentence_words

            # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

            def bow(sentence, words, show_details=True):
                # tokenize the pattern
                sentence_words = clean_up_sentence(sentence)
                # bag of words - matrix of N words, vocabulary matrix
                bag = [0] * len(words)
                for s in sentence_words:
                    for i, w in enumerate(words):
                        if w == s:
                            # assign 1 if current word is in the vocabulary position
                            bag[i] = 1
                            if show_details:
                                print("found in bag: %s" % w)
                return (np.array(bag))

            def predict_class(sentence, model):
                # filter out predictions below a threshold
                p = bow(sentence, words, show_details=False)
                res = model.predict(np.array([p]))[0]
                ERROR_THRESHOLD = 0.25
                results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
                # sort by strength of probability
                results.sort(key=lambda x: x[1], reverse=True)
                return_list = []
                for r in results:
                    return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
                return return_list

            def getResponse(ints, intents_json):
                tag = ints[0]['intent']
                list_of_intents = intents_json['intents']
                for i in list_of_intents:
                    if (i['tag'] == tag):
                        result = random.choice(i['responses'])
                        break
                return result

            def chatbot_response(msg):
                ints = predict_class(msg, model)
                res = getResponse(ints, intents)
                return res

            # Creating GUI with tkinter

            # Creating GUI with tkinter
            import tkinter
            import tkinter as tk
            import tkinter.messagebox
            import os
            import random

            from tkinter.tix import Tk

            import datetime as dt
            import time

            def send():
                msg = EntryBox.get("1.0", 'end-1c').strip()
                EntryBox.delete("0.0", END)
                if msg != '':
                    ChatLog.config(state=NORMAL)
                    ChatLog.insert(END, "You: " + msg + '\n\n')
                    ChatLog.config(foreground="#442265", font=("Verdana", 12))
                    res = chatbot_response(msg)
                    ChatLog.insert(END, "WeCare: " + res + '\n\n')
                    ChatLog.config(state=DISABLED)
                    ChatLog.yview(END)
                    timedate = Label(base,
                                     text="Last message sent:  " + f"{dt.datetime.now():%a, '%B %d, %Y'}" + '  at  ' + f"{dt.datetime.now():'%I:%M:%S %p'}",
                                     fg="black", font=("vrenda", 10))
                    timedate.place(x=406, y=480)

            def savechat():
                filepath = asksaveasfilename(
                    defaultextension="txt",
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                )
                if not filepath:
                    return
                with open(filepath, "w") as output_file:
                    text1="Patient information:\n\n"
                    text2="Name: "
                    textsp=' '
                    textint1= Final_list[0]
                    textint5= Final_list[1]
                    text3="\nAge: "
                    textint2= str(Final_list[2])
                    text4="\nContact: "
                    textint3= str(Final_list[3])
                    text5="\nGender/Sex: "
                    textint4= Final_list[4]
                    text0="\n\n\nChats:\n\n"
                    textsep="\n________________________________"
                    text = ChatLog.get(1.0, tk.END)
                    default = "\nWarning: \nAll the information provided by this application is very basic. It is very important to consult your family doctor and consume medicines with doctor's advise."
                    output_file.write(
                        text1 + text2 + textint1 + textsp + textint5 + text3 + textint2 + text5 + textint4 + text4 + textint3 + textsep + text0 + text + "_________\n\n[Chat saved on:  " + f"{dt.datetime.now():%a, '%B %d, %Y'}" + '  at  ' + f"{dt.datetime.now():'%I:%M:%S %p'}]\n\n" + textsep + default)
                # base.title(f"Text Editor Application - {filepath}")

            base = Tk()
            base.title("WeCare")
            base.geometry("800x500")
            base.resizable(width=FALSE, height=FALSE)

            sbtn = button = Button(base, font=("Verdana", 9), bg="light blue", text="Save Chat", command=savechat)
            sbtn.place(x=320, y=8)

            # Create Chat window
            ChatLog = Text(base, bd=1, bg="white", height="8", width="50", font="Arial", )
            ChatLog.config(state=DISABLED)

            # Bind scrollbar to Chat window
            scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
            ChatLog['yscrollcommand'] = scrollbar.set

            # Create Button to send message
            SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send   ", width="12", height=5,
                                bd=1, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                                command=send)

            # Create the box to enter message
            EntryBox = Text(base, bd=1, bg="white", width="29", height="5", font="Arial")
            # EntryBox.bind("<Return>", send)
            # EntryBox.insert(END,"type your message here..")
            EntryBox.pack()

            """def defaultentry(event):
                current = EntryBox.get("1.0", tk.END)
                if current == "type your message here..\n":
                    EntryBox.delete("1.0", tk.END)
                elif current == "\n":
                    EntryBox.insert("1.0", "type your message here..")

            EntryBox.bind("<FocusIn>", defaultentry)
            EntryBox.bind("<FocusOut>", defaultentry)"""

            # Creating a button with doctor's image that will tell user about how to operate the gui
            def helloCallBack():
                tkinter.messagebox.showinfo("Help",
                                            "Hi there! \nI am your medical chatbot. You can talk to me about anything and anytime. Consider me as your friend :)\n\nJust tell me, how are you feeling right now, in the entry box and start talking to me. We shall discuss the all the possible solutions together and I promise that I shall never judge you..\nYou can trust me :)")

            txt = Label(base, text='WeCare:', font=('Verdana', 15))
            txt1 = Label(base, text="^^^ Click Above Button^^^\n(if you want to know how it's work)")
            # txt2=Label(base, text="©WeCare - Let's be sure..")

            timedate = Label(base, text="No messages sent.", fg="black", font=("vrenda", 10))
            timedate.place(x=406, y=480)

            # create a list of different colors
            colors = ["black"]

            def color_changer():
                # choose and configure random color to the label text
                fg = random.choice(colors)
                copyrighttext.config(fg=fg)

                # call the color_changer() method after 200 micro seconds
                copyrighttext.after(2500, color_changer)

                # create a list of different texts
                labels = ["©WeCare - Let's be sure..", "• Madhav Singh Rawat - 19BCS3543", "• Shrey Jain - 19BCS3541",
                          "• Rishabh Mohata - 19BCS3542", "", "• Rashita - 19BCS3554", ""]
                # choose and configure random text to the label
                text = random.choice(labels)
                copyrighttext.config(text=text)

            copyrighttext = Label(base)
            color_changer()

            name_output = Label(base, text=Final_list[0] + ' ' + Final_list[1], font=('Verdana', 10))
            name_output.place(x=100, y=60)
            age_output = Label(base, text=Final_list[2], font=('Verdana', 10))
            age_output.place(x=300, y=60)
            sex_output = Label(base, text=Final_list[4], font=('Verdana', 10))
            sex_output.place(x=300, y=95)
            contact_output = Label(base, text=Final_list[3], font=('Verdana', 10))
            contact_output.place(x=100, y=95)



            photo = PhotoImage(file=r"D:\Desktop\WeCare- Medical Chatbot\images3.png")
            photoimage = photo.subsample(1, 1)
            # photoimage.place(x=6, y=50, height=50, weidth=50)
            btn = Button(base, image=photoimage, compound=LEFT, command=helloCallBack)

            # Creating labels that will show personal information
            patientinformation = Label(base, text="Patient Information:", font=('Verdana', 10, 'bold', 'underline'))
            patientinformation.place(x=20, y=20)
            name = Label(base, text="Name:", font=('Vdana', 10))
            name.place(x=20, y=60)
            contact = Label(base, text="Phone No.:", font=('Verdana', 10))
            contact.place(x=20, y=95)
            age = Label(base, text="Age:", font=('Verdana', 10))
            age.place(x=268, y=60)
            sex = Label(base, text="Sex:", font=('Verdana', 10))
            sex.place(x=268, y=95)

            # Place all components on the screen
            scrollbar.place(x=776, y=6, height=386)
            ChatLog.place(x=406, y=6, height=386, width=370)
            EntryBox.place(x=528, y=401, height=77, width=265)
            SendButton.place(x=406, y=401, height=77)
            txt.place(x=150, y=145)
            txt1.place(x=98.5, y=430)
            # txt2.place(x=6, y=480)
            copyrighttext.place(x=6, y=480)
            btn.place(x=80, y=180)
            base.mainloop()

            """import tkinter
            from tkinter import *


            def send():
                msg = EntryBox.get("1.0",'end-1c').strip()
                EntryBox.delete("0.0",END)

                if msg != '':
                    ChatLog.config(state=NORMAL)
                    ChatLog.insert(END, "You: " + msg + '\n\n')
                    ChatLog.config(foreground="#442265", font=("Verdana", 12 ))

                    res = chatbot_response(msg)
                    ChatLog.insert(END, "Doctor: " + res + '\n\n')

                    ChatLog.config(state=DISABLED)
                    ChatLog.yview(END)


            base = Tk()
            base.title("Hello")
            base.geometry("400x500")
            base.resizable(width=FALSE, height=FALSE)

            #Create Chat window
            ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)

            ChatLog.config(state=DISABLED)

            #Bind scrollbar to Chat window
            scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
            ChatLog['yscrollcommand'] = scrollbar.set

            #Create Button to send message
            SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                                bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                                command= send )

            #Create the box to enter message
            EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
            #EntryBox.bind("<Return>", send)


            #Place all components on the screen
            scrollbar.place(x=376,y=6, height=386)
            ChatLog.place(x=6,y=6, height=386, width=370)
            EntryBox.place(x=128, y=401, height=90, width=265)
            SendButton.place(x=6, y=401, height=90)

            base.mainloop()"""

        else:
            error_box2()
            #print("false")



        # Fetch one record and return result
    #variables=(Uname,Passwd)
    #cursor.execute(sql,variables)
    #user = cursor.fetchone()
    #print(Passwd, Uname)

userpass=Entry(base1, show = "*")
userpass.place(x=27, y=145, width=245, height=19)

def showpasslogfun() :
    if var.get() == 1 :
        userpass.configure(show = "")
    elif var.get() == 0 :
        userpass.configure(show = "*")

var = IntVar()

bt = Checkbutton(base1, command = showpasslogfun, offvalue = 0, onvalue = 1, variable = var)
bt.place(x = 255, y = 120)

loginbtn=Button(base1, text="Login", width=34, fg='white', bg='blue', command=CheckInput)
loginbtn.place(x=25, y=185)

"""frgtpass=Button(base1, text="forgot your password", font=('Verdana', 8, 'bold'), borderwidth = 0)
frgtpass.place(x=76, y=230)"""
def gotoregistration():
    base1.destroy()
    import regestrationpagegui2
mtregbtn=Button(base1, text="Register Your Account", font=('Verdana', 8), fg='red', borderwidth = 0,command=gotoregistration)
mtregbtn.place(x=82.9, y=251)

base1.mainloop()