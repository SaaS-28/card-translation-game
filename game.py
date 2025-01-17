# game.py
import os
from word_manager import WordManager
from player import Player

class Game:

    # Initialize the game by loading the words from the file chosen by the player
    def __init__(self, word_file):

        # Getting the full path of the file
        base_path = os.path.dirname(__file__)
        full_path = os.path.join(base_path, word_file)

        # Initializing the WordManager with the full path
        self.word_manager = WordManager(full_path)
        self.player = Player()
        self.current_word = None
        self.current_translations = None

    # Loads the next word and reset the attempts of the player
    def load_next_word(self):
        self.current_word, self.current_translations, self.examples = self.word_manager.get_next_word()
        print(self.current_translations)
        self.player.reset_attempts()

    # Check if the translation given by the user is correct
    def check_translation(self, user_input):
        for translation in self.current_translations:
            if user_input.lower() == translation.lower():
                return True, user_input, self.current_translations
        self.player.decrease_attempts()
        return False, f"{self.current_translations[0]}", self.current_translations.copy()

    # Restore the game (attempts and word list)
    def reset(self):
        self.player.attempts_left = self.player.max_attempts
        self.load_next_word()  # Riprendi dal primo termine

    # Shows the examples associetes to the word
    def show_examples(self):
        print("", " / ".join(self.examples))
