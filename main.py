from Tkinter import *
from ttk import Button, Style
from db import *


class Api(object):

    """docstring for api"""

    def __init__(self):
        fo = open("api.txt", "r")
        self.api = StringVar()
        fo.seek(0)
        if fo.read(1):
            fo.seek(0)
            s = fo.read()
            self.api.set(s)
        fo.close()

    def set_api(self, value):
        fo = open("api.txt", "w")
        fo.write(value)
        fo.close()
        self.api.set(value)

    def get_api(self):
        return self.api.get()


class Task(Frame):

    """docstring for Task"""

    def __init__(self, parent, id, title, message, task_type, datetime, window):
        Frame.__init__(self, parent, bg="white")
        #self.f1.grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

        self.id = id
        self.title = title
        self.message = message
        self.datetime = datetime
        self.task_type = task_type

        self.window = window

        self.title1 = Label(
            self, text=str(id) + '. ' + title, bg='white', justify=LEFT, wraplength=300)
        self.datetime1 = Label(
            self, text=datetime, bg='white')
        self.message1 = Label(
            self, text=message + task_type, bg="white", justify=LEFT, wraplength=300)
        self.delete = Label(
            self, text="X", bg='red', fg="white", justify=LEFT)
        self.edit = Label(
            self, text="Edit", bg='yellow', justify=LEFT)

        self.delete.bind('<Button-1>', self.delete_task)
        self.edit.bind('<Button-1>', self.edit_task)

        self.delete.pack(in_=self, anchor=NE, side=RIGHT)
        self.edit.pack(in_=self, anchor=NE, side=RIGHT)
        self.title1.pack(in_=self, anchor=W, fill=Y)
        self.message1.pack(in_=self, anchor=SW, fill=Y)
        self.datetime1.pack(in_=self, anchor=SE)

    def delete_task(self, e):
        mysql = MySQL()
        sqlite = SQLite()
        if self.datetime == '':
            sqlite.delete_task(self.id)
        else:
            remote_id = sqlite.get_remote_id(self.id)
            mysql.delete_task(remote_id)
            sqlite.delete_task(self.id)
        self.destroy()

    def edit_task(self, e):
        data = {
            'title': StringVar(),
            'message': StringVar(),
            'date': StringVar(),
            'time': StringVar()
        }

        data['title'].set(self.title)
        data['message'].set(self.message)
        data['date'].set(self.datetime.split()[0])
        data['time'].set(self.datetime.split()[1][:-3])
        self.delete_task(e)
        self.window.newtext(self.task_type, data, 'Edit')



class App(Frame):

    """docstring for App"""

    def paste(self):
        self.entry.event_generate('<Control-v>')

    def cut(self):
        self.entry.event_generate('<Control-x>')

    def copy(self):
        self.entry.event_generate('<Control-c>')

    def save(self):
        api = Api()
        api.set_api(self.api_entry.get())
        self.s.destroy()
        self.clearFrame()

    def setting(self):
        api = Api()
        self.s = Toplevel(self)
        val = StringVar()
        val.set(api.get_api())
        self.api_label = Label(self.s, text="API Key")
        self.api_label.grid(row=0, column=0, sticky=W)
        self.api_entry = Entry(self.s, textvariable=val)
        self.api_entry.grid(row=0, column=1, columnspan=2, sticky=W + E)
        self.save_btn = Button(self.s, text="Save", command=self.save)
        self.save_btn.grid(row=1, column=0, columnspan=3, sticky=W + E)

    def newtext(self, task_type, values=dict(), btn='Add Task'):
        if values == {}:
            values['title'] = StringVar().set('')
            values['message'] = StringVar().set('')
            values['date'] = StringVar()
            values['date'].set('2014-10-11')
            values['time'] = StringVar()
            values['time'].set('13:37')
        self.task_type = task_type
        self.t = Toplevel(self)
        # self.t.geometry("300x200+120+120")

        self.title_label = Label(self.t, text="Title")
        self.title_label.grid(row=0, column=0, sticky=W)
        self.title = Entry(self.t, textvariable=values['title'])
        self.title.grid(row=0, column=1, columnspan=2, sticky=W + E)

        self.message_label = Label(self.t, text="Message")
        self.message_label.grid(row=1, column=0, sticky=W)
        self.message = Entry(self.t, textvariable=values['message'])
        self.message.grid(row=1, column=1, columnspan=2, sticky=W + E)

        self.datetime_label = Label(self.t, text="Datetime")
        self.datetime_label.grid(row=2, column=0, sticky=W)

        self.datetime_date = Entry(
            self.t, textvariable=values['date'])
        self.datetime_date.grid(row=2, column=1, sticky=W)

        self.datetime_time = Entry(
            self.t, textvariable=values['time'])
        self.datetime_time.grid(row=2, column=2, sticky=W)

        self.l = Button(self.t)
        self.l["text"] = btn
        self.l["command"] = self.get_newtext
        self.l.grid(row=3, columnspan=3, sticky=N + E + W + S)

    def get_newtext(self):
        title = self.title.get()
        message = self.message.get()
        task_type = self.task_type
        date = self.datetime_date.get()
        time = self.datetime_time.get()
        self.addTask(title, message, task_type, date, time)
        self.t.destroy()

    def crateWidgets(self):
        self.row = 1

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
        self.new_text["command"] = lambda: self.newtext("text")

        self.new_text.grid(row=0, sticky=N + S + E + W, column=0)

        self.new_list = Button(self.frame)
        self.new_list["text"] = "List"
        self.new_list["command"] = lambda: self.newtext("list")

        self.new_list.grid(row=0, sticky=N + S + E + W, column=1)

        self.new_link = Button(self.frame)
        self.new_link["text"] = "Link"
        self.new_link["command"] = lambda: self.newtext("link")

        self.new_link.grid(row=0, sticky=N + S + E + W, column=2)

        self.new_file = Button(self.frame)
        self.new_file["text"] = "File"
        self.new_file["command"] = lambda: self.newtext("file")

        self.new_file.grid(row=0, sticky=N + S + E + W, column=3)

        self.QUIT = Button(self.frame, text="quit", command=quit)
        self.QUIT.grid(row=1, columnspan=4, sticky=W + E)

        self.pack()

        self.getTask()

    def clearFrame(self):
        for child in self.frame.winfo_children():
            child.destroy()
        self.crateWidgets()

    def createFrame(self, title, message, task_type, datetime, id=''):
        self.row += 1
        # self.f1 = Frame(self.frame, bg="white")
        # self.f1.grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

        # self.title1 = Label(
        #     self.frame, text=title, bg='white', justify=LEFT, font='serif 14', wraplengt=300)
        # self.datetime1 = Label(
        #     self.frame, text=datetime, bg='white', font='serif 10')
        # self.message1 = Label(
        # self.frame, text=message+link, bg="white", justify=LEFT, font='serif
        # 10', wraplengt=300)

        # self.title1.pack(in_=self.f1, ancho=W, fill=Y)
        # self.message1.pack(in_=self.f1, anchor=SW, fill=Y)
        # self.datetime1.pack(in_=self.f1, anchor=SE)
        Task(self.frame, id, title, message, task_type, datetime, self).grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

    def getTask(self):
        api = Api()
        self.api = api.get_api()
        for row in self.sqlite.get_task(self.api):
            print row
            self.createFrame(row[1], row[2], row[3], row[4], id=row[0])

    def addTask(self, title, message, task_type, date, time):
        print title, message, task_type, date, time
        self.data = {
            'api': self.api,
            'title': title,
            'message': message,
            'task_type': task_type,
        }
        if date == "" and time == "":
            self.data['time'] = ""
            self.data['remote_id'] = 0
        else:
            self.data['time'] = date + ' ' + time + ':00'
            self.data['remote_id'] = self.mysql.insert_task(self.data)
        task_id = self.sqlite.insert_task(self.data)
        print task_id

        self.createFrame(title, message, task_type, date + " " + time + ":00", task_id)
        #self.clearFrame()

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, master=None):

        self.mysql = MySQL()
        self.sqlite = SQLite('db.db')

        api = Api()
        self.api = api.get_api()
        #self.api = ''

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

        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Setting", command=self.setting)
        self.menubar.add_cascade(label="File", menu=filemenu)

        self.crateWidgets()


def main():
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("370x600+150+150")

    # menubar = Menu(root)
    # menu = Menu(menubar, tearoff=0)
    # menu.add_command(label="Setting", command=run_setting)
    # menu.add_command(label="Exit", command=root.quit)

    # menubar.add_cascade(label="File", menu=menu)

    # root.config(menu=menubar)
    app = App(master=None)
    app.mainloop()
    root.destroy()

main()
