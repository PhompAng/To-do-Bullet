from Tkinter import *
from ttk import Button, Style
from datetime import date, datetime, timedelta
import MySQLdb
#from pushbullet import PushBullet


class App(Frame):

    """docstring for App"""

    def newwin(self):
        self.t = Toplevel(self)
        self.title = Entry(self.t)
        self.title.pack()
        self.message = Entry(self.t)
        self.message.pack()
        self.l = Button(self.t)
        self.l["text"] = self.row
        self.l["command"] = self.createFrame
        #self.l["command"] = self.addTask
        self.l.pack()

    def crateWidgets(self):

        Style().configure("TButton", padding=(0, 3, 0, 3), font='serif 10')

        self.columnconfigure(0, pad=0)
        self.columnconfigure(1, pad=0)
        self.columnconfigure(2, pad=0)
        self.columnconfigure(3, pad=0)

        self.rowconfigure(0, pad=5, minsize=30)
        self.rowconfigure(1, pad=5, minsize=30)

        #self.rowconfigure(2, pad=5, minsize=30)

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

    def createFrame(self):
        self.row += 1
        self.f1 = Frame(self.frame, bg="red", height=100)
        self.title1 = Label(self.frame, text=self.title.get())
        self.message1 = Label(self.frame, text=self.message.get())
        self.f1.grid(row=self.row, columnspan=4)
        self.title1.place(in_=self.f1)
        self.message1.place(in_=self.f1)

    def addTask(self):
        self.db = MySQLdb.connect(host="",  # your host, usually localhost
                                  user="",  # your username
                                  passwd="",  # your password
                                  db="")  # name of the data base
        self.cur = self.db.cursor()
        self.data = {
            'api': self.api,
            'title': self.title.get(),
            'message': self.message.get(),
            'link': 'https://www.google.com',
            'time': datetime.now(),
        }
        self.add = ("INSERT INTO push "
                    "(api, title, message, link, time) "
                    "VALUES (%(api)s, %(title)s, %(message)s, %(link)s, %(time)s)")
        self.cur.execute(self.add, self.data)
        self.db.commit()
        self.createFrame()

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, master=None):
        self.api = ''
        self.row = 1

        Frame.__init__(self, master)
        self.canvas = Canvas(master, borderwidth=0, background="#ffffff")
        self.frame = Frame(self.canvas, background="#ff0000")
        self.vsb = Scrollbar(
            master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both")
        self.canvas.create_window((0, 0), window=self.frame, tags="self.frame")

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.crateWidgets()


def main():
    root = Tk()
    #root.resizable(width=FALSE, height=FALSE)
    root.geometry("400x600")
    app = App(master=None)
    app.mainloop()
    root.destroy()

main()
