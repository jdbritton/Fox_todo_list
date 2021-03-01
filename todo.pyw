###############################################################################
# Fox Co. To-Do List
# Created initially by James Britton
# Ver 0.9.5
# First created: 27/12/2020
# Last update: 01/03/2021
# Desc: To-do list with basic functionality and ability to save stuff.
###############################################################################

import sys, os, tkinter
import tkinter.font as font
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from datetime import datetime


###############################################################################
# Starting variables:
###############################################################################

now = datetime.now()
current_date = now.strftime("%D")
tasks = []
tasks_load = []

###############################################################################
# Custom classes:
###############################################################################

# This custom class is a dialogue box you can copy-paste from
class CustomDialog(tkinter.simpledialog.Dialog, Text):
    
    def __init__(self, parent, title=None, text=None):
        self.data = text
        tkinter.simpledialog.Dialog.__init__(self, parent, title=title)
    
    def buttonbox(self):
        box = Frame(self)
        w = Button(box, text="Change", width=10, command=self.update)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Button(box, text="Close", width=10, command=self.cancel, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
#        self.bind("<Return>", self.update)
        self.bind("<Escape>", self.cancel)
        box.pack()

    def body(self, parent):
        self.text = tkinter.Text(self, width=75, height=15)
        self.text.pack(fill="both", expand=True)
        self.text.insert("1.0", self.data)
        return self.text

    def update(self):
        global changetask
        self.currenttext = self.text.get('0.0',"end")
        changetask = self.currenttext 
        update_task(changetask)
        self.ok()



###############################################################################
# Functions:
###############################################################################

def update_taskbox():
    # Clear what's in there currently:
    clear_task_func()
    while("" in tasks): 
       tasks.remove("") 
    # Populate the visual listbox:
    for task in tasks:
        lb_tasks.insert("end", task)

def clear_task_func():
    # Clears all tasks by wiping out the list
    lb_tasks.delete(0, "end")

def add_task_func():
    task = txt_input.get()
    if task !="":
        now = datetime.now()
        current_time = now.strftime("%D %H:%M")
        tasks.append(str(current_time) + ":  " + task)
        update_taskbox()
        txt_input.delete(0,"end")
        lbl_display['text'] = "'{:.75}' ... added.".format(task)
    else:
        lbl_display['text'] = "Please enter an item, don't leave the field blank."

def remove_task_func():
    # Get the text of the currently selected item:
    task = lb_tasks.get("active")
    if task in tasks:
        tasks.remove(task)
        update_taskbox()
        lbl_display['text'] = "'{:.75}...' removed.".format(task)

def sort_task_asc():
    tasks.sort()
    lbl_display['text'] = "Sorting in ascending order."
    update_taskbox()

def sort_task_des():
    tasks.sort()
    tasks.reverse()
    lbl_display['text'] = "Sorting in descending order."
    update_taskbox()

def delete_all_task_func():
    #Note: task list is being changed globally, must be defined as global variable
    global tasks
    confirm = messagebox.askyesno("Confirm: Delete all tasks?", "Are you sure? This is irreversible!")
    if confirm:
        tasks = []
        update_taskbox()
        lbl_display['text'] = "All notes were cleared."
    else:
        messagebox.showinfo("Okay!", "Gotcha! ^_^")

def task_number_func():
    number_of_tasks = len(tasks)
    message = "Number of tasks: %s" % number_of_tasks
    lbl_display['text'] = message

def Quit():
    confirm = messagebox.askyesno("Confirm: quit?!", "Are you sure? Make sure you have saved, tasks do not have permanence unless saved!")
    if confirm:
        save_tasks()
        sys.exit()
    else:
        messagebox.showinfo("Cancelled.", "Cancelled.")

def task_popup_func(task): # Used for doubleclick function
    task = lb_tasks.get("active")
    messagebox.showinfo("Detail view", task)

def task_clipboard_func(task):
    task = lb_tasks.get("active")
    root.clipboard_clear()
    root.clipboard_append(task)
    message = "'{:.75}...' copied to clipboard.".format(task)
    lbl_display['text'] = message

# Only here to open the damn fox logo
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def save_tasks():
    confirm = messagebox.askyesno("Confirm: save?", "Would you like to save? This will overwrite the currently existing file, if it exists.")
    if confirm:
        while("" in tasks): 
            tasks.remove("")
        with open("todo_tasks_fox.txt", "w") as f: # The save-file is a text file loaded as "f"
            for s in tasks:
                f.write(str(s) +"\n")
    update_taskbox()
    lbl_display['text'] = "Saved notes to file todo_tasks_fox.txt."

def load_tasks():
    global tasks, tasks_load
    confirm = messagebox.askyesno("Confirm: load?", "Are you sure? This will overwrite notes in the listbox, if any, and replace with the contents of the save file.")
    if confirm:
        tasks = []
        tasks_load = []
        with open("todo_tasks_fox.txt", "r") as f:
            for line in f:
                tasks_load.append(str(line.strip()))
            tasks = tasks_load
        update_taskbox()
        lbl_display['text'] = "Loaded notes from file todo_tasks_fox.txt."

def show_dialog(task): # this opens the copy-able dialogue box
        task = lb_tasks.get("active") 
        detail_text = task
        CustomDialog(root, title="Detail view", text=detail_text)

def update_task(changetask):
        task = lb_tasks.get("active")
        tasks.remove(task)
        tasks.insert(0,changetask)
        update_taskbox()
        task = ""
        changetask = ""




###############################################################################
# Main window:
###############################################################################

root = tkinter.Tk()
root.configure()
root.title("Fox Co. To-Do List.")
root.geometry("680x460")

title_font = font.Font(family='Consolas', size=14)
lbl_title = tkinter.Label(root, text="Fox Co. To-Do List", font="title_font")
lbl_title.grid(row=0,column=0)

lbl_subtitle = tkinter.Label(root, text="Created by a fox (so excuse the bugs)", fg="orange")
lbl_subtitle.grid(row=0,column=1, sticky="e")
lbl_subtitle1 = tkinter.Label(root, text="Back to the grind!")
lbl_subtitle1.grid(row=1,column=0)

lbl_current_time = tkinter.Label(root, text=current_date)
lbl_current_time.grid(row=1,column=1, sticky="e")

lbl_spacer = tkinter.Label(root, text="                                                                        ")
lbl_spacer.grid(row=2,column=0)
lbl_display = tkinter.Label(root, text="Messages appear here -- double click tasks for detail view, left-then-right click to copy to clipboard.", fg="red") # Info box
lbl_display.grid(row=3,column=0, columnspan=2)
lbl_spacer1 = tkinter.Label(root, text="                                                                        ")
lbl_spacer1.grid(row=4,column=0)

txt_input = tkinter.Entry(root, width=75) # Entry field for tasks
txt_input.grid(row=5,column=1)

btn_add_task = tkinter.Button(root, text="Add task:", command=add_task_func)
btn_add_task.grid(row=5,column=0, sticky="ew")

btn_sort_task = tkinter.Button(root, text="Sort tasks", command=sort_task_asc)
btn_sort_task.grid(row=7,column=0, sticky="ew")

btn_sort_des_task = tkinter.Button(root, text="Sort tasks (desc.)", command=sort_task_des)
btn_sort_des_task.grid(row=8,column=0, sticky="ew")

btn_remove_task = tkinter.Button(root, text="Remove task", command=remove_task_func)
btn_remove_task.grid(row=9,column=0, sticky="ew")

btn_delete_all_task = tkinter.Button(root, text="Remove all tasks?", command=delete_all_task_func)
btn_delete_all_task.grid(row=10,column=0, sticky="ew")

btn_number_tasks = tkinter.Button(root, text="Number of tasks", command=task_number_func)
btn_number_tasks.grid(row=11,column=0, sticky="ew")

# The listbox and its scrollbar
lb_tasks = tkinter.Listbox(width=75)
lb_tasks.grid(row=7,column=1, rowspan=7)
scrollbar = Scrollbar(root, orient="horizontal", width=12)
scrollbar.grid(row=15,column=1, sticky="ew")    
lb_tasks.config(xscrollcommand = scrollbar.set)
scrollbar.config(command = lb_tasks.xview)
lb_tasks.bind('<Double-1>', show_dialog)
lb_tasks.bind('<Button-3>', task_clipboard_func)


# Credits & logo down here
cred_font = font.Font(family='Segoe Print', size=12)
lbl_credits = tkinter.Label(root, text="By James Britton, 2020", fg="orange", font=cred_font)
lbl_credits.grid(row=16,column=1, sticky="s")
logo = PhotoImage(file=resource_path("maned.png"))
lbl_logo = tkinter.Label(root, image=logo)
lbl_logo.grid(row=16,column=1, sticky="e")

# Saving and loading buttons, down the bottom
btn_save_tasks = tkinter.Button(root, text="Save tasks?", command=save_tasks,fg="orange",bg="black")
btn_save_tasks.grid(row=17,column=0, sticky="w")

btn_load_tasks = tkinter.Button(root, text="Load tasks?", command=load_tasks,fg="cyan",bg="black")
btn_load_tasks.grid(row=17,column=1, sticky="e")

# Quit button, hence the colors.
btn_quit = tkinter.Button(root, text="      Quit      ", command=Quit, fg="red", bg="black")
btn_quit.grid(row=18,column=0, sticky="w")

# Main loop.
root.mainloop()
