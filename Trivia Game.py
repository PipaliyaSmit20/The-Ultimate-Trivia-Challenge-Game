import requests
import random
import html
import sys 
import csv

def get_game_settings():
    settings = {}   

    while True: 
        try:
            question_number = int(input(" How many questions would you like to answer? (1-50): "))

            if  1 <= question_number <= 50:
                settings['amount'] = question_number
                break
            else:
                print(" Please choose a number between 1 and 50.")
        except ValueError:
            print("Invalid input. Please enter a valid number for questions.")
        
    print()

    category_dict = {
        "general knowledge": 9,
        "entertainment": 10,
        "science": 17,
        "sports": 21,
        "geography": 22
        }

    while True:
        Category = str(input(" Choose a category (General Knowledge, Entertainment, Science, Sports, Geography): ")).strip().lower()
        if Category in category_dict:       
            settings['category'] = category_dict[Category]
            break
        else:
            print("Invalid input. Please enter a valid category.")
    print()
    
    while True:
        diff_input = str(input(" Choose a difficulty (easy, medium, hard): ")).strip().lower()
        if diff_input in ['easy', 'medium', 'hard']:
            settings['difficulty'] = diff_input
            break
        else:
            print("Invalid input. Please enter 'easy', 'medium', or 'hard'.")
        
    return settings

def fetch_questions(settings):

    response = requests.get(f"https://opentdb.com/api.php?amount={settings['amount']}&category={settings['category']}&difficulty={settings['difficulty']}").json()
    
    try:
        questions = response['results']
        if response['response_code'] != 0:
            print(" No questions available for the selected category and difficulty. Please try again.")
            return None
        return questions
    except KeyError:
        print(" Error fetching questions. Please try again later.")
        return None 
    
def run_quiz(questions, hints_available):
    score = 0
    print()
    print(" Let's begin the quiz! \n")
    for i, q in enumerate(questions, 1):
        print(f"❓ Question {i}: {html.unescape(q['question'])} ")

        #    MULTIPLE CHOICE LOGIC 
        if q['type'] == 'multiple':
            options = q['incorrect_answers'][:] 
            correct_answer = html.unescape(q['correct_answer'])
            options.append(correct_answer)
            random.shuffle(options)

            while True: # Outer loop for handling hints
                option_letter = ['A', 'B', 'C', 'D'][:len(options)]
                for letter, option in zip(option_letter, options):
                    print(f"  {letter}. {html.unescape(option)} ")

                #  NEW: Inner loop for input validation 
                while True: 
                    hint_prompt = ""
                    if hints_available > 0:
                        hint_prompt = f" (or type 'hint' for a 50:50, {hints_available} left)"
                    
                    user_answer = input(f" Your answer{hint_prompt}: ").strip().upper()
                    
                    # Create a list of all valid inputs
                    valid_inputs = option_letter[:]
                    if hints_available > 0:
                        valid_inputs.append('HINT')

                    if user_answer in valid_inputs:
                        break # Exit validation loop if input is valid
                    else:
                        print(f"❌ Invalid input. Please enter one of the options: {', '.join(option_letter)}")

                # HINT LOGIC
                if user_answer == 'HINT' and hints_available > 0:
                    hints_available -= 1
                    print(f"💡 Hint used! You have {hints_available} hints left.")
                    incorrect_to_keep = random.choice(q['incorrect_answers'])
                    options = [correct_answer, incorrect_to_keep]
                    random.shuffle(options)
                    print("-" * 20)
                    continue
                
                # ANSWER CHECKING LOGIC
                correct_letter = option_letter[options.index(correct_answer)]
                if user_answer == correct_letter:
                    print("✅ Correct! \n")
                    score += 1
                else: 
                    print(f"❌ Wrong! The correct answer was {correct_letter}. {correct_answer} \n")
                break 

        #  TRUE/FALSE LOGIC 
        else:
            correct_answer = q['correct_answer']
            
            #  NEW: Loop for input validation
            while True:
                user_answer = input(" Your answer (True/False): ").strip().capitalize()
                if user_answer in ['True', 'False']:
                    break # Exit loop if input is valid
                else:
                    print("❌ Invalid input. Please enter 'True' or 'False'.")

            if user_answer == correct_answer:
                print("✅ Correct! \n")
                score += 1
            else: 
                print(f"❌ Wrong! The correct answer was {correct_answer}. \n")

    print("🎉 Quiz Over! 🎉\n")
    print(f"📊 You scored {score} out of {len(questions)}. ")

    return score, hints_available



def load_highscore():
    try:
        with open('Highscore.txt', 'r') as file:
                return int(file.read())

    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(new_highscore):
    with open('Highscore.txt', 'w') as file:
        file.write(str(new_highscore))
    
def main():
    print("\n Welcome to The Ultimate Command-Line Trivia Challenge! 🧠🎮\n")
    print(" It's great way to test your knowledge! \n")

    high_score = load_highscore()

    hints_available = 1

    while True:
        settings = get_game_settings()
        questions_list = fetch_questions(settings)
        if questions_list:
            current_score, hints_available = run_quiz(questions_list, hints_available)

            print(f"\nThe current high score is: {high_score}.")
            if current_score > high_score:
                print("🏆✨ Congratulations! You've set a new high score! ✨🏆")
                high_score = current_score
                save_highscore(high_score)
            
        play_again = input("🤔 Do you like to play again? (yes/no): ").strip().lower()
        if play_again != 'yes' and play_again != 'y':
            print("\n Thanks for playing! Goodbye! \n")
            break
        else:
            hints_available = 1
            print("=" * 50)

if __name__ == "__main__":
    main()