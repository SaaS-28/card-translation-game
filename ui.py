# ui.py
import tkinter as tk
from tkinter import filedialog
from game import Game
import os
import json

class GameUI:

    def __init__(self, master):
        self.master = master
        self.master.title("Language Learning Game")
        self.master.minsize(600, 400)

        self.backtext = None
        self.all_translations = None

        self.base_path = os.path.dirname(__file__)  # Getting the directory of the current file

        # Initializes the structure to memorize the profiles
        self.profiles = self.load_profiles()
        self.current_profile = None

        # Shows the initial window
        self.show_home_screen()

    # Loads the profiles from the "profile.json" file
    def load_profiles(self):
        if os.path.exists(self.base_path + "/profiles/profiles.json"):
            with open(self.base_path + "/profiles/profiles.json", "r") as f:
                return json.load(f)
        return {}

    # Delets a profile and update the "profile.json" file
    def delete_profile(self, profile_name):
        if profile_name in self.profiles:
            del self.profiles[profile_name]  # Delete the profile
            self.save_profiles()  # Update the file JSON
            self.show_home_screen()  # Reload the home page

    # Gets rid of all the widget in the window
    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

    # Saves the profile in the "profile.json" file
    def save_profiles(self):
        with open(self.base_path + "/profiles/profiles.json", "w") as f:
            json.dump(self.profiles, f)

    # Shows the home screen (here you can select or create a profile)
    def show_home_screen(self):
        self.clear_screen()
        self.master.unbind('<space>')
        self.master.unbind('<Return>')
        self.master.unbind('<Escape>')

        tk.Label(self.master, text="Card Traduction Game", font=("Helvetica", 24)).pack(pady=20)

        if not self.profiles:
            tk.Label(self.master, text="Create a profile to start learning.", font=("Helvetica", 16)).pack(pady=10)
            tk.Button(self.master, text="Create Profile", command=self.show_create_profile_screen, font=("Helvetica", 14)).pack(pady=5)
        else:
            tk.Label(self.master, text="Select a profile to continue learning.", font=("Helvetica", 16)).pack(pady=10)
            for profile_name in self.profiles.keys():
                profile_frame = tk.Frame(self.master)
                profile_frame.pack(pady=5)
                
                tk.Button(profile_frame, text=profile_name, command=lambda name=profile_name: self.select_profile(name), font=("Helvetica", 14)).pack(side="left", padx=10)
                tk.Button(profile_frame, text="Edit", command=lambda name=profile_name: self.show_edit_profile_screen(name), font=("Helvetica", 14)).pack(side="left", padx=10)
                tk.Button(profile_frame, text="Delete", command=lambda name=profile_name: self.delete_profile(name), font=("Helvetica", 14)).pack(side="left", padx=10)

            tk.Button(self.master, text="Create New Profile", command=self.show_create_profile_screen, font=("Helvetica", 14)).pack(pady=5)
        
        tk.Label(self.master, text="Press ENTER to check the translation", font=("Helvetica", 16)).pack(pady=(50, 5))
        tk.Label(self.master, text="Press SPACEBAR to pass on the next word", font=("Helvetica", 16)).pack(pady=(2, 2))
        tk.Label(self.master, text="Press ESC to return to the home screen", font=("Helvetica", 16)).pack(pady=(5, 50))

    # Shows the window used to create a new profile
    def show_create_profile_screen(self):
        self.clear_screen()

        tk.Label(self.master, text="Create New Profile", font=("Helvetica", 24)).pack(pady=20)
        tk.Label(self.master, text="Enter the language you want to learn:", font=("Helvetica", 14)).pack(pady=5)

        self.language_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.language_entry.pack(pady=5)
        self.language_entry.focus_set()

        vcmd = (self.master.register(self.validate_input), "%P")
        self.language_entry.config(validate="key", validatecommand=vcmd)

        tk.Button(self.master, text="Upload Word List", command=self.upload_word_list, font=("Helvetica", 14)).pack(pady=10)

        self.file_label = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.file_label.pack(pady=5)

        tk.Button(self.master, text="Save Profile", command=lambda: self.save_profile(False, None, None), font=("Helvetica", 14)).pack(pady=20)
        tk.Button(self.master, text="Back", command=self.show_home_screen, font=("Helvetica", 14)).pack(pady=5)

    # Shows the window used to modify the user profile
    def show_edit_profile_screen(self, name):
        self.clear_screen()

        tk.Label(self.master, text=f"Update The '{name}' Profile", font=("Helvetica", 24)).pack(pady=20)

        tk.Label(self.master, text="Enter the new namee for the profile:", font=("Helvetica", 14)).pack(pady=5)
        self.language_entry = tk.Entry(self.master, font=("Helvetica", 14))
        self.language_entry.pack(pady=5)
        self.language_entry.focus_set()

        vcmd = (self.master.register(self.validate_input), "%P")
        self.language_entry.config(validate="key", validatecommand=vcmd)

        tk.Button(self.master, text="Upload New Word List", command=self.upload_word_list, font=("Helvetica", 14)).pack(pady=10)

        self.file_label = tk.Label(self.master, text="", font=("Helvetica", 12))
        self.file_label.pack(pady=5)

        tk.Button(self.master, text="Save Profile", command=lambda: self.save_profile(True, self.language_entry.get() or name, name), font=("Helvetica", 14)).pack(pady=20)
        tk.Button(self.master, text="Back", command=self.show_home_screen, font=("Helvetica", 14)).pack(pady=5)

    def validate_input(self, value):
        if value.isalnum() or value == "":
            return True
        else:
            self.file_label.config(text="Only letters and numbers are allowed!!!", fg="red")
            return False

    # Upload the "words.txt" file
    def upload_word_list(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if not file_path.lower().endswith('.txt'):
                self.file_label.config(text="Make sure to upload only files with '.txt' extension!!!", fg="red")
            else:
                self.file_label.config(text=f"Uploaded: {file_path}", fg="black")
                self.word_list_path = file_path

    # Saves the profile created
    def save_profile(self, edit=False, name=None, previous_name=None):
        if not edit:
            language = self.language_entry.get()
        else:
            if name:
                language = name
            else:
                return  # Exit the function if no name is provided during edit

        if previous_name is not None:
            word_list = self.profiles[previous_name]["word_list"]

            # Delete the previous profile
            del self.profiles[previous_name]

            # Adds the new name by adding a new profile with the same word list 
            self.profiles[language] = {"word_list": word_list}
            
            self.save_profiles()
            self.show_home_screen()
        else:
            if language and hasattr(self, 'word_list_path'):
                self.profiles[language] = {"word_list": self.word_list_path}
                self.save_profiles()
                self.show_home_screen()
            else:
                self.file_label.config(text="Make sure to upload a list before saving the profile!!", fg="red")

    # Select an existing profile and start the game
    def select_profile(self, profile_name):
        self.current_profile = profile_name
        self.game = Game(self.profiles[profile_name]['word_list'])
        self.show_game_screen()

    # Shows the game screen
    def show_game_screen(self):
        self.clear_screen()
        self.master.title("Language Learning Game")

        # Set the minimum size of the window
        self.master.minsize(600, 400)

        self.game = Game('words.txt')
        
        # Frame for the layout
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20)

        # Canvas used to create the "animated" card
        self.canvas = tk.Canvas(self.frame, width=500, height=300, bg="gray")
        self.canvas.pack()

        # Word shown in the card
        self.word_label = self.canvas.create_text(250, 150, text="Word", font=("Helvetica", 36), fill="black", anchor="center")
        
        # Frame for input box and buttons
        self.input_frame = tk.Frame(self.master)
        self.input_frame.pack(pady=20)

        self.entry = tk.Entry(self.input_frame, font=("Helvetica", 18), width=30)
        self.entry.grid(row=0, column=0, padx=10)
        self.entry.focus_set()

        self.check_button = tk.Button(self.input_frame, text="Check", command=self.check_translation, bg="#4CAF50", fg="white", font=("Helvetica", 14))
        self.check_button.grid(row=0, column=1, padx=5)
        self.master.bind('<Return>', lambda event: self.check_translation())

        self.next_button = tk.Button(self.master, text="Next", command=self.load_next_word, state=tk.DISABLED, bg="#008CBA", fg="white", font=("Helvetica", 14))
        self.next_button.pack(pady=15)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=15)

        self.attempts_label = tk.Label(self.master, text="Attempts left: 3", font=("Helvetica", 16))
        self.attempts_label.pack(pady=10)

        self.all_tansalations_label = tk.Label(self.master, text="", font=("Helvetica", 16))
        self.all_tansalations_label.pack(pady=10)

        self.examples_label = tk.Label(self.master, text="", font=("Helvetica", 14), wraplength=500)
        self.examples_label.pack(pady=20)

        tk.Button(self.master, text="Go Back To The Home Screen", command=self.show_home_screen, font=("Helvetica", 14)).pack(pady=5)
        self.master.bind('<Escape>', lambda event: self.show_home_screen())

        self.load_next_word()

    # Load the next word
    def load_next_word(self):
        self.master.unbind('<space>')
        self.game.load_next_word()
        if not self.game.current_word:
            
            # Hide all the elements
            self.entry.grid_forget()  # Hiding input box
            self.check_button.grid_forget()  # Hiding "Check" button
            self.next_button.pack_forget()  # Hiding "Next" button
            
            # Hide all the labels
            self.result_label.pack_forget()  # Hiding "Result" label
            self.attempts_label.pack_forget()  # Hiding "Attempts" label
            self.examples_label.pack_forget()  # Hiding "Examples" label
            self.all_tansalations_label.pack_forget() # Hiding "Translations" label

            self.canvas.delete("all")
            self.canvas.config(bg="gray")
            self.canvas.create_text(250, 150, text="No more words!", font=("Helvetica", 36), fill="black", anchor="center")
            
            self.home_button = tk.Button(self.master, text="Return to home page", command=self.show_home_screen, font=("Helvetica", 14))
            self.home_button.pack(pady=10)

            self.play_again_button = tk.Button(self.master, text="Play again", command=self.play_again, font=("Helvetica", 14))
            self.play_again_button.pack(pady=10)

        else:

            # Cleaning the previous card
            self.canvas.delete("all")
            self.canvas.config(bg="gray")
            
            # Shows the word centered
            self.word_label = self.canvas.create_text(250, 150, text=self.game.current_word, font=("Helvetica", 36), fill="black", anchor="center")
            
            self.entry.delete(0, tk.END)
            self.result_label.config(text="")
            self.all_tansalations_label.config(text="")
            self.attempts_label.config(text=f"Attempts left: {self.game.player.max_attempts}")
            self.examples_label.config(text="")
            self.check_button.config(state=tk.NORMAL)
            self.master.bind('<Return>', lambda event: self.check_translation())
            self.next_button.config(state=tk.DISABLED)

    # Function used to play again
    def play_again(self):
        self.game.reset()  # Reset the game state
        self.load_next_word()  # Load the first word again

        # Remove the buttons and keep the game UI active
        self.home_button.pack_forget()
        self.play_again_button.pack_forget()
        self.show_game_screen()

    # First function used to simulate the animation of the card
    def animate_flip(self, is_correct):
        self.flip_step = 0
        self.flip_forward = True  # Direction of the animation
        self.flip_width = 500     # Initial width of the canvas
        self.is_correct = is_correct
        self.perform_flip()

    # Second function used to simulate the animation of the card
    def perform_flip(self):
        if self.flip_forward:
            self.flip_width -= 50  # Reducing width
        else:
            self.flip_width += 50  # Increasing width

        self.canvas.config(width=self.flip_width)
        self.canvas.delete("all")

        if self.flip_width <= 0 and self.flip_forward:

            # Changing the content on the back of the card
            if self.is_correct or self.game.player.attempts_left == 0:
                self.canvas.config(bg="green" if self.is_correct else "red")
            else:
                self.canvas.config(bg="gray")

            self.flip_forward = False  # Flipping the animation

        elif self.flip_width >= 500 and not self.flip_forward:
            # Animation completed
            if self.is_correct or self.game.player.attempts_left == 0:
                self.canvas.create_text(250, 150, text=self.backtext, font=("Helvetica", 36), fill="white", anchor="center")
                self.examples_label.config(text="".join(self.game.examples))
            else:
                self.canvas.create_text(250, 150, text=self.game.current_word, font=("Helvetica", 36), fill="black", anchor="center")

            # Updating text in the card
            if self.is_correct:
                self.result_label.config(text="Correct!", fg="green")
            elif self.game.player.attempts_left == 0:
                self.result_label.config(text=f"Out of attempts, the correct translation was: {self.backtext}", fg="red")

            if self.all_translations: self.all_tansalations_label.config(text=f"Other possible translations were: {', '.join(self.all_translations)}", fg="black")
            self.attempts_label.config(text=f"Attempts left: {self.game.player.attempts_left}")

            # Buttons management
            if self.is_correct or self.game.player.attempts_left == 0:
                self.check_button.config(state=tk.DISABLED)
                self.next_button.config(state=tk.NORMAL)
            else:
                self.check_button.config(state=tk.NORMAL)

            return  # Stopping the animation when it's completed

        # Going on with the animation
        self.master.after(50, self.perform_flip)

    # Function used to check the translation
    def check_translation(self):
        user_input = self.entry.get()
        correct, self.backtext, self.all_translations = self.game.check_translation(user_input)

        if correct:
            self.animate_flip(is_correct=True)
            self.game.player.attempts_left = self.game.player.max_attempts  # Restore the attempts if the translation is correct
            self.master.unbind('<Return>')
            self.master.bind('<space>', lambda event: self.load_next_word())
        else:
            if self.game.player.attempts_left > 0:
                self.attempts_label.config(text=f"Attempts left: {self.game.player.attempts_left}")
                self.result_label.config(text="Try again!", fg="orange")
                self.check_button.config(state=tk.DISABLED)
                self.master.after(1000, lambda: self.check_button.config(state=tk.NORMAL))
                if self.game.player.attempts_left == 0:
                    self.animate_flip(is_correct=False)
            else:
                self.master.unbind('<Return>')
                self.master.bind('<space>', lambda event: self.load_next_word())
                self.animate_flip(is_correct=False)

        if self.backtext in self.all_translations: self.all_translations.remove(self.backtext)
        print(self.all_translations)
        self.attempts_label.config(text=f"Attempts left: {self.game.player.attempts_left}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GameUI(root)
    root.mainloop()
