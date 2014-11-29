from Tkinter import *
from ttk import Button, Style
import MySQLdb
import sqlite3

class Task(Frame):
    """docstring for Task"""
    def __init__(self, parent, title, message, link, datetime):
        Frame.__init__(self, parent, bg="white")
        #self.f1.grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

        self.title1 = Label(
            self, text=title, bg='white', justify=LEFT, font='serif 14', wraplengt=300)
        self.datetime1 = Label(
            self, text=datetime, bg='white', font='serif 10')
        self.message1 = Label(
            self, text=message+link, bg="white", justify=LEFT, font='serif 10', wraplengt=300)

        self.title1.pack(in_=self, ancho=W, fill=Y)
        self.message1.pack(in_=self, anchor=SW, fill=Y)
        self.datetime1.pack(in_=self, anchor=SE)

class App(Frame):

    """docstring for App"""

    def newtext(self):
        self.t = Toplevel(self)
        # self.t.geometry("300x200+120+120")

        self.title_label = Label(self.t, text="Title")
        self.title_label.grid(row=0, column=0, sticky=W)
        self.title = Entry(self.t)
        self.title.grid(row=0, column=1, columnspan=2, sticky=W + E)

        self.message_label = Label(self.t, text="Message")
        self.message_label.grid(row=1, column=0, sticky=W)
        self.message = Entry(self.t)
        self.message.grid(row=1, column=1, columnspan=2, sticky=W + E)

        self.datetime_label = Label(self.t, text="Datetime")
        self.datetime_label.grid(row=2, column=0, sticky=W)

        self.datetime_date_placehold = StringVar()
        self.datetime_date_placehold.set("2014-10-11")
        self.datetime_date = Entry(
            self.t, textvariable=self.datetime_date_placehold)
        self.datetime_date.grid(row=2, column=1, sticky=W)

        self.datetime_time_placehold = StringVar()
        self.datetime_time_placehold.set("13:37")
        self.datetime_time = Entry(
            self.t, textvariable=self.datetime_time_placehold)
        self.datetime_time.grid(row=2, column=2, sticky=W)

        self.l = Button(self.t)
        self.l["text"] = self.row
        self.l["command"] = self.get_newtext
        self.l.grid(row=3, columnspan=3, sticky=N + E + W + S)

    def get_newtext(self):
        title=self.title.get()
        message=self.message.get()
        link=''
        date=self.datetime_date.get()
        time=self.datetime_time.get()
        self.addTask(title, message, link, date, time)

    def newlink(self):
        self.t = Toplevel(self)
        # self.t.geometry("300x200+120+120")

        self.title_label = Label(self.t, text="Title")
        self.title_label.grid(row=0, column=0, sticky=W)
        self.title = Entry(self.t)
        self.title.grid(row=0, column=1, columnspan=2, sticky=W + E)

        self.link_label = Label(self.t, text="Link")
        self.link_label.grid(row=1, column=0, sticky=W)
        self.link = Entry(self.t)
        self.link.grid(row=1, column=1, columnspan=2, sticky=W + E)

        self.datetime_label = Label(self.t, text="Datetime")
        self.datetime_label.grid(row=2, column=0, sticky=W)

        self.datetime_date_placehold = StringVar()
        self.datetime_date_placehold.set("2014-10-11")
        self.datetime_date = Entry(
            self.t, textvariable=self.datetime_date_placehold)
        self.datetime_date.grid(row=2, column=1, sticky=W)

        self.datetime_time_placehold = StringVar()
        self.datetime_time_placehold.set("13:37")
        self.datetime_time = Entry(
            self.t, textvariable=self.datetime_time_placehold)
        self.datetime_time.grid(row=2, column=2, sticky=W)

        self.l = Button(self.t)
        self.l["text"] = self.row
        self.l["command"] = self.get_newlink
        self.l.grid(row=3, columnspan=3, sticky=N + E + W + S)

    def get_newlink(self):
        title=self.title.get()
        message=''
        link=self.link.get()
        date=self.datetime_date.get()
        time=self.datetime_time.get()
        self.addTask(title, message, link, date, time)

    def crateWidgets(self):

        Style().configure("TButton", padding=(0, 3, 0, 3), font='serif 10')

        self.columnconfigure(0, pad=0)
        self.columnconfigure(1, pad=0)
        self.columnconfigure(2, pad=0)
        self.columnconfigure(3, pad=0)

        self.rowconfigure(0, pad=5, minsize=30)
        self.rowconfigure(1, pad=5, minsize=30)
        self.rowconfigure(2, pad=5, minsize=30)

        self.new_text = Button(self.frame)
        self.new_text["text"] = "Text"
        self.new_text["command"] = self.newtext

        self.new_text.grid(row=0, sticky=N + S + E + W, column=0)

        self.new_list = Button(self.frame)
        self.new_list["text"] = "List"
        self.new_list["command"] = self.newtext

        self.new_list.grid(row=0, sticky=N + S + E + W, column=1)

        self.new_link = Button(self.frame)
        self.new_link["text"] = "Link"
        self.new_link["command"] = self.newlink

        self.new_link.grid(row=0, sticky=N + S + E + W, column=2)

        self.new_file = Button(self.frame)
        self.new_file["text"] = "File"
        self.new_file["command"] = self.newtext

        self.new_file.grid(row=0, sticky=N + S + E + W, column=3)

        self.QUIT = Button(self.frame, text="quit", command=quit)
        self.QUIT.grid(row=1, columnspan=4, sticky=W + E)

        self.pack()

        self.getTask()

    def createFrame(self, title, message, link, datetime):
        self.row += 1
        # self.f1 = Frame(self.frame, bg="white")
        # self.f1.grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

        # self.title1 = Label(
        #     self.frame, text=title, bg='white', justify=LEFT, font='serif 14', wraplengt=300)
        # self.datetime1 = Label(
        #     self.frame, text=datetime, bg='white', font='serif 10')
        # self.message1 = Label(
        #     self.frame, text=message+link, bg="white", justify=LEFT, font='serif 10', wraplengt=300)

        # self.title1.pack(in_=self.f1, ancho=W, fill=Y)
        # self.message1.pack(in_=self.f1, anchor=SW, fill=Y)
        # self.datetime1.pack(in_=self.f1, anchor=SE)
        Task(self.frame, title, message, link, datetime).grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))


    def getTask(self):
        self.cur.execute(
            "SELECT title, message, link, time FROM task WHERE api=%s", [self.api])
        for row in self.cur.fetchall():
            print row
            self.createFrame(row[0], row[1], row[2], row[3])

    def addTask(self, title, message, link, date, time):
        print title, message, link, date, time
        self.data = {
            'api': self.api,
            'title': title,
            'message': message,
            'link': link,
            'time': date + ' ' + time + ':00',
        }
        self.add = ("INSERT INTO task "
                    "(api, title, message, link, time) "
                    "VALUES (%(api)s, %(title)s, %(message)s, %(link)s, %(time)s)")
        self.cur.execute(self.add, self.data)
        self.db.commit()

        self.sq3cur.execute("INSERT INTO task "
                            "(api_key, title, message, link, time) "
                            "VALUES (:api, :title, :message, :link, :time)", self.data)
        self.sq3.commit()

        self.createFrame(title, message, link, date + ' ' + time + ':00')

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, master=None):
        self.db = MySQLdb.connect(host="",  # your host, usually localhost
                                  user="",  # your username
                                  passwd="",  # your password
                                  db="")  # name of the data base
        self.cur = self.db.cursor()

        self.sq3 = sqlite3.connect('db.db')
        self.sq3cur = self.sq3.cursor()

        self.api = ''
        self.row = 1

        Frame.__init__(self, master)
        self.canvas = Canvas(
            master, borderwidth=0, background="#e5e5e5", width=350)
        self.frame = Frame(self.canvas, background="#b4b4b4")
        self.vsb = Scrollbar(
            master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both")
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.crateWidgets()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("370x600+150+150")

    menubar = Menu(root)
    menu = Menu(menubar, tearoff=0)
    menu.add_command(label="Setting")
    menu.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="File", menu=menu)

    root.config(menu=menubar)
    app = App(master=None)
    app.mainloop()
    root.destroy()

main()
