import tkinter as tk
from tkinter import font as tkfont
from math import sqrt

class ErrorFreeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔢 Error-Free Calculator")
        self.root.geometry("320x500")
        self.root.configure(bg="#121212")
        self.root.resizable(False, False)
        
        # Custom font
        self.display_font = tkfont.Font(size=24, weight="bold")
        self.button_font = tkfont.Font(size=16)
        
        # Display - using grid instead of pack
        self.display_var = tk.StringVar()
        self.display = tk.Entry(
            root, textvariable=self.display_var, font=self.display_font,
            borderwidth=0, relief="flat", justify="right", bg="#1e1e1e", fg="white",
            insertbackground="white", highlightthickness=0
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=20, pady=(30, 20), ipady=10)
        
        # Button layout
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
            ("C", 5, 0), ("⌫", 5, 1), ("√", 5, 2), ("^", 5, 3)
        ]
        
        # Button styling
        button_bg = "#2a2a2a"
        button_fg = "white"
        button_active_bg = "#3a3a3a"
        
        # Create buttons
        for (text, row, col) in buttons:
            btn = tk.Button(
                root, text=text, font=self.button_font, 
                command=lambda t=text: self.on_button_click(t),
                bg=button_bg, fg=button_fg, activebackground=button_active_bg,
                borderwidth=0, relief="flat", padx=20, pady=10
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Configure grid weights
        for i in range(6):  # Changed from (1,6) to include row 0
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        
        # Initialize calculator state
        self.current_input = ""
        self.bind_keyboard_events()
    
    def on_button_click(self, button_text):
        if button_text == "=":
            self.calculate_result()
        elif button_text == "C":
            self.clear_display()
        elif button_text == "⌫":
            self.backspace()
        elif button_text == "√":
            self.current_input += "sqrt("
            self.display_var.set(self.current_input)
        elif button_text == "^":
            self.current_input += "**"
            self.display_var.set(self.current_input)
        else:
            self.current_input += button_text
            self.display_var.set(self.current_input)
    
    def calculate_result(self):
        try:
            # Replace ^ with ** for exponentiation
            expression = self.current_input.replace("^", "**")
            result = str(eval(expression, {"sqrt": sqrt, "__builtins__": None}))
            self.display_var.set(result)
            self.current_input = result
        except ZeroDivisionError:
            self.display_var.set("Error: Division by zero")
            self.current_input = ""
        except (SyntaxError, NameError, TypeError):
            self.display_var.set("Error: Invalid input")
            self.current_input = ""
        except Exception:
            self.display_var.set("Error: Calculation failed")
            self.current_input = ""
    
    def clear_display(self):
        self.current_input = ""
        self.display_var.set("")
    
    def backspace(self):
        self.current_input = self.current_input[:-1]
        self.display_var.set(self.current_input)
    
    def bind_keyboard_events(self):
        self.root.bind("<Key>", self.handle_key_press)
    
    def handle_key_press(self, event):
        key = event.char
        if key in "0123456789+-*/.()":
            self.on_button_click(key)
        elif event.keysym == "Return":
            self.calculate_result()
        elif event.keysym == "BackSpace":
            self.backspace()
        elif event.keysym == "Escape":
            self.clear_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = ErrorFreeCalculator(root)
    root.mainloop()