import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import os

# ---------- Setup ----------
root = tk.Tk()
root.title("To-Do List")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

tasks = []

# ---------- Functions ----------
def save_tasks():
    with open("tasks.txt", "w", encoding="utf-8") as file:
        for task in tasks:
            file.write(task + "\n")

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r", encoding="utf-8") as file:
            for line in file:
                task = line.strip()
                tasks.append(task)
                listbox.insert(tk.END, task)

def add_task():
    task = entry.get()
    due = date_entry.get()
    if task:
        task_str = f"[❌] {task} (Due: {due})"
        tasks.append(task_str)
        listbox.insert(tk.END, task_str)
        entry.delete(0, tk.END)
        save_tasks()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def delete_task():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        listbox.delete(index)
        tasks.pop(index)
        save_tasks()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to delete.")

def toggle_done():
    selected = listbox.curselection()
    if selected:
        index = selected[0]
        task = tasks[index]
        if "[❌]" in task:
            task = task.replace("[❌]", "[✔]")
        else:
            task = task.replace("[✔]", "[❌]")
        tasks[index] = task
        listbox.delete(index)
        listbox.insert(index, task)
        save_tasks()
    else:
        messagebox.showwarning("Selection Error", "Please select a task to toggle.")

def sort_tasks():
    def task_key(t):
        done = "[✔]" in t
        date_part = t.split("Due: ")[-1].replace(")", "") if "Due:" in t else "9999-99-99"
        return (done, date_part)
    global tasks
    tasks.sort(key=task_key)
    listbox.delete(0, tk.END)
    for t in tasks:
        listbox.insert(tk.END, t)
    save_tasks()

def filter_tasks(event):
    search = search_entry.get().lower()
    listbox.delete(0, tk.END)
    for t in tasks:
        if search in t.lower():
            listbox.insert(tk.END, t)

# ---------- Widgets ----------
search_entry = tk.Entry(root, width=30, font=("Arial", 12))
search_entry.pack(pady=10)
search_entry.insert(0, "Search...")
search_entry.bind("<KeyRelease>", filter_tasks)

entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=5)

due_label = tk.Label(root, text="Due Date:", bg="#f0f0f0", font=("Arial", 10))
due_label.pack()

date_entry = DateEntry(root, width=20, background='darkblue',
                       foreground='white', borderwidth=2, font=("Arial", 10))
date_entry.pack(pady=5)

add_button = tk.Button(root, text="Add Task", command=add_task,
                       font=("Arial", 10), bg="#4CAF50", fg="white", width=15)
add_button.pack(pady=5)

listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12), selectbackground="#a0a0ff")
listbox.pack(pady=10)

done_button = tk.Button(root, text="Toggle Done", command=toggle_done,
                        font=("Arial", 10), bg="#2196F3", fg="white", width=15)
done_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task,
                          font=("Arial", 10), bg="#f44336", fg="white", width=15)
delete_button.pack(pady=5)

sort_button = tk.Button(root, text="Sort Tasks", command=sort_tasks,
                        font=("Arial", 10), bg="#FFC107", fg="black", width=15)
sort_button.pack(pady=5)

# ---------- Load Existing Tasks ----------
load_tasks()

# ---------- Run App ----------
root.mainloop()
