import json
import time
import os
import random
import keyboard

exit_flag = False

def set_exit_flag():
    global exit_flag
    exit_flag = True
keyboard.add_hotkey('ctrl+q', set_exit_flag)
def load_words_from_json(category):
    with open('words.json', 'r') as f:
        words_dict = json.load(f)
    words = words_dict[category]
    return words
def update_leaderboard(leaderboard, user_data, category):
    user_data['category'] = category
    leaderboard.append(user_data)
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    with open('leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

def show_leaderboard():
    with open('leaderboard.json', 'r') as f:
        leaderboard = json.load(f)
        print("Leaderboard:")
    for i, data in enumerate(leaderboard, start=1):
        category = data.get('category', 'Unknown')
        print(f"{i}. {data['name']} - {data['score']} words per minute - (Category: {category})")

def load_leaderboard():
    if os.path.exists('leaderboard.json') and os.path.getsize('leaderboard.json') > 0:
        with open('leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    else:
        leaderboard = []
    return leaderboard



def load_words_from_json(category):
    with open('words.json', 'r') as f:
        words_dict = json.load(f)
    words = words_dict[category]
    
    return words

def get_user_input(prompt):
    return input(prompt)
def main():
    username = get_user_input("Enter your username: ")
    leaderboard = load_leaderboard()
    categories = {
        '1': 'C',
        '2': 'Python',
        '3': 'Java',
        '4': 'JavaScript',
        '5': 'Ruby',
        '6': 'C++',
        '7': 'Go',
        '8': 'C#',
        '9': 'TypeScript',
        '10': 'Rust'
    }
    while True:
        if exit_flag:
            print("Exiting...")
       
        print("1. Start typing test")
        print("2. Show leaderboard")
        print("3. Exit")
        option = get_user_input("Choose an option: ")
        if option == '1':
            print("Choose a category:")
            for number, category in categories.items():
                print(f"{number}. {category}")
            category_number = get_user_input("Enter the number for your chosen category: ")
            category = categories[category_number]
            num_words = int(get_user_input("Enter the number of words to practice (1-200): "))
            words = load_words_from_json(category)
            words = random.sample(words, num_words)
            num_words_typed = 0
            words_per_minute = 0
            total_time = 0
            for word in words:
                print(f"Type this word: {word}")
                start_time = time.time()
                user_input = get_user_input("Your input: ")
                end_time = time.time()
                if user_input == word:
                    time_taken = end_time - start_time
                    total_time += time_taken
                    words_per_minute = (60 / time_taken)
                    print(f"Correct! Your time was: {time_taken} seconds. Words per minute: {words_per_minute}")
                    num_words_typed += 1
                else:
                    print("Incorrect! The correct word was: " + word)

            average_wpm = (num_words_typed * 60) / total_time if total_time > 0 else 0
            update_leaderboard(leaderboard, {'name': username, 'score': words_per_minute}, category)
            print(f"Typing Metrics for {username}:")
            print(f"Words Typed: {num_words_typed}")
            print(f"Time Taken: {total_time} seconds")
            print(f"Words Per Minute: {average_wpm}")
            print("Press any key to continue...")
        elif option == '2':
            show_leaderboard()
        elif option == '3':
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
