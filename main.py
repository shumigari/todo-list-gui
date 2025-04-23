import tkinter as tk
from tkinter import messagebox
import os

# ---------- Setup ----------
root = tk.Tk()
root.title("To-Do List")
root.geometry("450x500")
root.configure(bg="#f0f0f0")

tasks = []

# ---------- Functions ----------
def save_tasks():
    with open("tasks.txt", "w") as file:
        for task in tasks:
            file.write(task + "\n")

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as file:
            for line in file:
                task = line.strip()
                tasks.append(task)
                listbox.insert(tk.END, task)

def add_task():
    task = entry.get()
    if task:
        task = f"[❌] {task}"
        tasks.append(task)
        listbox.insert(tk.END, task)
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
        messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

# ---------- Widgets ----------
entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=15)

add_button = tk.Button(root, text="Add Task", command=add_task,
                       font=("Arial", 10), bg="#4CAF50", fg="white", width=15)
add_button.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=10, font=("Arial", 12), selectbackground="#a0a0ff")
listbox.pack(pady=10)

done_button = tk.Button(root, text="Toggle Done", command=toggle_done,
                        font=("Arial", 10), bg="#2196F3", fg="white", width=15)
done_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task,
                          font=("Arial", 10), bg="#f44336", fg="white", width=15)
delete_button.pack(pady=5)

# ---------- Load Existing Tasks ----------
load_tasks()

# ---------- Run App ----------
root.mainloop()
