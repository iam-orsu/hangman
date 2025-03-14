import requests
import random
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API URLs stored in .env
API_URLS = {
    "1": ("Fruits", os.getenv("FRUITS_API")),
    "2": ("Animals", os.getenv("ANIMALS_API")),
    "3": ("Movies", os.getenv("MOVIES_API")),
    "4": ("Programming Languages", os.getenv("PROGRAMMING_API")),
}

SCORE_FILE = "scores.csv"

def fetch_word():
    """Fetch a word from the selected category."""
    print("\nChoose a category:")
    for key, value in API_URLS.items():
        print(f"{key}. {value[0]}")

    choice = input("Enter your choice (1-4): ").strip()
    category_name, url = API_URLS.get(choice, API_URLS["1"])  # Default to Fruits

    response = requests.get(url)
    if response.status_code == 200:
        words = response.json()
        chosen_word = random.choice(words)
        return category_name, chosen_word["name"].upper(), chosen_word["hint"]
    else:
        print("Failed to fetch data. Check your internet connection.")
        exit()

def save_score(player_name, category, result):
    """Save the score in a CSV file."""
    file_exists = os.path.exists(SCORE_FILE)
    with open(SCORE_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Player", "Category", "Result"])
        writer.writerow([player_name, category, result])

def play_game():
    """Main function to play Hangman."""
    player_name = input("\nEnter your name: ").strip()
    category, word, hint = fetch_word()
    attempts = 10
    guessed_letters = set()

    print(f"\nWelcome, {player_name}! You chose {category}. You have {attempts} attempts.")
    print("\nHint:", hint)

    while attempts > 0:
        display_word = " ".join([letter if letter in guessed_letters else "_" for letter in word])
        print("\nWord:", display_word)

        guess = input("Guess a letter: ").strip().upper()

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

def main():
    """Game menu loop."""
    while True:
        play_game()
        print("\n1. Try Again")
        print("2. New Player")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            continue
        elif choice == "2":
            os.execlp("python", "python", __file__)  # Restart script for a new player
        elif choice == "3":
            print("Thanks for playing! See you next time! 👋")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
