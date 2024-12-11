import random

def choose_word():
    words = ["luqman", "fawwaz", "challenge", "programming", "development", "fayyadh", "badri", "khairil", "akim", "zarul"]
    return random.choice(words)

def display_hangman(tries):
    stages = [
        """
           ------
           |    |
           |    O
           |   /|\\
           |   / \\
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|\\
           |   /
           |
        """,
        """
           ------
           |    |
           |    O
           |   /|
           |   
           |
        """,
        """
           ------
           |    |
           |    O
           |    |
           |   
           |
        """,
        """
           ------
           |    |
           |    O
           |   
           |   
           |
        """,
        """
           ------
           |    |
           |    
           |   
           |   
           |
        """,
        """
           ------
           |    |
           |    
           |   
           |   
           |
        """,
    ]
    return stages[tries]

def play_hangman():
    word = choose_word()
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6

    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")

    while not guessed and tries > 0:
        guess = input("Please guess a letter or word: ").lower()

        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed that letter. Try again.")
            elif guess not in word:
                print("Oops! That letter is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job! That letter is in the word.")
                guessed_letters.append(guess)
                word_as_list = list(word_completion)
                indices = [i for i, letter in enumerate(word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)

                if "_" not in word_completion:
                    guessed = True

        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed that word. Try again.")
            elif guess != word:
                print("Oops! That is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word

        else:
            print("Invalid input. Please enter a letter or a word.")

        print(display_hangman(tries))
        print(word_completion)
        print("\n")

    if guessed:
        print("Congratulations! You've guessed the word!")
    else:
        print(f"Sorry, you've run out of tries. The word was '{word}'.")

if __name__ == "__main__":
    play_hangman()