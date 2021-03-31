from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import *
import webbrowser
from tkcalendar import *
import sqlite3

# create connection to BMI database
cn = sqlite3.connect("bmil")
cr = cn.cursor()
# if there is no database here we created it

try:
    cr.execute(
        """CREATE TABLE report(id_inc INTEGER PRIMARY KEY, 
            Name TEXT (25),
            Weight INTEGER, 
            Height REAL,
            B_Date TEXT);"""
    )
    ID = 0
except:
    print("Table Already Exists")


Indextabl = 0
sqs = "SELECT * FROM report order by id_inc"  # query to select (all(*)) from db table ordered by id
cr.execute(sqs)  # executes the sqs to run the query
tbl = cr.fetchall()  # fetchall is a query result set and returns a list of tuples


def table():
    cr.execute("select * from report")
    return cr.fetchall()


if len(table()) == 0:
    ID = 0
else:
    ID = table()[-1][0] + 1

# def exit for window protocol and for exit menu
def Exit():
    cr.close()  # close the cursor
    cn.close()  # close the connection
    win.destroy()  # destroys the window


def is_num(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


# clearing al fields and results
def Clear(a=""):
    v1.set("")  # sets the stingvar of name entry ''(nothing)
    v2.set("")  # sets the stingvar of weight entry ''(nothing)
    v3.set("")  # sets the stingvar of height entry ''(nothing)
    Clear_Lb()  # change the color for the category result
    e1.focus()  # sets the name entry to enter data


# resetting result labels to be unshown
def Clear_Lb(a=""):
    lb11.config(text="     ")
    lb12.config(fg="lightgray")
    lb13.config(fg="lightgray")
    lb14.config(fg="lightgray")
    lb15.config(fg="lightgray")
    lb17.config(fg="lightgray")
    lb18.config(fg="lightgray")


# saving every thing to database and checks if any field is empty or not
def Save(a=""):
    if (not is_num(e2.get())) or float(e2.get()) <= 0:
        # checks if weight entry isn't a number or float
        e2.focus()  # puts the mouse in the weight entry
        v2.set("")  # sets nothing in the weight entry
        return

    if (not is_num(e3.get())) or float(e2.get()) <= 0:
        # checks if height entry isn't a number or float
        e3.focus()  # puts the mouse in the height entry
        v3.set("")  # sets nothing in the height entry
        return
    d2 = datetime.strptime(
        e4.get(), "%d/%m/%Y"
    )  # strptime() method creates a datetime object from the given string
    if todaydat <= d2:  # if today date is less than or equal to date time of now
        messagebox.showerror(
            "Update", "Date should be < System date"
        )  # shows messagebox
        return False
    Calcul()  # calculates the gives height and weight
    quest = messagebox.askyesno(
        "Save", "Do you want to save data ?"
    )  # asks yes or no if you really want to save
    if quest == True:  # if quest = yes then ...
        global ID
        sql = "INSERT INTO report(id_inc,Name,Weight,Height,B_Date) VALUES (%d, '%s', %s, %s, '%s');"
        x = (
            ID,
            e1.get(),
            e2.get(),
            e3.get(),
            d2,
        )  # gets the name,weight,height,dateentry entries
        cr.execute(sql % x)
        cn.commit()
        ID += 1

    Clear()  # clears all fields


# updates any record in database (getting it through name while clicking to view one and you can update the name)
def Update(a=""):
    if (not is_num(e2.get())) or float(e2.get()) <= 0:
        # checks if weight entry isn't number or float
        e2.focus()  # puts the mouse in the weight entry
        v2.set("")  # sets the weight entry string nothing
        return

    if (not is_num(e3.get())) or float(e2.get()) <= 0:
        # checks if height entry isn't number or float
        e3.focus()  # puts the mouse in the height entry
        v3.set("")  # sets the height entry string nothing
        return

    d2 = datetime.strptime(
        e4.get(), "%d/%m/%Y"
    )  # strptime() method creates a datetime object from the given string
    print(e4.get())
    if todaydat <= d2:  # checks if today date is less than or equal to date time of now
        messagebox.showerror(
            "Update", "Date should be < System date"
        )  # shows messagebox
        return False
    Calcul()  # calculates the current entered data of weight and height
    quest = messagebox.askyesno(
        "Update", "Sure to update data ?"
    )  # asks yes or no if you really want to update
    if quest == True:  # if quest = yes then...
        sq = "update report set Weight=%s, Height=%s, B_Date='%s' where Name='%s'"  # updates the current data entered where name = name entered
        x = (
            e2.get(),
            e3.get(),
            d2,
            e1.get(),
        )
        # gets weight,height,dateentry and name entry
        print(x)
        cr.execute(sq % x)  # execute the sq query and the x variable
        cn.commit()  # make changes in the database

    Clear()  # clearing all data in the fields


# gets the height and weight entry and calculate it and checks if height or weight is empty and if contains negative num
def Calcul(a=""):
    Clear_Lb()  # runs the clear_lb function whick cofigure the foreground of the category to be unshown

    if (is_num(e2.get())) and float(
        e2.get()
    ) > 0:  # checks if weight entry is number and float
        w = float(e2.get())  # gets the float of the weight
    else:  # if weight entry isn't number (float)
        e2.focus()  # puts the mouse in the weight entry
        v2.set("")  # sets nothing in the weight entry string
        return

    if (is_num(e3.get())) and float(
        e3.get()
    ) > 0:  # checks if height entry is number and float
        h = float(e3.get())  # gets the float of the height
    else:  # if height entry isn't number (float)
        e3.focus()  # puts the mouse in the height entry
        v3.set("")  # sets nothing in the height entry string
        return

    r = float(w / (h ** 2))  # bmi calculation (weight / height*height)

    lb11.config(text=str(round(r, 2)))  # gives you the result of the calculation
    # if results
    if r < 18.5:
        lb12.config(fg="red")
        lb18.config(fg="red")
    elif 18.5 <= r < 25:
        lb13.config(fg="red")
        lb17.config(fg="red")
    elif 25 <= r < 30:
        lb14.config(fg="red")
        lb18.config(fg="red")
    else:
        lb15.config(fg="red")
        lb18.config(fg="red")


# view all records from database in a listbox ordereb by name and you can view or delete any record
def VAll(a=""):
    global ls1  # globaling the list box
    win2 = Tk()  # new window for view all
    win2.geometry("720x400")  # geomatry for view all window
    win2.title("View All Patient BMI")  # title for view all window

    y = [
        "ID",
        "Name",
        "Weight",
        "Height",
        "Bith Date",
        "BMI",
        "Healthy",
    ]  # titles for database records
    s1 = "{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}".format(
        y[0], y[1], y[2], y[3], y[4], y[5], y[6]
    )  # making spaces between fields
    lb30 = Label(
        win2, text=s1, bg="lightblue", font=("courier", 10)
    )  # label for spaces for titles with background

    fr1 = Frame(win2)  # creating a frame to put the list box
    sb1 = Scrollbar(fr1)  # scroll bar for the list box to see all records
    ls1 = Listbox(
        fr1, yscrollcommand=sb1.set, font=("courier", 10), width=80, height=15
    )  # list box to put records in

    sq = "select * from report ORDER by Name"  # query for selecting all(*) from table ordered by name
    cr.execute(sq)  # executes the current query
    rd = cr.fetchall()
    # shows all rows of a query result set and returns a list of tuples

    for row in rd:
        # doing for loop for putting bmi result and if healthy or not without saving in into database
        w = int(row[2])  # taking the integer of weight
        h = float(row[3])  # taking the float of height
        r = float(w / (h ** 2))  # result (bmi)
        if 18.5 <= r < 25:
            ht = "Yes"  # healthy = yes
        else:
            ht = "No"  # healthy = no

        s2 = "{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}".format(
            row[0], row[1], row[2], row[3], str(row[4]), round(r, 2), ht
        )  # formatting with spaces to print bmi result and if healthy without saving to db
        ls1.insert(END, s2)  # insert the data of the current format

    sb1.config(command=ls1.yview)
    lb30.place(x=30, y=30)
    fr1.place(x=30, y=60)
    ls1.pack(side=LEFT)
    sb1.pack(side=LEFT, fill=Y)
    button = Button(
        win2, text="Delete it", bg="red", width=20, command=delete_selected
    ).place(x=200, y=350)
    # delete any selected record
    button1 = Button(
        win2, text="View it", bg="green", width=20, command=lambda: view_selected(win2)
    ).place(x=400, y=350)
    # view any selected record

    win2.mainloop()


# get's the name you entered and printing the data on the fields place by place if record exists and checks if exist
def VOne(a=""):
    Clear_Lb()  # runs the clear_lb function which configure the category labels lightblue to be unshown
    if e1.get() == "":  # if name entry is empty
        messagebox.showinfo("VOne", "please enter name")  # shows message box
    else:  # if it is not empty then ...
        sq = "Select * from report where Name = '%s';"  # query to view(select) all entered data (refer to name entered)
        cr.execute(
            sq % e1.get()
        )  # executes the current query and getting the name entry
        rd = (
            cr.fetchall()
        )  # shows all rows of a query result set and returns a list of tuples
        for row in rd:
            for j in range(len(row)):
                v2.set(row[2])  # sets height record in the height entry
                v3.set(row[3])  # sets weight record in the weight entry
                e4.set_date(
                    datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
                )  # sets date record in the date entry
        Calcul()  # calculates the current data entered


# get's the name you entered and delete it if exists
def Delete(a=""):
    if e1.get() == "":  # checks if name is empty
        messagebox.showinfo("Delete", "Please enter the Name")  # shows message box
    else:  # if name isn't empty
        try:
            sq = "Select * from report where Name = '%s';"  # selects all data in the table where name equal name entry
            cr.execute(sq % e1.get())
            # executes the current query and getting the value of name entry
            nam = cr.fetchone()[
                1
            ]  # retrieves the next row of a query result set and returns a single sequence
            if e1.get() == nam:  # if name exists in the database then...
                sq = "Delete from report where Name = '%s'"  # deletes the record from database where name = value of name entry
                cr.execute(
                    sq % e1.get()
                )  # executes the current query and get's the value of name entry
                cn.commit()  # makes changes in the database
                messagebox.showinfo("Delete", "One Record Removed")  # shows message box
                Clear()  # clears all fields
        except:  # if name doesn't exists
            messagebox.showinfo("Delete", "Name not found")  # shows message box
            v1.set("")  # sets name empty
            e1.focus()  # put the mouse in the name entry


# prints first record place by place
def Frst():
    global Indextabl
    try:
        cr.execute(
            "SELECT * FROM report ORDER BY id_inc limit 1 "
        )  # query to select 1 record oredered bi id
        for rec in cr:
            for j in range(len(rec)):
                v1.set(rec[1])  # sets name in the name entry
                v2.set(rec[2])  # sets weight in the weight entry
                v3.set(rec[3])  # sets height in the height entry
                e4.set_date(datetime.strptime(rec[4], "%d/%m/%y"))
                btP["state"] = "disabled"  # if no more records disable the button
                btN[
                    "state"
                ] = "normal"  # normal button will be stated if there is records
                Indextabl = 1
                ctr = str(Indextabl) + "/" + str(len(tbl) - 1)  # for pagination
                lb20.config(text=ctr)
        Calcul()  # calculates the current data on the height and weight fields
    except:
        messagebox.showinfo("First", " No records was found ")  # shows messagebox


# prints last record place by place
def Lst():
    global Indextabl
    try:
        cr.execute(
            "SELECT * FROM report ORDER BY id_inc DESC LIMIT 1 "
        )  # query to select last record ordered by id
        for rec in cr:
            for j in range(len(rec)):
                v1.set(rec[1])  # sets name in the name entry
                v2.set(rec[2])  # sets weight in the weight entry
                v3.set(rec[3])  # sets height in the height entry
                e4.set_date(rec[4])  # sets date in the date entry
                btN["state"] = "disabled"  # if no records disable the button
                btP[
                    "state"
                ] = "normal"  # normal button will be stated if there is records
                Indextabl = len(tbl) - 1
                ctr = (
                    str(Indextabl) + "/" + str(len(tbl) - 1)
                )  # for counting (pagination)
                lb20.config(text=ctr)
        Calcul()  # calculates the current data on the height and weight fields
    except:
        messagebox.showwarning("Last", " No records was found ")  # shows message


# prints any record record place by place
def Prntdata(r):
    v1.set(r[1])  # sets data to name entry
    v2.set(r[2])  # sets data to weight entry
    v3.set(r[3])  # sets data to height entry
    e4.set_date(
        datetime.strptime(r[4], "%Y-%m-%d %H:%M:%S")
    )  # sets date to date time entry
    Calcul()  # calculates the current height and weight
    print(Indextabl)  # prints number of record in the table


# gives you all records ordered by the id(+1)
def Nxt():
    sqs = "SELECT * FROM report order by id_inc"  # selects all records from db table ordered by id
    cr.execute(sqs)  # executes the current query
    tbl = (
        cr.fetchall()
    )  # prints all rows of a query result set and returns a list of tuples

    global Indextabl
    if Indextabl < len(tbl) - 1:
        Indextabl += 1
    btP["state"] = "normal"  # if there is data set button normal
    if Indextabl == len(tbl) - 1:
        btN["state"] = "disabled"  # the no more data set button disabled
    Prntdata(tbl[Indextabl - 1])  # prints the current data in fields
    ctr = str(Indextabl) + "/" + str(len(tbl) - 1)  # shows pagination
    lb20.config(text=ctr)


# gives you all records ordered by id(-1)
def Prvs():
    sqs = "SELECT * FROM report order by id_inc"  # selects all records from db table ordered by id
    cr.execute(sqs)  # executes the current query
    tbl = (
        cr.fetchall()
    )  # prints all rows of a query result set and returns a list of tuples

    global Indextabl
    if Indextabl > 0:
        Indextabl -= 1
        Prntdata(tbl[Indextabl])
        ctr = str(Indextabl) + "/" + str(len(tbl) - 1)
        lb20.config(text=ctr)
    if Indextabl <= 1:
        btP["state"] = "disabled"  # the no more data set button disabled
    if btN["state"] == "disabled":
        btN["state"] = "normal"


# help menu
def help_me():
    window = Tk()
    window.title("Help?")
    window.geometry("400x200")
    label = Label(
        window, text="Need to improve your health?", font=("Tahoma", 19, "bold")
    )
    label.pack()
    label1 = Label(
        window,
        text="Are you obese, underweight or  overweight? want to improve your health?",
    )
    label1.pack()
    label2 = Label(
        window,
        text="Click here",
        font=("calibiri", 20, "bold"),
        cursor="hand2",
        fg="blue",
    )
    label2.pack()
    label2.bind(
        "<Button-1>",
        lambda e: click_me(
            "https://www.healthline.com/nutrition/18-foods-to-gain-weight#TOC_TITLE_HDR_2"
        ),
    )
    window.mainloop()


# refer to help_me menu
def click_me(url):
    webbrowser.open_new(url)


# deletes any record selected in the view all window list
def delete_selected():
    id = ls1.get(ANCHOR)[:7].strip()
    cr.execute("delete from report where id_inc=%s" % id)
    cn.commit()
    ls1.delete(ANCHOR)


# view any record selected in the view all window list
def view_selected(win: Tk):
    id = ls1.get(ANCHOR)[:7].strip()
    cr.execute("select * from report Where id_inc=%s " % id)
    z = cr.fetchall()
    for row in z:
        for j in range(len(row)):
            v1.set(row[1])
            win.destroy()
            return VOne()


# white mode in the menu colors
def test():
    global labels
    global buttons
    global entries
    for i in labels + entries + buttons:
        i.config(bg="white", fg="black")
    for o in labels2:
        o.config(bg="white", fg="lightgray")


def white_red():
    win.config(bg="white")
    for i in labels + entries + buttons:
        i.config(fg="#cc0005", bg="white")
    for o in labels2:
        o.config(bg="white", fg="lightgray")


def white_gray():
    global labels
    global buttons
    global entries
    for i in labels + entries + buttons:
        i.config(bg="white", fg="gray")
    for o in labels2:
        o.config(bg="white", fg="lightgray")


def dark_red():
    e4.config({"foreground": "red"})
    win.config(bg="black")
    for i in labels + entries + buttons:
        i.config(fg="red", bg="black")
    for o in labels2:
        o.config(bg="black", fg="black")


def brown_yello():
    win.config(bg="brown")
    for i in labels + entries + buttons:
        i.config(fg="yellow", bg="brown")
    for o in labels2:
        o.config(bg="brown", fg="brown")


# menu themes
def default():
    s.theme_use("default")


def clam():
    s.theme_use("clam")


def alt():
    s.theme_use("alt")


def classic():
    s.theme_use("classic")


def about():
    messagebox.messagebox.showinfo(
        "About Bmi",
        "Body mass index (BMI) is a measure of body fat based on height and weight that applies to adult men and women",
    )


# it searches if there is a record(refer to the name entered)
def search_table(x):
    cr.execute("SELECT * FROM report where Name like '%s%%'" % x)
    table = cr.fetchall()  # shows all rows in the db table and returns a list of tuple
    return table


##refer to search_table + design and showing records
def search():
    search_win = Tk()
    search_win.title("Result for your search")
    search_win.geometry("800x300")
    y = [
        "ID",
        "Name",
        "Weight",
        "Height",
        "Bith Date",
        "BMI",
        "Healthy",
    ]  # title for the records
    s1 = "{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}".format(
        y[0], y[1], y[2], y[3], y[4], y[5], y[6]
    )  # sets spaces between each field
    lb30 = Label(search_win, text=s1, bg="lightblue", font=("courier", 10))
    fr1 = Frame(search_win)
    sb1 = Scrollbar(fr1)
    ls1 = Listbox(
        fr1, yscrollcommand=sb1.set, font=("courier", 10), width=80, height=15
    )
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

        s2 = "{:^7}{:^25}{:^8}{:^8}{:^15}{:^8}{:^8}".format(
            row[0], row[1], row[2], row[3], str(row[4]), round(r, 2), ht
        )
        ls1.insert(END, s2)

    sb1.config(command=ls1.yview)
    lb30.place(x=30, y=30)
    fr1.place(x=30, y=60)
    ls1.pack(side=LEFT)
    sb1.pack(side=LEFT, fill=Y)
    keyword_entry = v1.get()
    my_result = search_table(keyword_entry)


win = Tk()
win.title("Body Mass Index")
win.geometry("620x420")
win.bind("<Control-x>", quit)  # for quitting in the menu bar
win.bind("<Control-s>", Save)  # for saving any record to db
win.bind("<Control-d>", Delete)  # for deleting any record in db
win.bind("<Control-B>", VAll)  # for viewing all records in db
win.bind("<Control-b>", VOne)  # fro viewing one record (checks name entry)
win.bind("<Control-u>", Update)  # for updating any record(checks name entry)
win.bind("<Control-r>", Calcul)  # for calculating height and weight
win.bind("<Control-q>", Clear)  # reseting all fields
s = ttk.Style()
menubar = Menu(win)
image = PhotoImage(file="../assets/exit.png")  # exit png
image1 = PhotoImage(file="../assets/about.png")  # about png
image2 = PhotoImage(file="../assets/theme.png")  # themes png
image3 = PhotoImage(file="../assets/save.png")  # save png
image4 = PhotoImage(file="../assets/delete.png")  # delete png
image5 = PhotoImage(file="../assets/improve.png")  # improve png
image6 = PhotoImage(file="../assets/viewall.png")  # view all png
image7 = PhotoImage(file="../assets/viewone.png")  # view one png
image8 = PhotoImage(file="../assets/update.png")  # update png
image9 = PhotoImage(file="../assets/calculate.png")  # calculate png
imag10 = PhotoImage(file="../assets/color.png")  # colors png
image10 = PhotoImage(file="../assets/clear.png")  # clear png
# menu bar commands and cascades
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
edit = Menu(menubar, tearoff=0)
help = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
submenu = Menu(edit, tearoff=0)
submenu2 = Menu(edit, tearoff=0)

filemenu.add_cascade(
    label="  Save                  Ctrl+S", image=image3, compound=LEFT, command=Save
)
filemenu.add_cascade(
    label="  Delete               Ctrl+D", image=image4, compound=LEFT, command=Delete
)
filemenu.add_cascade(
    label="  View one          Ctrl+b", image=image7, compound=LEFT, command=VOne
)
filemenu.add_cascade(
    label="  View all             Ctrl+shift+b",
    image=image6,
    compound=LEFT,
    command=VAll,
)

filemenu.add_separator()
edit.add_cascade(
    label="  Update             Ctrl+u", image=image8, compound=LEFT, command=Update
)
edit.add_cascade(
    label="Calculate           Ctrl+R", image=image9, compound=LEFT, command=Calcul
)
edit.add_cascade(
    label="Clear                  Ctrl+Q", image=image10, compound=LEFT, command=Clear
)
edit.add_separator()
edit.add_cascade(
    label="  Colors", image=image2, compound=LEFT, menu=submenu, underline=0
)
check1 = submenu.add_radiobutton(label="White mode", command=test)
check2 = submenu.add_radiobutton(label="White red mode", command=white_red)
check3 = submenu.add_radiobutton(label="white gray mode", command=white_gray)
check4 = submenu.add_radiobutton(label="Dark red mode", command=dark_red)
check5 = submenu.add_radiobutton(label="brown yellow mode", command=brown_yello)
edit.add_cascade(label="  Themes", image=imag10, compound=LEFT, menu=submenu2)
checkme = submenu2.add_radiobutton(label="default", command=default)
checkme1 = submenu2.add_radiobutton(label="clam", command=clam)
checkme2 = submenu2.add_radiobutton(label="alt", command=alt)
checkme3 = submenu2.add_radiobutton(label="classic", command=classic)
themes = [check1, check2, check3, check4]
menubar.add_cascade(label="help", menu=help)
help.add_cascade(
    label="improve your health?", image=image5, compound=LEFT, command=help_me
)
help.add_cascade(
    label="About bmi calculator", image=image1, compound=LEFT, command=about
)

filemenu.add_cascade(
    label="  Exit                    Ctrl+X", image=image, compound=LEFT, command=Exit
)
win.config(menu=menubar)


# labels
lb1 = Label(win, text="BMI CALCULATOR", font=("Arial", 20))  # bmi calculator label
lb2 = Label(win, text="Full Name")  # full name label
lb3 = Label(win, text="Weight in Kg")  # weight label
lb4 = Label(win, text="Height in m")  # height label
lb5 = Label(win, text="Date of Birth")  # date of birth label
# string vars
v1 = StringVar()  # for name entry
v2 = StringVar()  # weight entry
v3 = StringVar()  # height entry

e1 = Entry(win, textvariable=v1)  # name entry
e2 = Entry(win, textvariable=v2, justify="right")  # weight entry
e3 = Entry(win, textvariable=v3, justify="right")  # height entry

vd = date.today()
todaydat = datetime(vd.year, vd.month, vd.day)
e4 = DateEntry(
    win,
    width=12,
    borderwidth=2,
    day=vd.day,
    month=vd.month,
    year=vd.year,
    date_pattern="dd/mm/yyyy",
    maxdate=vd,
)  # date entry

bt1 = Button(win, text="New", fg="green", width=8, command=Clear)  # clear button
bt2 = Button(win, text="Save", fg="red", width=8, command=Save)  # save button
bt3 = Button(win, text="UpDate", fg="red", width=8, command=Update)  # update button
bt4 = Button(
    win, text="Calculate", fg="green", width=8, command=Calcul
)  # calculate button
bt5 = Button(win, text="View One", fg="green", width=8, command=VOne)  # view one button
bt6 = Button(win, text="View All", fg="green", width=8, command=VAll)  # view all button
bt7 = Button(win, text="Delete", fg="red", width=8, command=Delete)  # delete buttons
bt8 = Button(win, text="Last", fg="blue", width=8, command=Lst)  # last  button
bt9 = Button(win, text="First", fg="blue", width=8, command=Frst)  # first button
btP = Button(win, text="<<", fg="blue", width=8, command=Prvs)  # previous button
btN = Button(win, text=">>", fg="blue", width=8, command=Nxt)  # next button
sech = Button(win, text="Search", fg="green", width=8, command=search)  # search button
lb10 = Label(win, text="Your BMI is:")  # your bmi is label
lb11 = Label(win, text="      ", bg="white", relief=SUNKEN, font=("Arial", 10))
fr1 = LabelFrame(win, text="Your Category is", padx=20, pady=20)  # category label frame
# category results
lb12 = Label(
    fr1, fg="lightgray", text="You Are UnderWeight"
)  # under weight category label
lb13 = Label(fr1, fg="lightgray", text="You Are Normal")  # normal category label
lb14 = Label(
    fr1, fg="lightgray", text="You Are Over Weight"
)  # over weight category label
lb15 = Label(fr1, fg="lightgray", text="You Are Obese")  # obese category label
lb16 = Label(win, text="Healthy ? ")  # healthy label
lb17 = Label(win, fg="lightgray", text="Yes")  # yes label
lb18 = Label(win, fg="lightgray", text="No")  # no label
ctr = str(Indextabl) + "/" + str(len(tbl) - 1)  # pagination
lb20 = Label(
    win, text=ctr, bg="white", width=4, justify="center"
)  # label for pagination
labels = [
    lb1,
    lb2,
    lb3,
    lb4,
    lb5,
    lb10,
    lb11,
    lb16,
    lb20,
    fr1,
]  # for looping colors for labels
buttons = [
    bt1,
    bt2,
    bt3,
    bt4,
    bt5,
    bt6,
    bt7,
    bt8,
    bt9,
    btN,
    btP,
]  # for looping colors for buttont
labels2 = [lb12, lb13, lb14, lb15, lb17, lb18]  # for looping colors for labels(results)
entries = [e1, e2, e3]
# placing every thing
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
sech.place(x=240, y=75)
lb20.place(x=275, y=310)

fr1.place(x=350, y=120)
lb12.pack(anchor=CENTER)
lb13.pack(anchor=CENTER)
lb14.pack(anchor=CENTER)
lb15.pack(anchor=CENTER)
win.protocol(
    "WM_DELETE_WINDOW", Exit
)  # for while closing the window function exit will work
win.mainloop()