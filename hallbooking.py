import sqlite3
import webbrowser
import tkinter as tk
import winsound
from tkinter import ttk
from tkinter import messagebox
conn=sqlite3.connect('hall_booking.db')
cursor=conn.cursor()
#cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
#              user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#               user_name TEXT NOT NULL
#               );''')'''
cursor.execute('''CREATE TABLE IF NOT EXISTS HALLS(
               buildingName TEXT NOT NULL ,
                Room_No Integer not null,
                Primary key(buildingName,Room_No) 
               );''')
cursor.execute('''CREATE TABLE IF NOT EXISTS booking (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    buildingName TEXT NOT NULL,
    Room_No INTEGER,
    booking_date TEXT,
    startTime INTEGER,
    endTime INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (buildingName, Room_No) REFERENCES HALLS(buildingName, Room_No)
);''')
who="user"
global n
n=0
win =tk.Tk()
win.title("CED Project 005")
'''style=ttk.Style()
style.theme_use("clam")
win.configure(bg="#2E2E2E")'''
win.geometry("400x300")
label=tk.Label(win,text="Welcome to room booking services!",font=("Arial",16))
global whov
whov = tk.StringVar(value=f"You are signed in as: {who}")
labelwho=tk.Label(win,textvariable=whov,font=("Arial",16))
labelwho.pack(pady=10)
def adminsign():
    subwin=tk.Toplevel(win)
    subwin.geometry("300x200")
    subwin.title("signin")
    subwin.grab_set()
    subwin.focus_set()
    subwin.transient(win)
    

    labelsw1=tk.Label(subwin,text="Sign in for admin privledge")
    labelsw1.pack(padx=10,pady=10)
    labelsw2=tk.Label(subwin,text="Enter the password")
    labelsw2.pack(padx=0,pady=10)
    entrysw=tk.Entry(subwin)
    entrysw.pack(pady=10)
    entrysw.focus_set()

    def getus(event=None):
        password=entrysw.get()
        if password=="1234":
            global n
            if n>=1:
                messagebox.showinfo("Signed in as admin","Already signed in as admin") 
                return
            else:    
                signm.add_command(label="signout",command=signout)
                global who
                who="admin"
                whov.set(f"You are signed in as: {who}")
                subwin.destroy()
                winsound.Beep(900,200)
                messagebox.showinfo("Signed in as admin","Welcome admin") 
                n+=1 
        else:
            winsound.Beep(500,100)
            messagebox.showinfo("Incorrect Password","The Password is Incorrect")
            return
    button2=tk.Button(subwin,text="Enter",command=getus)
    button2.pack(pady=10)
    subwin.bind("<Return>",lambda event:getus())
#button = tk.Button(win,text="Click Me",command=onbc)
#button.pack(pady=20)
label.pack(pady=20)
j=0
def open():
    webbrowser.open("https://anmol02122005.github.io/CED-Project-/")

entry=tk.Entry(win,width=30)
entry.pack(pady=10,ipady=4)
entry.focus_set()
def roomExists(buildingName:str,roomId:str):
    cursor.execute('SELECT * FROM HALLS WHERE buildingName = ? AND Room_No = ? ', (buildingName, int(roomId) ))  
    result=cursor.fetchone()
    if result is None:
        winsound.Beep(500,300)
        messagebox.showinfo("Invalid Room","Room is not available for booking or does not exists")
        return 0
    else:
        return 1
def authenticate():
    if who!="admin":
        winsound.Beep(500,300)
        messagebox.showinfo("Permission denied","You need admin priviledge to do that")
        return 0
    else:
        return 1
def processInstruction():
    if len(tokens) < 1: 
        winsound.Beep(400,200)
        messagebox.showinfo("Input Error", "Please enter a command.")
       # return
    tokens[0]=tokens[0].lower()
    global length
    length=len(tokens)
    if length>1:
        tokens[1]=tokens[1].lower()
    if tokens[0]=="add" and length==3:
        valid(tokens[2])
        addRoom(tokens[1],tokens[2])
    elif tokens[0]=="remove" and length==3:
        valid(tokens[2])
        removeRoom(tokens[1],tokens[2]) 
    elif tokens[0]=="reserve" and length==5:
        run()
        reserveRoom(tokens[1],tokens[2],int(tokens[3]),int(tokens[4]))
    elif tokens[0]=="cancel" and length==5:
        run()
        cancelRoom(tokens[1],tokens[2],int(tokens[3]),int(tokens[4]))
    elif tokens[0]=="rooms" and length==1:
        displayRooms()
    elif tokens[0]=="timeslots" and length==1:
        displayTimeSlots()
    elif tokens[0]=="exit"  and length==1:
        win.quit()
    elif tokens[0]=="delete"  and length==1:
        whichtable()
    elif tokens[0]=="edit" and length==7:
        editRoom(tokens[1],tokens[2],int(tokens[3]),int(tokens[4]),int(tokens[5]),int(tokens[6]))
    else:
        messagebox.showinfo("Invalid Command","Please enter a valid command")
        j=1
if j!=1:
    entry.delete(0, tk.END)    
    j=0
def whichtable():
    global tabs
    tabs=tk.Tk()
    tabs.title("Select records to delete")
    tabs.geometry("400x200")
    global listbox
    listbox = tk.Listbox(tabs, selectmode=tk.MULTIPLE, height=5)
    options = ["HALLS", "booking"] 
    for option in options:
        listbox.insert(tk.END,option)
    listbox.pack(pady=10)
    btn = tk.Button(tabs, text="Submit", command=choices)
    btn.pack(pady=10)
def valid(val):
    try:
        return int(val)  
    except ValueError:
        winsound.Beep(400,250)
        messagebox.showerror("Invalid Input", f"'{val}' is not a valid integer.")
        return None

def run():
    valid(tokens[2])
    valid(tokens[3])
    valid(tokens[4])
def choices():
    choicesmade=listbox.curselection()  # Get the indices of the selected items
    for i in choicesmade:
        deleteTable(listbox.get(i))
    tabs.destroy()
    
def deleteTable(Table_name:str):
    if authenticate():
        cursor.execute(f'''Select * FROM {Table_name}''') 
        data=cursor.fetchone()
        if data: 
            try:
                cursor.execute(f'''DELETE FROM {Table_name}''')  
                conn.commit()
                winsound.Beep(900,100)
                messagebox.showinfo("Success", f"All records in '{Table_name}' deleted.")
            except sqlite3.OperationalError as t:
                messagebox.showerror("Error", f"Failed to delete table '{Table_name}': {t}")
        else:
             messagebox.showerror("No Data found", f"'{Table_name} is already empty'")
def getFields(event=None):
    
    global tokens
    user_input=entry.get()
    tokens= user_input.split()
    processInstruction()
    #messagebox.showinfo("Input",f"You entered:{user_input.split()}")
def addRoom(buildingName:str,roomId:str):
    if authenticate():
        cursor.execute('SELECT * FROM Halls WHERE buildingName = ? AND Room_No = ? ', (buildingName, int(roomId) ))  
        result=cursor.fetchone()
        if result is None:
            cursor.execute('INSERT INTO HALLS VALUES (?, ?)', (buildingName, int(roomId)))
            conn.commit()
            winsound.Beep(800,100)
            messagebox.showinfo("Success", f"Room {roomId} in {buildingName} added.")
        else:
            winsound.Beep(500,200)
            messagebox.showinfo("Duplicate entry", f"Room {roomId} in {buildingName} already exists.")
def removeRoom(buildingName:str,roomId:str):
    if authenticate():
        if roomExists(buildingName,roomId):
            cursor.execute('DELETE FROM HALLS WHERE buildingName = ? AND Room_No = ?', (buildingName, int(roomId)))
            conn.commit()
            winsound.Beep(600,200)
            messagebox.showinfo("Success", f"Room {roomId} in {buildingName} removed.") 
def reserveRoom(buildingName:str,roomId:str,startTime:int,endTime:int):
    if roomExists(buildingName,roomId):
        cursor.execute('SELECT * FROM booking WHERE buildingName= ? AND Room_No = ? AND((startTime <= ? AND endTime > ?) OR (startTime < ? AND endTime >= ?) OR(startTime >= ? AND endTime <= ?))',  (buildingName, int(roomId), startTime, startTime, endTime, endTime, startTime, endTime))
        result=cursor.fetchone()
        if result:
            winsound.Beep(500,300)
            messagebox.showinfo("Sorry","This slot is already booked")
        else:
            if 0<=startTime<24 and 0<=endTime<24:
                cursor.execute('INSERT INTO booking (buildingName, Room_No, startTime, endTime) VALUES (?, ?, ?, ?)', (buildingName, int(roomId), startTime, endTime))
                conn.commit()
                winsound.Beep(1000,150)
                messagebox.showinfo("Success", f"Room {roomId} in {buildingName} booked from {startTime} to {endTime}.")
            else:
                winsound.Beep(400,100)
                messagebox.showinfo("Invalid Command", "Start and end times must be between 0 and 23.")
def editRoom(buildingName:str,roomId:str,startTime1:int,endTime1:int,startTime2:int,endTime2:int):
    cancelRoom(buildingName,roomId,startTime1,endTime1)
    reserveRoom(buildingName,roomId,startTime2,endTime2)
def cancelRoom(buildingName:str,roomId:str,startTime:int,endTime:int):
    roomExists(buildingName,roomId)
    cursor.execute('SELECT * FROM booking WHERE buildingName = ? AND Room_No = ? AND startTime = ? AND endTime = ?', (buildingName, int(roomId), startTime, endTime))  
    result=cursor.fetchone()
    if result is None:
        messagebox.showinfo("Slot not found","No such slot booked for this room")
    else:
        cursor.execute('DELETE FROM booking WHERE buildingName = ? AND Room_No = ? AND startTime = ? AND endTime = ?', (buildingName, int(roomId), startTime, endTime))
        conn.commit()

def displayRooms():
   #  showrooms():

    cursor.execute('''select * from HALLS''')
    rooms = cursor.fetchall()
    if rooms:
            showr=tk.Tk()
            showr.title("HALLS Database")
            showr.geometry("300x400")
            tree=ttk.Treeview(showr,columns=("Building_Name","Room_No"),show="headings")
            tree.heading("Building_Name", text="Building_Name")
            tree.heading("Room_No", text="Room_No")
            tree.column("Building_Name", width=150,anchor="center")
            tree.column("Room_No", width=100,anchor="center")
            tree.pack(fill="both",expand=True)
        #rooms_list = "\n".join([f"{room[0]}, {room[1]}" for room in rooms])
        #messagebox.showinfo("Available Rooms", rooms_list)
            for room in rooms:
                tree.insert("", "end", values=(room[0].capitalize(), room[1]))
    else:
        messagebox.showinfo("Available Rooms", "No rooms available.")
def signout():
    global who
    who="user"
    n=0
    winsound.Beep(1100,150)
    signm.delete("signout")
    whov.set(f"You are signed in as: {who}")
def displayTimeSlots():
    cursor.execute('''select buildingName,Room_No,startTime, endTime from booking''')
    slots = cursor.fetchall()
    if slots:
        showt=tk.Tk()
        showt.title("HALLS Database")
        showt.geometry("900x400")
        winsound.Beep(900,100)
        tree=ttk.Treeview(showt,columns=("Building_Name","Room_No","StartTime","EndTime"),show="headings")
        tree.heading("Building_Name", text="Building_Name")
        tree.heading("Room_No", text="Room_No")
        tree.heading("StartTime", text="StartTime")
        tree.heading("EndTime", text="EndTime")
        tree.column("Building_Name", width=150,anchor="center")
        tree.column("Room_No", width=100,anchor="center")
        tree.column("StartTime", width=100,anchor="center")
        tree.column("EndTime", width=100,anchor="center")
        tree.pack(fill="both",expand=True)
        #slots_list = "\n".join([f"Building: {slot[0]}, Room: {slot[1]}, Time: {slot[2]} to {slot[3]}" for slot in slots])
        #messagebox.showinfo("Booked Time Slots", slots_list)
        for slot in slots:
                tree.insert("", "end", values=(slot[0].capitalize(), slot[1],slot[2],slot[3]))
    else:
        messagebox.showinfo("Booked Time Slots", "No bookings made.")
def refresh():
    entry.delete(0, tk.END)

input_button=tk.Button(win,text="Enter",command=getFields)
input_button.pack(pady=10)
menubar=tk.Menu(win)
win.config(menu=menubar)
filem=tk.Menu(menubar,tearoff=0)
signm=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=filem)
menubar.add_cascade(label="Sign_in",menu=signm)
filem.add_command(label="Help",command=open)
filem.add_command(label="New",command=refresh)
filem.add_separator()
filem.add_command(label="Exit",command=win.quit)
signm.add_command(label="admin",command=adminsign)

win.bind("<Return>",lambda event:getFields())
win.mainloop()