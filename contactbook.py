import tkinter as tk
from tkinter import ttk, messagebox

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("📒 Contact Book")
        self.root.geometry("700x500")
        self.root.configure(bg="#121212")
        
        # Custom fonts
        self.title_font = ("Arial", 18, "bold")
        self.text_font = ("Arial", 12)
        
        # Contact storage (list of dictionaries)
        self.contacts = []
        
        # UI Setup
        self.setup_ui()
    
    def setup_ui(self):
        # Main Frame
        main_frame = tk.Frame(self.root, bg="#121212")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(main_frame, text="CONTACT BOOK", font=self.title_font, 
                bg="#121212", fg="white").grid(row=0, column=0, columnspan=2, pady=10)
        
        # Input Frame
        input_frame = tk.Frame(main_frame, bg="#1e1e1e", padx=10, pady=10)
        input_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Contact Fields
        fields = ["Name", "Phone", "Email", "Address"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            tk.Label(input_frame, text=f"{field}:", bg="#1e1e1e", fg="white", 
                    font=self.text_font).grid(row=i, column=0, sticky="w", pady=5)
            entry = tk.Entry(input_frame, width=30, font=self.text_font, bg="#2a2a2a", 
                            fg="white", insertbackground="white")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[field.lower()] = entry
        
        # Buttons
        button_frame = tk.Frame(input_frame, bg="#1e1e1e")
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        buttons = [
            ("Add", self.add_contact),
            ("Update", self.update_contact),
            ("Delete", self.delete_contact),
            ("Clear", self.clear_fields)
        ]
        
        for i, (text, command) in enumerate(buttons):
            tk.Button(button_frame, text=text, width=10, font=self.text_font,
                     command=command, bg="#2a2a2a", fg="white").grid(row=0, column=i, padx=5)
        
        # Search Frame
        search_frame = tk.Frame(main_frame, bg="#1e1e1e", padx=10, pady=10)
        search_frame.grid(row=2, column=0, sticky="ew", pady=10)
        
        tk.Label(search_frame, text="Search:", bg="#1e1e1e", fg="white", 
                font=self.text_font).grid(row=0, column=0)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30, 
                                   font=self.text_font, bg="#2a2a2a", fg="white")
        self.search_entry.grid(row=0, column=1, padx=5)
        self.search_entry.bind("<KeyRelease>", self.search_contact)  # Search as you type
        tk.Button(search_frame, text="Clear", font=self.text_font,
                 command=self.clear_search, bg="#2a2a2a", fg="white").grid(row=0, column=2, padx=5)
        
        # Contacts List
        list_frame = tk.Frame(main_frame, bg="#1e1e1e")
        list_frame.grid(row=1, column=1, rowspan=2, sticky="nsew", padx=10)
        
        self.tree = ttk.Treeview(list_frame, columns=("Name", "Phone"), show="headings", height=15)
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.pack(fill="both", expand=True)
        
        # Bind selection event
        self.tree.bind("<ButtonRelease-1>", self.load_selected_contact)
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
    
    def add_contact(self):
        contact = {field: self.entries[field].get() for field in self.entries}
        if not contact["name"]:
            messagebox.showerror("Error", "Name is required!")
            return
        
        self.contacts.append(contact)
        self.update_contact_list()
        self.clear_fields()
        messagebox.showinfo("Success", "Contact added successfully!")
    
    def update_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No contact selected!")
            return
        
        index = int(self.tree.item(selected, "tags")[0])
        for field in self.entries:
            self.contacts[index][field] = self.entries[field].get()
        
        self.update_contact_list()
        messagebox.showinfo("Success", "Contact updated successfully!")
    
    def delete_contact(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No contact selected!")
            return
        
        if messagebox.askyesno("Confirm", "Delete this contact?"):
            index = int(self.tree.item(selected, "tags")[0])
            del self.contacts[index]
            self.update_contact_list()
            self.clear_fields()
    
    def search_contact(self, event=None):
        query = self.search_var.get().lower()
        if not query:
            self.update_contact_list()
            return
        
        results = []
        for i, contact in enumerate(self.contacts):
            if (query in contact["name"].lower() or 
                query in contact["phone"].lower()):
                results.append((i, contact))
        
        self.update_contact_list(results if results else None)
    
    def clear_search(self):
        self.search_var.set("")
        self.update_contact_list()
    
    def load_selected_contact(self, event):
        selected = self.tree.focus()
        if selected:
            index = int(self.tree.item(selected, "tags")[0])
            contact = self.contacts[index]
            for field in self.entries:
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, contact[field])
    
    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def update_contact_list(self, contacts=None):
        self.tree.delete(*self.tree.get_children())
        display_list = contacts if contacts else enumerate(self.contacts)
        
        for i, contact in display_list:
            self.tree.insert("", "end", 
                            values=(contact["name"], contact["phone"]), 
                            tags=(i,))

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()