# player.py
class Player:

    # Initializes the player with a max number of attempts
    def __init__(self, max_attempts=3):
        self.max_attempts = max_attempts
        self.attempts_left = max_attempts

    # Restore the attempts
    def reset_attempts(self):
        self.attempts_left = self.max_attempts

    # Reduces by one the remaning attempts
    def decrease_attempts(self):
        self.attempts_left -= 1
