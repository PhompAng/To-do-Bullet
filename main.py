from Tkinter import *
from ttk import Button, Style
from datetime import date, datetime, timedelta
import MySQLdb
import sqlite3
#from pushbullet import PushBullet


class App(Frame):

    """docstring for App"""

    def newwin(self):
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
        self.datetime_time_placehold.set("14:00")
        self.datetime_time = Entry(
            self.t, textvariable=self.datetime_time_placehold)
        self.datetime_time.grid(row=2, column=2, sticky=W)

        self.l = Button(self.t)
        self.l["text"] = self.row
        #self.l["command"] = self.createFrame
        self.l["command"] = self.addTask
        self.l.grid(row=3, columnspan=3, sticky=N + E + W + S)

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
        self.new_text["command"] = self.newwin

        self.new_text.grid(row=0, sticky=N + S + E + W, column=0)

        self.new_list = Button(self.frame)
        self.new_list["text"] = "List"
        self.new_list["command"] = self.newwin

        self.new_list.grid(row=0, sticky=N + S + E + W, column=1)

        self.new_link = Button(self.frame)
        self.new_link["text"] = "Link"
        self.new_link["command"] = self.newwin

        self.new_link.grid(row=0, sticky=N + S + E + W, column=2)

        self.new_file = Button(self.frame)
        self.new_file["text"] = "File"
        self.new_file["command"] = self.newwin

        self.new_file.grid(row=0, sticky=N + S + E + W, column=3)

        self.QUIT = Button(self.frame, text="quit", command=quit)
        self.QUIT.grid(row=1, columnspan=4, sticky=W + E)

        self.pack()

        self.getTask()

    def createFrame(self, title, message, datetime):
        self.row += 1
        self.f1 = Frame(self.frame, bg="white")
        self.f1.grid(row=self.row, columnspan=4, sticky=W + E)

        self.title1 = Label(
            self.frame, text=title, bg='white', justify=LEFT, font='serif 14', wraplengt=300)
        self.datetime1 = Label(
            self.frame, text=datetime, bg='white', font='serif 10')
        self.message1 = Label(
            self.frame, text=message, bg="white", justify=LEFT, font='serif 10', wraplengt=300)

        self.title1.pack(in_=self.f1, ancho=W, fill=Y)
        self.message1.pack(in_=self.f1, anchor=SW, fill=Y)
        self.datetime1.pack(in_=self.f1, anchor=SE)

    def getTask(self):
        self.cur.execute(
            "SELECT title, message, time FROM task WHERE api=%s", [self.api])
        for row in self.cur.fetchall():
            print row
            self.createFrame(row[0], row[1], row[2])

    def addTask(self):
        self.data = {
            'api': self.api,
            'title': self.title.get(),
            'message': self.message.get(),
            'link': 'https://www.google.com',
            'time': self.datetime_date.get() + ' ' + self.datetime_time.get() + ':00',
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

        self.createFrame(self.title.get(), self.message.get(
        ), self.datetime_date.get() + ' ' + self.datetime_time.get() + ':00')

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
            master, borderwidth=0, background="#ffffff", width=350)
        self.frame = Frame(self.canvas, background="#ff0000")
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
    app = App(master=None)
    app.mainloop()
    root.destroy()

main()
