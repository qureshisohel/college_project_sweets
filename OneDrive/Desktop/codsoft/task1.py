import tkinter as tk
from tkinter import messagebox

def add_item():
    new_item = item_entry.get()
    if new_item.strip():
        listbox.insert(tk.END, new_item)
        item_entry.delete(0, tk.END)
        show_success_label("Text added successfully", "green")

def show_success_label(message, color):
    success_label.config(text=message, fg=color)
    success_label.pack()
    success_label.after(3000, clear_success_label)

def clear_success_label():
    success_label.config(text="")
    success_label.pack_forget()

def remove_item():
    selected_item_index = listbox.curselection()
    if selected_item_index:
        listbox.delete(selected_item_index)
        show_success_label("Text deleted successfully", "green")
    else:
        show_success_label("Please select a task to delete", "red")

def edit_item():
    selected_item_index = listbox.curselection()
    if selected_item_index:
        item_text = listbox.get(selected_item_index)
        item_entry.delete(0, tk.END)
        item_entry.insert(0, item_text)
        add_button.config(text="Edit", command=apply_edit)
        edit_button.config(state=tk.DISABLED)

def apply_edit():
    selected_item_index = listbox.curselection()
    if selected_item_index:
        edited_text = item_entry.get()
        listbox.delete(selected_item_index)
        listbox.insert(selected_item_index, edited_text)
        item_entry.delete(0, tk.END)
        add_button.config(text="Submit", command=add_item)
        edit_button.config(state=tk.NORMAL)
        show_success_label("Text edited successfully", "green")
    else:
        show_success_label("Please select a task to edit", "red")



app = tk.Tk()
app.title("To-Do List")
app.geometry("500x400")
header = tk.Label(app, text="To-Do List", font=("Comic Sans MS", 18, "bold"), bg="green", fg="white", padx=10, pady=10)
header.pack(fill=tk.X)

item_entry = tk.Entry(app, font=("Arial", 12))
item_entry.pack(fill=tk.X, padx=10, pady=10)

add_button = tk.Button(app, text="Submit", command=add_item, font=("Arial", 12), bg="black", fg="white")
add_button.pack()

success_label = tk.Label(app, text="", font=("Arial", 10, "italic"))

listbox = tk.Listbox(app, font=("Arial", 12), bg="white", selectbackground="lightgrey")
listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
remove_button = tk.Button(app, text="Delete", command=remove_item, font=("Arial", 12), bg="red", fg="white")
remove_button.pack()

edit_button = tk.Button(app, text="Edit", command=edit_item, font=("Arial", 12), bg="green", fg="white")
edit_button.pack()

# ... (other widget configurations remain the same)

app.mainloop()
