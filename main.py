from Tkinter import *
from ttk import Style
try:
    from PIL import ImageTK, Image
except ImportError:
    import ImageTk, Image
from db import *
import datetime as dt


class Api(object):

    """API Setting"""

    def __init__(self, api_file="api.txt"):
        """
        @param txt  A API filename (use api.txt) as a default
        """
        self.api_file = api_file
        fo = open(self.api_file, "r")
        self.api = StringVar()
        fo.seek(0)
        if fo.read(1):
            fo.seek(0)
            self.api.set(fo.read())
        fo.close()

    def set_api(self, value):
        """
        Save API Key to file
        @param value A user's API Key
        """
        fo = open(self.api_file, "w")
        fo.write(value)
        fo.close()
        self.api.set(value)

    def get_api(self):
        """Get User's API Key"""
        return self.api.get()


class Task(Frame):

    """Task card"""

    def __init__(self, parent, id, title, message, task_type, datetime, window):
        if dt.datetime.strptime(datetime, '%Y-%m-%d %H:%M:%S') > dt.datetime.now():
            Frame.__init__(self, parent, bg="white")
            self.title1 = Label(self, text=title, bg='white', justify=LEFT, wraplength=300, font="Arial 14")
            self.datetime1 = Label(self, text=datetime, bg='white', font="Arial 10")
            self.message1 = Label(self, text=message, bg="white", justify=LEFT, wraplength=300, font="Arial 10")
        else:
            Frame.__init__(self, parent)
            self.title1 = Label(self, text=title, justify=LEFT, wraplength=300, font="Arial 14")
            self.datetime1 = Label(self, text=datetime, font="Arial 10", fg="red")
            self.message1 = Label(self, text=message, justify=LEFT, wraplength=300, font="Arial 10")

        delete_img = ImageTk.PhotoImage(Image.open("del.png"))
        edit_img = ImageTk.PhotoImage(Image.open("edit.png"))

        self.id = id
        self.title = title
        self.message = message
        self.datetime = datetime
        self.task_type = task_type

        self.window = window

        self.delete = Label(self, image=delete_img, bg='#e74c3c', justify=LEFT)
        self.delete.image = delete_img
        self.edit = Label(self, image=edit_img, bg='#2ecc71', justify=LEFT)
        self.edit.image = edit_img

        self.delete.bind('<Button-1>', self.delete_task)
        self.delete.bind("<Enter>", lambda event, h=self.delete: h.configure(bg="#B83C30"))
        self.delete.bind("<Leave>", lambda event, h=self.delete: h.configure(bg="#e74c3c"))
        self.edit.bind('<Button-1>', self.edit_task)
        self.edit.bind("<Enter>", lambda event, h=self.edit: h.configure(bg="#25A65C"))
        self.edit.bind("<Leave>", lambda event, h=self.edit: h.configure(bg="#2ecc71"))

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
        self.window.new_task(self.task_type, data, 'Edit Task')



class App(Frame):

    """docstring for App"""

    def paste(self):
        """Override Paste Shortcut"""
        self.entry.event_generate('<Control-v>')

    def cut(self):
        """Override Cut Shortcut"""
        self.entry.event_generate('<Control-x>')

    def copy(self):
        """Override Copy Shortcut"""
        self.entry.event_generate('<Control-c>')

    def save(self):
        """Save User's API Key in Setting"""
        api = Api()
        api.set_api(self.api_entry.get())
        self.s.destroy()
        self.clear_frame()

    def setting(self):
        """Create Setting Window"""
        api = Api()
        val = StringVar()
        val.set(api.get_api())
        self.s = Toplevel(self, padx=10, pady=10)
        self.s.title("Update API Key")
        self.s.resizable(0, 0)

        self.api_label = Label(self.s, text="API Key")
        self.api_label.grid(row=0, column=0, sticky=W, ipady=10)
        self.api_entry = Entry(self.s, textvariable=val, width=40)
        self.api_entry.grid(row=0, column=1, columnspan=2, sticky=W + E, ipady=3)
        self.save_btn = Button(self.s, text="Save", padx=10, pady=5, command=self.save)
        self.save_btn.grid(row=1, column=0, columnspan=3, sticky=W + E, pady=5)

    def new_task(self, task_type, values=dict(), btn='Add Task'):
        """
        Create "Add a task" Window
        @param task_type Get type of task
                value A dict of task data (title, message, date, time)
                btn Text display in Button
        """
        if values == {}:
            values['title'] = StringVar().set('')
            values['message'] = StringVar().set('')
            values['date'] = StringVar()
            values['date'].set('2014-10-11')
            values['time'] = StringVar()
            values['time'].set('13:37')
        self.task_type = task_type

        self.t = Toplevel(self, padx=10, pady=10)
        self.t.title("Add a task")
        self.t.resizable(0, 0)

        self.title_label = Label(self.t, text="Title")
        self.title_label.grid(row=0, column=0, sticky=W, ipady=10)
        self.title = Entry(self.t, textvariable=values['title'])
        self.title.grid(row=0, column=1, columnspan=2, sticky=W + E, ipady=3)

        self.message_label = Label(self.t, text="Message")
        self.message_label.grid(row=1, column=0, sticky=W, ipady=10)
        self.message = Entry(self.t, textvariable=values['message'])
        self.message.grid(row=1, column=1, columnspan=2, sticky=W + E, ipady=3)

        self.datetime_label = Label(self.t, text="Datetime")
        self.datetime_label.grid(row=2, column=0, sticky=W, ipady=10)
        self.datetime_date = Entry(self.t, textvariable=values['date'])
        self.datetime_date.grid(row=2, column=1, sticky=W, ipady=3)
        self.datetime_time = Entry(self.t, textvariable=values['time'])
        self.datetime_time.grid(row=2, column=2, sticky=W, ipady=3)

        self.l = Button(self.t, padx=10, pady=5)
        self.l["text"] = btn
        self.l["command"] = self.get_new_task
        self.l.grid(row=3, columnspan=3, sticky=N + E + W + S, pady=5)

    def get_new_task(self):
        """Get data from "Add a task" Window and add task"""
        title = self.title.get()
        message = self.message.get()
        task_type = self.task_type
        date = self.datetime_date.get()
        time = self.datetime_time.get()

        self.add_task(title, message, task_type, date, time)
        self.t.destroy()

    def create_widget(self):
        """Create main window program"""
        self.row = 0

        self.columnconfigure(0, pad=0)
        self.columnconfigure(1, pad=0)
        self.columnconfigure(2, pad=0)
        self.columnconfigure(3, pad=0)

        self.new_text = Button(self.frame, padx=25, pady=10, bg="white", borderwidth=0)
        self.new_text["text"] = "Text"
        self.new_text["command"] = lambda: self.new_task("text")
        self.new_text.bind("<Enter>", lambda event, h=self.new_text: h.configure(bg="#cccccc"))
        self.new_text.bind("<Leave>", lambda event, h=self.new_text: h.configure(bg="#ffffff"))
        self.new_text.grid(row=0, sticky=N + S + E + W, column=0, pady=(0, 2))

        self.new_list = Button(self.frame, padx=25, pady=10, bg="white", borderwidth=0)
        self.new_list["text"] = "List"
        self.new_list["command"] = lambda: self.new_task("list")
        self.new_list.bind("<Enter>", lambda event, h=self.new_list: h.configure(bg="#cccccc"))
        self.new_list.bind("<Leave>", lambda event, h=self.new_list: h.configure(bg="#ffffff"))
        self.new_list.grid(row=0, sticky=N + S + E + W, column=1, pady=(0, 2))

        self.new_link = Button(self.frame, padx=25, pady=10, bg="white", borderwidth=0)
        self.new_link["text"] = "Link"
        self.new_link["command"] = lambda: self.new_task("link")
        self.new_link.bind("<Enter>", lambda event, h=self.new_link: h.configure(bg="#cccccc"))
        self.new_link.bind("<Leave>", lambda event, h=self.new_link: h.configure(bg="#ffffff"))
        self.new_link.grid(row=0, sticky=N + S + E + W, column=2, pady=(0, 2))

        self.new_file = Button(self.frame, padx=25, pady=10, bg="white", borderwidth=0)
        self.new_file["text"] = "File"
        self.new_file["command"] = lambda: self.new_task("file")
        self.new_file.bind("<Enter>", lambda event, h=self.new_file: h.configure(bg="#cccccc"))
        self.new_file.bind("<Leave>", lambda event, h=self.new_file: h.configure(bg="#ffffff"))
        self.new_file.grid(row=0, sticky=N + S + E + W, column=3, pady=(0, 2))

        self.pack()

        self.get_task()

    def clear_frame(self):
        """Clear main window and refresh task"""
        for child in self.frame.winfo_children():
            child.destroy()
        self.create_widget()

    def create_frame(self, title, message, task_type, datetime, id=''):
        """Create Task Frame on main window"""
        self.row += 1
        Task(self.frame, id, title, message, task_type, datetime, self).grid(row=self.row, columnspan=4, sticky=W + E, pady=(0, 2))

    def get_task(self):
        """Get All User's Task"""
        api = Api()
        self.api = api.get_api()
        for row in self.sqlite.get_task(self.api):
            print row
            self.create_frame(row[1], row[2], row[3], row[4], id=row[0])
        print '---------------------------------------------------------------'

    def add_task(self, title, message, task_type, date, time):
        """Add task to database"""
        print title, message, task_type, date, time
        print '---------------------------------------------------------------'

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

        self.create_frame(title, message, task_type, date + " " + time + ":00", task_id)

    def OnFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def __init__(self, master=None):
        """create database connection and init App frame and Canvas"""

        self.mysql = MySQL()
        self.sqlite = SQLite('db.db')

        api = Api()
        self.api = api.get_api()

        Frame.__init__(self, master)

        Style().configure('.', font=('Arial', 10))

        self.canvas = Canvas(master, borderwidth=0, background="white", width=320)
        self.frame = Frame(self.canvas, background="#cccccc")
        self.vsb = Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both")
        self.canvas.create_window((0, 0), window=self.frame, anchor=NW)

        self.frame.bind("<Configure>", self.OnFrameConfigure)

        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Setting", command=self.setting)
        filemenu.add_command(label="Quit", command=quit)
        self.menubar.add_cascade(label="File", menu=filemenu)

        self.create_widget()


def main():
    """init program"""
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("320x600+150+150")
    root.title('To-do Bullet (Dev.)')

    app = App(master=None)
    app.mainloop()
    root.destroy()

main()

