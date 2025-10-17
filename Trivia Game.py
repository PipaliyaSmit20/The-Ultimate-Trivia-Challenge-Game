import requests
import random
import html

def get_categories():
    print("Fetching categories...")
    try:
        response = requests.get("https://opentdb.com/api_category.php")
        response.raise_for_status()  # Raise an HTTPError 
        api_categories = response.json()['trivia_categories']
        return {cat['name'].lower(): cat['id'] for cat in api_categories}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching categories: {e}. Using a default list.")
        return {
            "general knowledge": 9,
            "entertainment: books": 10,
            "science & nature": 17,
            "sports": 21,
            "geography": 22
        }

def get_game_settings(category_dict):
    settings = {}

    # Get number of questions
    while True:
        try:
            question_number = int(input("How many questions would you like? (1-50): "))
            if 1 <= question_number <= 50:
                settings['amount'] = question_number
                break
            else:
                print("Please choose a number between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    print()

    # Get category
    print("Available Categories:")
    for category_name in category_dict.keys():
        print(f"- {category_name.title()}")

    while True:
        category_input = input("Choose a category: ").strip().lower()
        if category_input in category_dict:
            settings['category'] = category_dict[category_input]
            break
        else:
            print("Invalid category. Please choose from the list above.")
    print()

    # Get difficulty
    while True:
        diff_input = input("Choose a difficulty (easy, medium, hard): ").strip().lower()
        if diff_input in ['easy', 'medium', 'hard']:
            settings['difficulty'] = diff_input
            break
        else:
            print("Invalid input. Please enter 'easy', 'medium', or 'hard'.")

    return settings

def fetch_questions(settings):
    # Fetches questions from the API based on user settings.
    url = f"https://opentdb.com/api.php?amount={settings['amount']}&category={settings['category']}&difficulty={settings['difficulty']}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # API response_code 0 means success
        if data['response_code'] != 0:
            print("Could not retrieve questions for the selected settings. Please try a different category or difficulty.")
            return None
        return data['results']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching questions from the API: {e}")
        return None
    except KeyError:
        print("Received an unexpected format from the API. Please try again later.")
        return None

def run_quiz(questions, hints_available):
    score = 0
    print("\nLet's begin the quiz! 🚀\n")

    for i, q in enumerate(questions, 1):
        question_text = html.unescape(q['question'])
        correct_answer = html.unescape(q['correct_answer'])
        print(f"❓ Question {i}: {question_text}")

        # Multiple Choice Logic
        if q['type'] == 'multiple':
            options = [html.unescape(ans) for ans in q['incorrect_answers']]
            options.append(correct_answer)
            random.shuffle(options)
            
            hint_used = False
            while True: # Loop to allow for a hint retry
                option_letters = ['A', 'B', 'C', 'D']
                for letter, option in zip(option_letters, options):
                    print(f"  {letter}. {option}")

                # Input validation loop
                while True:
                    prompt = "Your answer: "
                    if hints_available > 0 and not hint_used:
                        prompt = f"Your answer (or type 'hint' for a 50:50, {hints_available} left): "
                    
                    user_answer = input(prompt).strip().upper()
                    
                    valid_inputs = option_letters[:len(options)]
                    if hints_available > 0 and not hint_used:
                        valid_inputs.append('HINT')

                    if user_answer in valid_inputs:
                        break
                    else:
                        print(f"❌ Invalid input. Please enter one of: {', '.join(option_letters[:len(options)])}")

                # Hint Logic
                if user_answer == 'HINT':
                    hints_available -= 1
                    hint_used = True
                    print(f"💡 Hint used! You have {hints_available} hints left.")
                    
                    # Remove two incorrect answers, keeping the correct one and one other
                    incorrect_to_remove = random.sample([opt for opt in options if opt != correct_answer], 2)
                    options = [opt for opt in options if opt not in incorrect_to_remove]
                    print("-" * 20)
                    continue # Re-display the question with fewer options

                # Answer Checking Logic
                chosen_option = options[option_letters.index(user_answer)]
                if chosen_option == correct_answer:
                    print("✅ Correct!\n")
                    score += 1
                else:
                    print(f"❌ Wrong! The correct answer was {correct_answer}.\n")
                break # Exit the hint loop and move to the next question

        # True/False Logic
        else:
            while True:
                user_answer = input("Your answer (True/False): ").strip().capitalize()
                if user_answer in ['True', 'False']:
                    break
                else:
                    print("❌ Invalid input. Please enter 'True' or 'False'.")

            if user_answer == correct_answer:
                print("✅ Correct!\n")
                score += 1
            else:
                print(f"❌ Wrong! The correct answer was {correct_answer}.\n")

    print("🎉 Quiz Over! 🎉\n")
    print(f"📊 You scored {score} out of {len(questions)}.")
    return score, hints_available

def load_highscore():
    try:
        with open('highscore.txt', 'r') as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(new_highscore):
    with open('highscore.txt', 'w') as file:
        file.write(str(new_highscore))

def main():
    print("\n🧠 Welcome to The Ultimate Command-Line Trivia Challenge! 🎮\n")
    
    high_score = load_highscore()
    category_dict = get_categories()

    while True:
        hints_available = 2 # Reset hints for each new game
        settings = get_game_settings(category_dict)
        questions_list = fetch_questions(settings)

        if questions_list:
            current_score, hints_available = run_quiz(questions_list, hints_available)
            print(f"\nThe current high score is: {high_score}.")
            if current_score > high_score:
                print("🏆✨ Congratulations! You've set a new high score! ✨🏆")
                high_score = current_score
                save_highscore(high_score)

        play_again = input("\n🤔 Play again? (yes/no): ").strip().lower()
        if play_again not in ('yes', 'y'):
            print("\nThanks for playing! Goodbye!\n")
            break
        else:
            print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()