import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to the database or create it
conn = sqlite3.connect('job.db')
cursor = conn.cursor()

# Create the jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    position TEXT NOT NULL,
    company TEXT NOT NULL,
    status TEXT NOT NULL,
    date TEXT NOT NULL
)
""")
conn.commit()

# Functions to manage the records
def add_job():
    position = entry_position.get()
    company = entry_company.get()
    status = entry_status.get()
    date = entry_date.get()

    if position and company and status and date:
        cursor.execute("INSERT INTO jobs (position, company, status, date) VALUES (?, ?, ?, ?)",
                       (position, company, status, date))
        conn.commit()
        messagebox.showinfo("Success", "Job added successfully")
        clear_entries()
        view_jobs()
    else:
        messagebox.showwarning("Input Error", "All fields are required")

def view_jobs():
    cursor.execute("SELECT * FROM jobs")
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, row)

def update_job():
    selected_item = listbox.curselection()
    if selected_item:
        job_id = listbox.get(selected_item)[0]
        position = entry_position.get()
        company = entry_company.get()
        status = entry_status.get()
        date = entry_date.get()

        if position and company and status and date:
            cursor.execute("""
            UPDATE jobs
            SET position=?, company=?, status=?, date=?
            WHERE id=?
            """, (position, company, status, date, job_id))
            conn.commit()
            messagebox.showinfo("Success", "Job updated successfully")
            clear_entries()
            view_jobs()
        else:
            messagebox.showwarning("Input Error", "All fields are required")
    else:
        messagebox.showwarning("Selection Error", "No job selected")

def delete_job():
    selected_item = listbox.curselection()
    if selected_item:
        job_id = listbox.get(selected_item)[0]
        cursor.execute("DELETE FROM jobs WHERE id=?", (job_id,))
        conn.commit()
        messagebox.showinfo("Success", "Job deleted successfully")
        view_jobs()
    else:
        messagebox.showwarning("Selection Error", "No job selected")

def clear_entries():
    entry_position.delete(0, tk.END)
    entry_company.delete(0, tk.END)
    entry_status.delete(0, tk.END)
    entry_date.delete(0, tk.END)

# Setup the GUI
root = tk.Tk()
root.title("Jobhunt Tracker")

tk.Label(root, text="Position").grid(row=0, column=0, padx=10, pady=5)
tk.Label(root, text="Company").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Status").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="Date").grid(row=3, column=0, padx=10, pady=5)

entry_position = tk.Entry(root)
entry_position.grid(row=0, column=1, padx=10, pady=5)
entry_company = tk.Entry(root)
entry_company.grid(row=1, column=1, padx=10, pady=5)
entry_status = tk.Entry(root)
entry_status.grid(row=2, column=1, padx=10, pady=5)
entry_date = tk.Entry(root)
entry_date.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Add Job", command=add_job).grid(row=4, column=0, padx=10, pady=5)
tk.Button(root, text="Update Job", command=update_job).grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Delete Job", command=delete_job).grid(row=5, column=0, padx=10, pady=5)
tk.Button(root, text="Clear Fields", command=clear_entries).grid(row=5, column=1, padx=10, pady=5)

listbox = tk.Listbox(root, width=50)
listbox.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

view_jobs()

root.mainloop()

# Close the database connection when the program ends
conn.close()
