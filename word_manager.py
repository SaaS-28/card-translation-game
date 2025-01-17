import random

class WordManager:

    def __init__(self, word_file):
        self.words = []
        self.load_words(word_file)

    def load_words(self, word_file):
        with open(word_file, 'r') as file:
            for line in file:
                word, rest = line.split('=')
                translations = [t.strip() for t in rest.strip().split('-') if t.strip() != word.strip()]

                # Trova l'indice di '/' e separa traduzioni da esempi
                index = rest.find('/')
                if index != -1:
                    translations_part, examples_part = rest.split('/', 1)
                    translations = [t.strip() for t in translations_part.strip().split('-') if t.strip() != word.strip()]
                    examples = examples_part.strip().split('.')
                else:
                    examples = []

                self.words.append((word.strip(), translations, examples))

    def get_next_word(self):
        if self.words:
            random_index = random.randint(0, len(self.words) - 1) 
            word, all_translations, examples = self.words.pop(random_index)
            return word, all_translations, examples
        else:
            return None, [], []