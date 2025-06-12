import tkinter as tk
from tkinter import font as tkfont
import random

class VisualRPSGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Visual RPS Game")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f0f0")
        
        # Game variables
        self.user_score = 0
        self.comp_score = 0
        self.choices = ["rock", "paper", "scissors"]
        self.choice_emojis = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
        self.choice_colors = {"rock": "#3498db", "paper": "#e74c3c", "scissors": "#2ecc71"}
        
        # Create UI
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_font = tkfont.Font(size=24, weight="bold")
        tk.Label(self.root, text="Rock Paper Scissors", 
                font=title_font, bg="#f0f0f0").pack(pady=20)
        
        # Score display
        self.score_label = tk.Label(self.root, 
                                  text=f"You: {self.user_score}  Computer: {self.comp_score}",
                                  font=tkfont.Font(size=16),
                                  bg="#f0f0f0")
        self.score_label.pack()
        
        # Choice buttons
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=30)
        
        for choice in self.choices:
            btn = tk.Button(button_frame, text=f"{self.choice_emojis[choice]} {choice.capitalize()}",
                          font=tkfont.Font(size=14),
                          bg=self.choice_colors[choice], fg="white",
                          command=lambda c=choice: self.play_round(c),
                          padx=20, pady=10)
            btn.pack(side="left", padx=10)
        
        # Visual display area
        self.display_frame = tk.Frame(self.root, bg="#ecf0f1", width=400, height=200)
        self.display_frame.pack(pady=20)
        self.display_frame.pack_propagate(False)
        
        # User choice display
        self.user_display = tk.Label(self.display_frame, text="", 
                                   font=tkfont.Font(size=40),
                                   bg="#ecf0f1")
        self.user_display.pack(side="left", padx=40)
        
        # VS label
        tk.Label(self.display_frame, text="VS", 
                font=tkfont.Font(size=20),
                bg="#ecf0f1").pack(side="left")
        
        # Computer choice display
        self.comp_display = tk.Label(self.display_frame, text="", 
                                    font=tkfont.Font(size=40),
                                    bg="#ecf0f1")
        self.comp_display.pack(side="left", padx=40)
        
        # Result display
        self.result_label = tk.Label(self.root, text="", 
                                   font=tkfont.Font(size=18, weight="bold"),
                                   bg="#f0f0f1")
        self.result_label.pack()
        
        # Play again button
        self.play_again_btn = tk.Button(self.root, text="Play Again", 
                                      font=tkfont.Font(size=12),
                                      state=tk.DISABLED,
                                      command=self.reset_game)
        self.play_again_btn.pack(pady=20)
    
    def play_round(self, user_choice):
        # Computer makes random choice
        comp_choice = random.choice(self.choices)
        
        # Update visual displays
        self.user_display.config(text=self.choice_emojis[user_choice])
        self.comp_display.config(text=self.choice_emojis[comp_choice])
        
        # Determine winner
        if user_choice == comp_choice:
            result = "It's a tie!"
            color = "#f39c12"  # Orange
        elif (user_choice == "rock" and comp_choice == "scissors") or \
             (user_choice == "paper" and comp_choice == "rock") or \
             (user_choice == "scissors" and comp_choice == "paper"):
            result = "You win!"
            color = "#2ecc71"  # Green
            self.user_score += 1
        else:
            result = "Computer wins!"
            color = "#e74c3c"  # Red
            self.comp_score += 1
        
        # Update UI
        self.result_label.config(text=result, fg=color)
        self.score_label.config(text=f"You: {self.user_score}  Computer: {self.comp_score}")
        self.play_again_btn.config(state=tk.NORMAL)
    
    def reset_game(self):
        # Clear displays
        self.user_display.config(text="")
        self.comp_display.config(text="")
        self.result_label.config(text="")
        
        # Enable buttons
        self.play_again_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    game = VisualRPSGame(root)
    root.mainloop()