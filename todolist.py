import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class UltimateTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("✅ Ultimate To-Do List")
        self.root.geometry("650x750")
        self.root.configure(bg="#f8f9fa")
        
        # Data file
        self.data_file = "todos.json"
        self.todos = []
        
        # Load existing todos
        self.load_todos()
        
        # Custom fonts
        self.title_font = ("Segoe UI", 20, "bold")
        self.text_font = ("Segoe UI", 12)
        self.serial_font = ("Segoe UI", 10, "bold")
        
        # Create UI
        self.setup_ui()
    
    def setup_ui(self):
        # Header with gradient
        header_frame = tk.Frame(self.root, bg="#6a11cb")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        tk.Label(header_frame, text="Ultimate To-Do List", 
                font=self.title_font, bg="#6a11cb", fg="white", padx=20, pady=15).pack()
        
        # Input area with shadow effect
        input_frame = tk.Frame(self.root, bg="#f8f9fa")
        input_frame.pack(fill="x", padx=20, pady=15)
        
        self.task_entry = tk.Entry(input_frame, font=self.text_font, 
                                 bg="white", relief="flat", highlightthickness=1,
                                 highlightbackground="#ddd", highlightcolor="#6a11cb")
        self.task_entry.pack(side="left", expand=True, fill="x", padx=(0, 10), ipady=8)
        
        add_btn = tk.Button(input_frame, text="➕ Add", command=self.add_task,
                          bg="#6a11cb", fg="white", font=self.text_font,
                          relief="flat", padx=15)
        add_btn.pack(side="right")
        
        # Task list with serial numbers
        self.list_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.list_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Create treeview with custom style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Ultimate.Treeview", font=self.text_font, rowheight=45, 
                       background="#ffffff", fieldbackground="#ffffff")
        style.configure("Ultimate.Treeview.Heading", font=("Segoe UI", 12, "bold"),
                       background="#e9ecef", foreground="#495057")
        style.map("Ultimate.Treeview", background=[("selected", "#e2e2e2")])
        
        self.tree = ttk.Treeview(self.list_frame, columns=("serial", "status", "task"), 
                               show="headings", style="Ultimate.Treeview")
        
        # Configure columns
        self.tree.heading("serial", text="#")
        self.tree.heading("status", text="✓")
        self.tree.heading("task", text="Task Description")
        
        self.tree.column("serial", width=50, anchor="center")
        self.tree.column("status", width=50, anchor="center")
        self.tree.column("task", width=400, anchor="w")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        
        # Bind events
        self.tree.bind("<Double-1>", self.toggle_complete)
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Right-click menu with all options
        self.menu = tk.Menu(self.root, tearoff=0, font=self.text_font)
        self.menu.add_command(label="Mark Complete", command=self.toggle_complete)
        self.menu.add_command(label="Update Task", command=self.update_task_dialog)
        self.menu.add_command(label="Delete Task", command=self.delete_task)
        self.menu.add_separator()
        self.menu.add_command(label="Clear Completed", command=self.clear_completed)
        
        self.tree.bind("<Button-3>", self.show_menu)
        
        # Action buttons frame
        action_frame = tk.Frame(self.root, bg="#f8f9fa")
        action_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Button(action_frame, text="Mark Complete", command=self.toggle_complete,
                bg="#28a745", fg="white", font=self.text_font).pack(side="left", padx=5)
        tk.Button(action_frame, text="Update Task", command=self.update_task_dialog,
                bg="#17a2b8", fg="white", font=self.text_font).pack(side="left", padx=5)
        tk.Button(action_frame, text="Delete Task", command=self.delete_task,
                bg="#dc3545", fg="white", font=self.text_font).pack(side="left", padx=5)
        
        # Load existing tasks
        self.refresh_list()
    
    def add_task(self):
        task = self.task_entry.get().strip()
        if task:
            self.todos.append({"task": task, "completed": False})
            self.task_entry.delete(0, tk.END)
            self.save_todos()
            self.refresh_list()
    
    def toggle_complete(self, event=None):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a task first!")
            return
        item = self.tree.selection()[0]
        index = int(self.tree.item(item, "values")[0]) - 1
        self.todos[index]["completed"] = not self.todos[index]["completed"]
        self.save_todos()
        self.refresh_list()
    
    def update_task_dialog(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a task first!")
            return
        item = self.tree.selection()[0]
        index = int(self.tree.item(item, "values")[0]) - 1
        current_task = self.todos[index]["task"]
        
        # Create update dialog
        new_task = simpledialog.askstring("Update Task", "Edit your task:", 
                                        initialvalue=current_task,
                                        parent=self.root)
        
        if new_task and new_task.strip():
            self.todos[index]["task"] = new_task.strip()
            self.save_todos()
            self.refresh_list()
    
    def delete_task(self):
        if not self.tree.selection():
            messagebox.showwarning("Warning", "Please select a task first!")
            return
        if messagebox.askyesno("Confirm", "Delete this task permanently?"):
            item = self.tree.selection()[0]
            index = int(self.tree.item(item, "values")[0]) - 1
            del self.todos[index]
            self.save_todos()
            self.refresh_list()
    
    def clear_completed(self):
        if messagebox.askyesno("Confirm", "Clear all completed tasks?"):
            self.todos = [todo for todo in self.todos if not todo["completed"]]
            self.save_todos()
            self.refresh_list()
    
    def show_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)
    
    def refresh_list(self):
        self.tree.delete(*self.tree.get_children())
        for i, todo in enumerate(self.todos, 1):
            serial = str(i).zfill(2)  # 01, 02, etc.
            status = "✓" if todo["completed"] else ""
            tags = ("completed",) if todo["completed"] else ()
            self.tree.insert("", "end", values=(serial, status, todo["task"]), tags=tags)
        
        # Style completed tasks
        self.tree.tag_configure("completed", foreground="#adb5bd")
    
    def load_todos(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    self.todos = json.load(f)
            except:
                self.todos = []
    
    def save_todos(self):
        with open(self.data_file, "w") as f:
            json.dump(self.todos, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = UltimateTodoApp(root)
    root.mainloop()