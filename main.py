# main.py
from ui import GameUI
import tkinter as tk

def main():
    
    # Create the main window using tkinter
    root = tk.Tk()
    app = GameUI(root)  # Initialize the main class GameUI class with root window
    root.mainloop()  # Start the loop

if __name__ == "__main__":
    main()
