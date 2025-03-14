import requests
import csv
import os
import random

def get_word(category):
    api_urls = {
        "fruits": "https://orsu.io/fruits.json",
        "vegetables": "https://orsu.io/vegetables.json",
        "animals": "https://orsu.io/animals.json",
        "movies": "https://orsu.io/movies.json",
        "programming_languages": "https://orsu.io/programming_languages.json"
    }

    response = requests.get(api_urls[category])
    if response.status_code == 200:
        data = response.json()
        chosen_item = random.choice(data)
        return chosen_item["name"].upper(), chosen_item["hint"]
    else:
        print("Failed to fetch data. Check your internet connection.")
        exit()

def display_hangman(attempts):
    stages = [
        """
           ----
           |  |
           |  O
           | /|\\
           | / \\
           |
        """,
        """
           ----
           |  |
           |  O
           | /|\\
           | /
           |
        """,
        """
           ----
           |  |
           |  O
           | /|\\
           |
           |
        """,
        """
           ----
           |  |
           |  O
           | /|
           |
           |
        """,
        """
           ----
           |  |
           |  O
           |  |
           |
           |
        """,
        """
           ----
           |  |
           |  O
           |
           |
           |
        """,
        """
           ----
           |  |
           |
           |
           |
           |
        """
    ]
    print(stages[6 - attempts])

def play_game(player_name, category):
    word, hint = get_word(category)
    guessed_letters = set()
    attempts = 6  # Traditional hangman style

    print(f"\nHint: {hint}")

    while attempts > 0:
        print("\nWord:", " ".join([letter if letter in guessed_letters else "_" for letter in word]))
        display_hangman(attempts)
        guess = input("Guess a letter: ").upper()

        if len(guess) != 1 or not guess.isalpha():
            print("Invalid input. Please enter a single letter.")
            continue

        if guess in guessed_letters:
            print("You already guessed that letter!")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("Good job! That letter is in the word.")
            if all(letter in guessed_letters for letter in word):
                print(f"🎉 Congratulations, {player_name}! You guessed the word: {word}")
                save_score(player_name, category, "Won")
                return
        else:
            attempts -= 1
            print("Wrong guess!")

    print(f"Game over! The correct word was {word}.")
    save_score(player_name, category, "Lost")

def save_score(player_name, category, result):
    score_file = "scores.csv"
    file_exists = os.path.exists(score_file)

    with open(score_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player", "Category", "Result"])
        writer.writerow([player_name, category, result])
    print("✅ Score saved successfully!")

def main():
    while True:
        player_name = input("Enter your name: ")
        print("Choose a category: \n1. Fruits\n2. Vegetables\n3. Animals\n4. Movies\n5. Programming Languages")
        category_choice = input("Enter the number of your choice: ")
        category_map = {"1": "fruits", "2": "vegetables", "3": "animals", "4": "movies", "5": "programming_languages"}
        category = category_map.get(category_choice, "fruits")

        play_game(player_name, category)

        while True:
            next_step = input("\n1. Try again\n2. New player\n3. Exit\nChoose an option: ")
            if next_step == "1":
                play_game(player_name, category)
            elif next_step == "2":
                break
            elif next_step == "3":
                print("Thanks for playing! See you next time! 👋")
                exit()
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
