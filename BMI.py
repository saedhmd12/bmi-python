from tkinter.messagebox import *
from tkcalendar import *
import mysql.connector
from datetime import *
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import webbrowser
import tkinter.ttk as ttk
# create connection to BMI database
cn = mysql.connector.connect(host='localhost',
                             user='root',
                             password='',
                             database="BMI")
cr = cn.cursor()
# if there is no database here we created it
cr.execute("create database if not exists BMI")
# creating table in the bmi database (report)
cr.execute('''create table if not exists Report (
                        Id_Inc int auto_increment, 
                        Name varchar(25) not null,
                        Weight int,
                        Height float,
                        B_Date date,
                        primary key(Id_Inc))''')


Indextabl = 0
sqs = "SELECT * FROM BMI.Report order by id_inc"
cr.execute(sqs)
tbl = cr.fetchall()

#def exit for window protocol and for exit menu
def Exit():
    cr.close()
    cn.close()
    win.destroy()

# checking in name have number or not
def is_num(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True

#clearing al fields and results
def Clear(a=""):
    v1.set('')
    v2.set('')
    v3.set('')
    Clear_Lb()
    e1.focus()

#resetting result labels to be unshown
def Clear_Lb(a=""):
    lb11.config(text='     ')
    lb12.config(fg='lightgray')
    lb13.config(fg='lightgray')
    lb14.config(fg='lightgray')
    lb15.config(fg='lightgray')
    lb17.config(fg='lightgray')
    lb18.config(fg='lightgray')

#saving every thing to database and checks if any field is empty or not
def Save(a=""):
    if (not is_num(e2.get())) or float(e2.get()) <= 0:
        e2.focus()
        v2.set('')
        return

    if (not is_num(e3.get())) or float(e2.get()) <= 0:
        e3.focus()
        v3.set('')
        return
    d2 = datetime.strptime(e4.get(), '%d/%m/%Y')
    if todaydat <= d2:
        showerror('Update', 'Date should be < System date')
        return False
    Calcul()
    quest = messagebox.askyesno("Save", "Do you want to save data ?")
    if quest == True:
        sq = '''insert into BMI.Report (Name, Weight, Height, B_Date) 
               values(%s, %s, %s, %s) '''
        x = (e1.get(), e2.get(), e3.get(), d2)
        cr.execute(sq, x)
        cn.commit()
    Clear()

#updates any record in database (getting it through name while clicking to view one and you can update the name)
def Update(a=""):
    if (not is_num(e2.get())) or float(e2.get()) <= 0:
        e2.focus()
        v2.set('')
        return

    if (not is_num(e3.get())) or float(e2.get()) <= 0:
        e3.focus()
        v3.set('')
        return

    d2 = datetime.strptime(e4.get(), '%d/%m/%Y')
    if todaydat <= d2:
        showerror('Update', 'Date should be < System date')
        return False
    Calcul()
    quest = messagebox.askyesno("Update", "Sure to update data ?")
    if quest == True:
        sq = 'update BMI.Report set Weight=%s, Height=%s, B_Date=%s where Name=%s'
        x = (e2.get(), e3.get(), d2, e1.get())
        cr.execute(sq, x)
        cn.commit()

    Clear()

#gets the height and weight entry and calculate it and checks if height or weight is empty and if contains negative num
def Calcul(a=""):
    Clear_Lb()

    if (is_num(e2.get())) and float(e2.get()) > 0:
        w = float(e2.get())
    else:
        e2.focus()
        v2.set('')
        return

    if (is_num(e3.get())) and float(e3.get()) > 0:
        h = float(e3.get())
    else:
        e3.focus()
        v3.set('')
        return

    r = float(w / (h ** 2))

    lb11.config(text=str(round(r, 2)))

    if r < 18.5:
        lb12.config(fg='red')
        lb18.config(fg='red')
    elif 18.5 <= r < 25:
        lb13.config(fg='red')
        lb17.config(fg='red')
    elif 25 <= r < 30:
        lb14.config(fg='red')
        lb18.config(fg='red')
    else:
        lb15.config(fg='red')
        lb18.config(fg='red')

#view all records from database in a listbox ordereb by name and you can view or delete any record
def VAll(a=""):
    global ls1
    win2 = Tk()
    win2.geometry('720x400')
    win2.title("View All Patient BMI")

    y = ['ID', 'Name', 'Weight', 'Height', 'Bith Date', 'BMI', 'Healthy']
    s1 = '{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}'.format(y[0], y[1], y[2], y[3], y[4], y[5], y[6])
    lb30 = Label(win2, text=s1, bg='lightblue', font=('courier', 10))

    fr1 = Frame(win2)
    sb1 = Scrollbar(fr1)
    ls1 = Listbox(fr1, yscrollcommand=sb1.set, font=('courier', 10), width=80, height=15)

    sq = 'select * from BMI.Report ORDER by Name'
    cr.execute(sq)
    rd = cr.fetchall()

    for row in rd:
        w = int(row[2])
        h = float(row[3])
        r = float(w / (h ** 2))
        if 18.5 <= r < 25:
            ht = "Yes"
        else:
            ht = "No"

        s2 = '{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}'.format(row[0], row[1], row[2], row[3], str(row[4]), round(r, 2),
                                                            ht)
        ls1.insert(END, s2)

    sb1.config(command=ls1.yview)
    lb30.place(x=30, y=30)
    fr1.place(x=30, y=60)
    ls1.pack(side=LEFT)
    sb1.pack(side=LEFT, fill=Y)
    button = Button(win2, text='Delete it', bg = 'red', width = 20, command = delete_selected).place(x = 200, y = 350)
    button1 = Button(win2, text = 'View it',bg = 'green', width = 20,command = view_selected).place(x = 400 , y = 350)

    win2.mainloop()

#get's the name you entered and printing the data on the fields place by place if record exists and checks if exist
def VOne(a=""):
    Clear_Lb()
    if e1.get() == "":
        showinfo("VOne", "please enter name")
    else:
        sq = 'select * from BMI.Report where Name = %s'
        cr.execute(sq, (e1.get(),))
        rd = cr.fetchall()
        for row in rd:
            for j in range(len(row)):
                v2.set(row[2])
                v3.set(row[3])
                e4.set_date(row[4])
        Calcul()

#get's the name you entered and delete it if exists
def Delete(a=""):
    if e1.get() == "":
        showinfo("Delete", "Please enter the Name")
    else:
        try:
            sq = 'select * from BMI.Report where Name = %s'
            cr.execute(sq, (e1.get(),))
            nam = (cr.fetchone()[1])
            if e1.get() == nam:
                sq = 'Delete from BMI.Report where Name = %s'
                cr.execute(sq, (e1.get(),))
                cn.commit()
                showinfo("Delete", "One Record Removed")
                Clear()
        except:
            showinfo("Delete", "Name not found")
            v1.set('')
            e1.focus()

#prints first record place by place
def Frst():
    global Indextabl
    try:
        cr.execute("SELECT * FROM BMI.Report ORDER BY id_inc limit 1 ")
        for rec in cr:
            for j in range(len(rec)):
                v1.set(rec[1])
                v2.set(rec[2])
                v3.set(rec[3])
                e4.set_date(rec[4])
                btP['state'] = "disabled"
                btN['state'] = "normal"
                Indextabl = 1
                ctr = str(Indextabl) + '/' + str(len(tbl) - 1)
                lb20.config(text=ctr)
        Calcul()
    except:
        showinfo("First", " No records was found ")

#prints last record place by place
def Lst():
    global Indextabl
    try:
        cr.execute("SELECT * FROM BMI.Report ORDER BY id_inc DESC LIMIT 1 ")
        for rec in cr:
            for j in range(len(rec)):
                v1.set(rec[1])
                v2.set(rec[2])
                v3.set(rec[3])
                e4.set_date(rec[4])
                btN['state'] = "disabled"
                btP['state'] = "normal"
                Indextabl = len(tbl) - 1
                ctr = str(Indextabl) + '/' + str(len(tbl) - 1)
                lb20.config(text=ctr)
        Calcul()
    except:
        showwarning("Last", " No records was found ")

#prints any record record place by place
def Prntdata(r):
    v1.set(r[1])
    v2.set(r[2])
    v3.set(r[3])
    e4.set_date(r[4])
    Calcul()
    print(Indextabl)

#gives you all records ordered by the id(+1)
def Nxt():
    sqs = "SELECT * FROM BMI.Report order by id_inc"
    cr.execute(sqs)
    tbl = cr.fetchall()

    global Indextabl
    if Indextabl < len(tbl) - 1:
        Indextabl += 1
    btP['state'] = "normal"
    if Indextabl == len(tbl) - 1:
        btN['state'] = "disabled"
    Prntdata(tbl[Indextabl - 1])
    ctr = str(Indextabl) + '/' + str(len(tbl) - 1)
    lb20.config(text=ctr)

#gives you all records ordered by id(-1)
def Prvs():
    sqs = "SELECT * FROM BMI.Report order by id_inc"
    cr.execute(sqs)
    tbl = cr.fetchall()

    global Indextabl
    if Indextabl > 0:
        Indextabl -= 1
        Prntdata(tbl[Indextabl])
        ctr = str(Indextabl) + '/' + str(len(tbl) - 1)
        lb20.config(text=ctr)
    if Indextabl <= 1:
        btP['state'] = 'disabled'
    if btN['state'] == 'disabled':
        btN['state'] = 'normal'
#help menu
def help_me():
    window = Tk()
    window.title("Help?")
    window.geometry('400x200')
    label = Label(window,text = 'Need to improve your health?', font=('Tahoma',19,'bold'))
    label.pack()
    label1 = Label(window,text = 'Are you obese, underweight or  overweight? want to improve your health?')
    label1.pack()
    label2 = Label( window,text = 'Click here', font = ('calibiri', 20,'bold'), cursor= 'hand2', fg="blue")
    label2.pack()
    label2.bind('<Button-1>', lambda e: click_me("https://www.healthline.com/nutrition/18-foods-to-gain-weight#TOC_TITLE_HDR_2"))
    window.mainloop()
#refer to help_me menu
def click_me(url):
    webbrowser.open_new(url)

#deletes any record selected in the view all window list
def delete_selected():
    id = ls1.get(ANCHOR)[:7].strip()
    cr.execute('delete from BMI.report where id_inc=%s'%id)
    ls1.delete(ANCHOR)

#view any record selected in the view all window list
def view_selected():
    id = ls1.get(ANCHOR)[:7].strip()
    cr.execute('select * from report Where id_inc=%s '%id)
    z = cr.fetchall()
    for row in z:
        for j in range(len(row)):
            v1.set(row[1])
            VOne()

#white mode in the menu colors
def test():
    global labels
    global buttons
    global entries
    for i in labels+entries+buttons:
        i.config(bg = 'white', fg = 'black')
    for o in labels2:
        o.config(bg = 'white', fg = 'lightgray')

def white_red():
    win.config(bg = 'white')
    for i in labels+entries+buttons:
        i.config(fg='#cc0005', bg = 'white')
    for o in labels2:
        o.config(bg='white',fg='lightgray')
def white_gray():
    global labels
    global buttons
    global entries
    for i in labels+entries+buttons:
        i.config(bg = 'white', fg = 'gray')
    for o in labels2:
        o.config(bg = 'white', fg = 'lightgray')
def dark_red():
    e4.config({"foreground" :"red"})
    win.config(bg='black')
    for i in labels+entries+buttons:
        i.config(fg='red',bg='black')
    for o in labels2:
        o.config(bg='black',fg = 'black')
def brown_yello():
    win.config(bg = 'brown')
    for i in labels+entries+buttons:
        i.config(fg='yellow', bg = 'brown')
    for o in labels2:
        o.config(bg='brown',fg='brown')
#menu themes
def default():
    s.theme_use('default')
def clam():
    s.theme_use('clam')
def alt():
    s.theme_use('alt')
def classic():
    s.theme_use('classic')
def about():
    messagebox.showinfo("About Bmi","Body mass index (BMI) is a measure of body fat based on height and weight that applies to adult men and women")
#it searches if there is a record(refer to the name entered)
def search_table(x):
    cr.execute('SELECT * FROM BMI.report')
    table = cr.fetchall()
    results = tuple(row for row in table if row[1].startswith(x))
    return results
##refer to search_table + design and showing records
def search():
    search_win = Tk()
    search_win.title("Result for your search")
    search_win.geometry('800x300')
    y = ['ID', 'Name', 'Weight', 'Height', 'Bith Date', 'BMI', 'Healthy']
    s1 = '{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}'.format(y[0], y[1], y[2], y[3], y[4], y[5], y[6])
    lb30 = Label(search_win, text=s1, bg='lightblue', font=('courier', 10))
    fr1 = Frame(search_win)
    sb1 = Scrollbar(fr1)
    ls1 = Listbox(fr1, yscrollcommand=sb1.set, font=('courier', 10), width=80, height=15)
    search_phrase = v1.get()
    my_result = search_table(search_phrase)
    for row in my_result:
        w = int(row[2])
        h = float(row[3])
        r = float(w / (h ** 2))
        if 18.5 <= r < 25:
            ht = "Yes"
        else:
            ht = "No"

        s2 = '{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}'.format(row[0], row[1], row[2], row[3], str(row[4]), round(r, 2),
                                                            ht)
        ls1.insert(END, s2)

    sb1.config(command=ls1.yview)
    lb30.place(x=30, y=30)
    fr1.place(x=30, y=60)
    ls1.pack(side=LEFT)
    sb1.pack(side=LEFT, fill=Y)
    keyword_entry = v1.get()
    my_result = search_table(keyword_entry)

win = Tk()
win.title('Body Mass Index')
win.geometry('620x420')
win.bind('<Control-x>', quit)# for quitting in the menu bar
win.bind('<Control-s>', Save)# for saving any record to db
win.bind('<Control-d>', Delete)# for deleting any record in db
win.bind('<Control-B>', VAll)# for viewing all records in db
win.bind('<Control-b>', VOne)# fro viewing one record (checks name entry)
win.bind('<Control-u>', Update)# for updating any record(checks name entry)
win.bind('<Control-r>', Calcul)# for calculating height and weight
win.bind('<Control-q>', Clear)# reseting all fields 
s = ttk.Style()
menubar = tk.Menu(win)
image  = PhotoImage(file='exit.png')# exit png
image1 = PhotoImage(file='about.png')# about png
image2 = PhotoImage(file='theme.png')# themes png
image3 = PhotoImage(file='save.png')# save png
image4 = PhotoImage(file='delete.png')# delete png
image5 = PhotoImage(file='improve.png')# improve png
image6 = PhotoImage(file='viewall.png')#view all png
image7 = PhotoImage(file='viewone.png')# view one png
image8 = PhotoImage(file='update.png')#update png
image9 = PhotoImage(file='calculate.png')#calculate png
imag10 = PhotoImage(file='color.png')# colors png
image10= PhotoImage(file='clear.png')#clear png
#menu bar commands and cascades
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
edit = tk.Menu(menubar, tearoff=0)
help = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Edit', menu=edit)
submenu = tk.Menu(edit,tearoff = 0)
submenu2 = tk.Menu(edit,tearoff=0)

filemenu.add_cascade(label='  Save                  Ctrl+S', image = image3, compound=tk.LEFT, command=Save)
filemenu.add_cascade(label = '  Delete               Ctrl+D', image = image4, compound = tk.LEFT, command = Delete)
filemenu.add_cascade(label = '  View one          Ctrl+b', image = image7, compound = tk.LEFT, command = VOne)
filemenu.add_cascade(label = '  View all             Ctrl+shift+b', image = image6 , compound = tk.LEFT, command = VAll)

filemenu.add_separator()
edit.add_cascade(label = '  Update             Ctrl+u', image = image8 ,compound = tk.LEFT,command = Update)
edit.add_cascade(label = 'Calculate           Ctrl+R', image = image9, compound = tk.LEFT, command = Calcul)
edit.add_cascade(label = 'Clear                  Ctrl+Q', image = image10, compound = tk.LEFT, command = Clear)
edit.add_separator()
edit.add_cascade(label='  Colors', image = image2, compound= tk.LEFT,menu=submenu, underline=0)
check1 = submenu.add_radiobutton(label='White mode', command=test)
check2 = submenu.add_radiobutton(label = 'White red mode', command= white_red)
check3 = submenu.add_radiobutton(label='white gray mode',command = white_gray)
check4 = submenu.add_radiobutton(label = 'Dark red mode', command = dark_red)
check5 = submenu.add_radiobutton(label = 'brown yellow mode',command = brown_yello)
edit.add_cascade(label='  Themes', image = imag10, compound = tk.LEFT, menu = submenu2)
checkme = submenu2.add_radiobutton(label='default',command = default)
checkme1 = submenu2.add_radiobutton(label = 'clam',command = clam)
checkme2 = submenu2.add_radiobutton(label='alt',command = alt)
checkme3 = submenu2.add_radiobutton(label = 'classic',command = classic)
themes = [check1, check2, check3, check4]
menubar.add_cascade(label = 'help', menu = help)
help.add_cascade(label = 'improve your health?', image = image5, compound = tk.LEFT,command = help_me)
help.add_cascade(label = 'About bmi calculator',image = image1, compound = tk.LEFT, command = about)

filemenu.add_cascade(label='  Exit                    Ctrl+X', image = image, compound=tk.LEFT, command= Exit)
win.config(menu=menubar)


#labels
lb1 = Label(win, text='BMI CALCULATOR', font=('Arial', 20))#bmi calculator label
lb2 = Label(win, text='Full Name')# full name label
lb3 = Label(win, text='Weight in Kg')#weight label
lb4 = Label(win, text='Height in m')# height label
lb5 = Label(win, text='Date of Birth')#date of birth label
#string vars
v1 = StringVar()# for name entry
v2 = StringVar()# weight entry
v3 = StringVar()# height entry

e1 = Entry(win, textvariable=v1)# name entry
e2 = Entry(win, textvariable=v2, justify='right')#weight entry
e3 = Entry(win, textvariable=v3, justify='right')#height entry

vd = date.today()
todaydat = datetime(vd.year, vd.month, vd.day)
e4 = DateEntry(win, width=12, borderwidth=2, day=vd.day, month=vd.month, year=vd.year, date_pattern='dd/mm/yyyy', maxdate = vd)#date entry

bt1 = Button(win, text='New', fg='green', width=8, command=Clear)# clear button
bt2 = Button(win, text='Save', fg='red', width=8, command=Save)# save button
bt3 = Button(win, text='UpDate', fg='red', width=8, command=Update)# update button
bt4 = Button(win, text='Calculate', fg='green', width=8, command=Calcul)# calculate button
bt5 = Button(win, text='View One', fg='green', width=8, command=VOne)#view one button
bt6 = Button(win, text='View All', fg='green', width=8, command=VAll)#view all button
bt7 = Button(win, text='Delete', fg='red', width=8, command=Delete)#delete buttons
bt8 = Button(win, text='Last', fg='blue', width=8, command=Lst)# last  button
bt9 = Button(win, text='First', fg='blue', width=8, command=Frst)# first button
btP = Button(win, text='<<', fg='blue', width=8, command=Prvs)# previous button
btN = Button(win, text='>>', fg='blue', width=8, command=Nxt)# next button
sech= Button(win, text = 'Search', fg = 'green', width = 8,command = search)# search button
lb10 = Label(win, text='Your BMI is:')#your bmi is label
lb11 = Label(win, text='      ', bg='white', relief=SUNKEN, font=('Arial', 10))
fr1 =  LabelFrame(win, text='Your Category is', padx=20, pady=20)# category label frame
# category results
lb12 = Label(fr1, fg='lightgray', text='You Are UnderWeight')
lb13 = Label(fr1, fg='lightgray', text='You Are Normal')
lb14 = Label(fr1, fg='lightgray', text='You Are Over Weight')
lb15 = Label(fr1, fg='lightgray', text='You Are Obese')
lb16 = Label(win, text='Healthy ? ')
lb17 = Label(win, fg='lightgray', text='Yes')
lb18 = Label(win, fg='lightgray', text='No')
ctr =  str(Indextabl) + '/' + str(len(tbl) - 1)
lb20 = Label(win, text=ctr, bg='white', width=4, justify='center')
labels = [lb1,lb2,lb3,lb4,lb5,lb10,lb11,lb16,lb20,fr1]#for looping colors for labels
buttons = [bt1,bt2,bt3,bt4,bt5,bt6,bt7,bt8,bt9,btN,btP]#for looping colors for buttont
labels2 = [lb12,lb13,lb14,lb15,lb17,lb18]#for looping colors for labels(results)
#placing every thing
lb1.place(x=200, y=5)
lb2.place(x=20, y=80)
lb3.place(x=20, y=120)
lb4.place(x=20, y=160)
lb5.place(x=20, y=200)
lb10.place(x=350, y=80)
lb11.place(x=418, y=75)
lb16.place(x=453, y=75)
lb17.place(x=505, y=75)
lb18.place(x=527, y=75)

e1.place(x=100, y=80)
e2.place(x=100, y=120)
e3.place(x=100, y=160)
e4.place(x=100, y=200)

bt1.place(x=20, y=270)
bt2.place(x=20, y=310)
bt3.place(x=100, y=310)
bt4.place(x=260, y=270)
bt5.place(x=100, y=270)
bt6.place(x=180, y=270)
bt7.place(x=180, y=310)
bt8.place(x=20, y=350)
bt9.place(x=100, y=350)
btP.place(x=180, y=350)
btN.place(x=260, y=350)
sech.place(x = 240, y = 75)
lb20.place(x=275, y=310)

fr1.place(x=350, y=120)
lb12.pack(anchor=CENTER)
lb13.pack(anchor=CENTER)
lb14.pack(anchor=CENTER)
lb15.pack(anchor=CENTER)
win.protocol('WM_DELETE_WINDOW', Exit)# for while closing the window function exit will work
win.mainloop()