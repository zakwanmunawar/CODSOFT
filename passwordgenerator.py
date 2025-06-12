import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Secure Password Generator")
        self.root.geometry("400x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#121212")

        # Custom fonts
        self.title_font = ("Arial", 18, "bold")
        self.text_font = ("Arial", 12)

        # Initialize variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=12)
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.digits_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)

        # Build UI
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(
            self.root, text="PASSWORD GENERATOR",
            font=self.title_font, bg="#121212", fg="white"
        ).pack(pady=(15, 10))

        # Length Control
        length_frame = tk.Frame(self.root, bg="#1e1e1e")
        length_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(
            length_frame, text="Length (8-32):",
            font=self.text_font, bg="#1e1e1e", fg="white"
        ).pack(side="left", padx=5)

        tk.Scale(
            length_frame, from_=8, to=32, orient="horizontal",
            variable=self.length_var, bg="#1e1e1e", fg="white",
            highlightthickness=0, troughcolor="#2a2a2a"
        ).pack(side="left", expand=True, fill="x", padx=5)

        # Character Options
        options_frame = tk.Frame(self.root, bg="#1e1e1e", padx=10, pady=10)
        options_frame.pack(fill="x", padx=20, pady=10)

        tk.Checkbutton(
            options_frame, text="A-Z", variable=self.uppercase_var,
            bg="#1e1e1e", fg="white", selectcolor="#121212"
        ).grid(row=0, column=0, sticky="w", pady=2)

        tk.Checkbutton(
            options_frame, text="a-z", variable=self.lowercase_var,
            bg="#1e1e1e", fg="white", selectcolor="#121212"
        ).grid(row=1, column=0, sticky="w", pady=2)

        tk.Checkbutton(
            options_frame, text="0-9", variable=self.digits_var,
            bg="#1e1e1e", fg="white", selectcolor="#121212"
        ).grid(row=0, column=1, sticky="w", pady=2)

        tk.Checkbutton(
            options_frame, text="!@#", variable=self.symbols_var,
            bg="#1e1e1e", fg="white", selectcolor="#121212"
        ).grid(row=1, column=1, sticky="w", pady=2)

        # Generate Button
        tk.Button(
            self.root, text="GENERATE", command=self.generate_password,
            font=self.text_font, bg="#2a2a2a", fg="white", pady=5
        ).pack(pady=10, fill="x", padx=40)

        # Password Display
        tk.Entry(
            self.root, textvariable=self.password_var, font=("Arial", 14),
            state="readonly", readonlybackground="#1e1e1e", fg="#4CAF50",
            borderwidth=0, justify="center"
        ).pack(fill="x", padx=40, pady=5)

        # Copy Button (using Tkinter's built-in clipboard)
        tk.Button(
            self.root, text="COPY", command=self.copy_password,
            font=self.text_font, bg="#2a2a2a", fg="white", pady=5
        ).pack(pady=5, fill="x", padx=40)

    def generate_password(self):
        try:
            # Validate selection
            if not any([
                self.uppercase_var.get(),
                self.lowercase_var.get(),
                self.digits_var.get(),
                self.symbols_var.get()
            ]):
                messagebox.showerror("Error", "Select at least one character type!")
                return

            # Build character pool
            chars = ""
            if self.uppercase_var.get():
                chars += string.ascii_uppercase
            if self.lowercase_var.get():
                chars += string.ascii_lowercase
            if self.digits_var.get():
                chars += string.digits
            if self.symbols_var.get():
                chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"

            # Generate password
            length = self.length_var.get()
            password = "".join(random.choices(chars, k=length))
            self.password_var.set(password)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate: {str(e)}")

    def copy_password(self):
        if password := self.password_var.get():
            self.root.clipboard_clear()
            self.root.clipboard_append(password)
            messagebox.showinfo("Copied!", "Password copied to clipboard!")
        else:
            messagebox.showerror("Error", "No password to copy!")

if __name__ == "__main__":
    root = tk.Tk()
    PasswordGenerator(root)
    root.mainloop()