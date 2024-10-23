import sqlite3
import webbrowser
import tkinter as tk
from tkinter import messagebox
conn=sqlite3.connect('hall_booking.db')
cursor=conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
               user_id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_name TEXT NOT NULL
               );''')
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
win =tk.Tk()
win.title("CED Project 005")
win.geometry("400x300")
label=tk.Label(win,text="Welcome to room booking services!",font=("Arial",16))
whov = tk.StringVar(value=f"You are signed in as {who}")
labelwho=tk.Label(win,textvariable=whov,font=("Arial",16))
labelwho.pack(pady=10)
def adminsign():
    subwin=tk.Toplevel(win)
    subwin.geometry("300x200")
    subwin.title("signin")
    labelsw1=tk.Label(subwin,text="Sign in for admin privledge")
    labelsw1.pack(padx=10,pady=10)
    labelsw2=tk.Label(subwin,text="Enter the password")
    labelsw2.pack(padx=0,pady=10)
    entrysw=tk.Entry(subwin)
    entrysw.pack(pady=10)

    def getus():
        password=entrysw.get()
        if password=="1234":
            global who
            who="admin"
            whov.set(f"You are signed in as {who}")
            subwin.destroy()
            messagebox.showinfo("Signed in as admin","Welcome admin")  
        else:
            messagebox.showinfo("Incorrect Password","The Password is Incorrect")
            return
    button2=tk.Button(subwin,text="Enter",command=getus)
    button2.pack(pady=10)
    subwin.bind("<Return>",lambda event:getus())
#button = tk.Button(win,text="Click Me",command=onbc)
#button.pack(pady=20)
label.pack(pady=20)

def open():
    webbrowser.open("https://anmol02122005.github.io/CED-Project-/")

entry=tk.Entry(win,width=30)
entry.pack(pady=10,ipady=4)
def roomExists(buildingName:str,roomId:str):
    cursor.execute('SELECT * FROM HALLS WHERE buildingName = ? AND Room_No = ? ', (buildingName, int(roomId) ))  
    result=cursor.fetchone()
    if result is None:
        messagebox.showinfo("Invalid Room","Room is not available for booking or does not exists")
        return 0
    else:
        return 1
def authenticate():
    if who!="admin":
        messagebox.showinfo("Permission denied","You need admin priviledge to do that")
        return 0
    else:
        return 1
def processInstruction():
    if len(tokens) < 1: 
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
    elif tokens[0]=="delete"  and length==2:
        deleteTable(tokens[1])
    elif tokens[0]=="edit" and length==5:
        editRoom(tokens[1],tokens[2],int(tokens[3]),int(tokens[4]))
    else:
        messagebox.showinfo("Invalid Command","Please enter a valid command")
    entry.delete(0, tk.END)    
'''def combinedcommands(event=None):
    getFields()  
    getus()'''
def valid(val):
    try:
        return int(val)  
    except ValueError:
        messagebox.showerror("Invalid Input", f"'{val}' is not a valid integer.")
        return None

def run():
    valid(tokens[2])
    valid(tokens[3])
    valid(tokens[4])

def deleteTable(Table_name:str):
    if authenticate():
        try:
            cursor.execute(f'''DELETE FROM {Table_name}''')  
            conn.commit()
            messagebox.showinfo("Success", f"All records in '{Table_name}' deleted.")
        except sqlite3.OperationalError as t:
            messagebox.showerror("Error", f"Failed to delete table '{Table_name}': {t}")
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
            messagebox.showinfo("Success", f"Room {roomId} in {buildingName} added.")
        else:
            messagebox.showinfo("Duplicate entry", f"Room {roomId} in {buildingName} already exists.")
def removeRoom(buildingName:str,roomId:str):
    if authenticate():
        if roomExists(buildingName,roomId):
            cursor.execute('DELETE FROM HALLS WHERE buildingName = ? AND Room_No = ?', (buildingName, int(roomId)))
            conn.commit()
            messagebox.showinfo("Success", f"Room {roomId} in {buildingName} removed.") 
def reserveRoom(buildingName:str,roomId:str,startTime:int,endTime:int):
    if roomExists(buildingName,roomId):
        cursor.execute('SELECT * FROM booking WHERE buildingName= ? AND Room_No = ? AND (startTime < ? AND endTime > ?)',  (buildingName, int(roomId), endTime, startTime))
        result=cursor.fetchone()
        if result:
            messagebox.showinfo("Sorry","This slot is already booked")
        else:
            if 0<=startTime<24 and 0<=endTime<24:
                cursor.execute('INSERT INTO booking (buildingName, Room_No, startTime, endTime) VALUES (?, ?, ?, ?)', (buildingName, int(roomId), startTime, endTime))
                conn.commit()
                messagebox.showinfo("Success", f"Room {roomId} in {buildingName} booked from {startTime} to {endTime}.")
            else:
                messagebox.showinfo("Invalid Command", "Start and end times must be between 0 and 23.")
def editRoom(buildingName:str,roomId:str,startTime:int,endTime:int):
    cancelRoom(buildingName,roomId,startTime,endTime)
    reserveRoom(buildingName,roomId,startTime,endTime)
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
    cursor.execute('''select * from HALLS''')
    rooms = cursor.fetchall()
    if rooms:
        rooms_list = "\n".join([f"{room[0]}, {room[1]}" for room in rooms])
        messagebox.showinfo("Available Rooms", rooms_list)
    else:
        messagebox.showinfo("Available Rooms", "No rooms available.")
def signout():
    who="user"
def displayTimeSlots():
    cursor.execute('''select buildingName,Room_No,startTime, endTime from booking''')
    slots = cursor.fetchall()
    if slots:
        slots_list = "\n".join([f"Building: {slot[0]}, Room: {slot[1]}, Time: {slot[2]} to {slot[3]}" for slot in slots])
        messagebox.showinfo("Booked Time Slots", slots_list)
    else:
        messagebox.showinfo("Booked Time Slots", "No bookings made.")
def refresh():
    entry.delete(0, tk.END)

input_button=tk.Button(win,text="Enter",command=getFields)
input_button.pack(pady=10)
menubar=tk.Menu(win)
win.config(menu=menubar)
file_menu=tk.Menu(menubar,tearoff=0)
sign_menu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=file_menu)
menubar.add_cascade(label="Sign_in",menu=sign_menu)
file_menu.add_command(label="Help",command=open)
file_menu.add_command(label="New",command=refresh)
file_menu.add_separator()
file_menu.add_command(label="Exit",command=win.quit)
sign_menu.add_command(label="admin",command=adminsign)
sign_menu.add_command(label="signout",command=signout)
win.bind("<Return>",lambda event:getFields())
win.mainloop()