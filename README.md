# Python translation game

In this game, you can **create profiles** for the languages you want to learn and **upload lists of words** to translate. 
You can also **update the profile name** or **re-upload the word lists** at any time.

## How to Play:

- On the home screen, click on a profile name to start.
- A word will appear that you need to translate.
- If you translate the word correctly, the panel showing the word will flip and turn green.
- If you get it wrong three times in a row, the panel will turn red.
- For words with multiple translations, all valid translations will be displayed below the panel.

## Project structure

The project is composed by **five python files** and **one json file**:

- **main.py**: main file used to run the game.
- **ui.py**: handles all the graphic elements in the game.
- **game.py**: handles all the backend logic in the game.
- **word_manger.py**: handles the logic for loading the words or getting new ones for th game.
- **player.py**: handles the logic of the player (attempts only by now).
- **profiles.json**: used to save all the profiles the user want to use using the following **format**: "Word to translate" = "translation" - "translation2" - ... - "translationN" / Examples: "Example".

In the pytohn files i use **classes** to correctly manage all the interactions between all the files.
