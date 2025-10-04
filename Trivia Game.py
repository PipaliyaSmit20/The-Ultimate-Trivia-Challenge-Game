import requests
import random
import html

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

    response = requests.get(f"https://opentdb.com/api.php?amount={settings['amount']}&category={settings['category']}&difficulty={settings['difficulty']}&type=multiple").json()
    
    try:
        questions = response['results']
        if response['response_code'] != 0:
            print(" No questions available for the selected category and difficulty. Please try again.")
            return None
        return questions
    except KeyError:
        print(" Error fetching questions. Please try again later.")
        return None 
    
    
    return questions
def run_quiz(questions):
    score = 0
    print()
    print(" Let's begin the quiz! \n")
    for i, q in enumerate(questions, 1):
        print(f" Question {i}: {html.unescape(q['question'])} ")

        options = q['incorrect_answers']
        correct_answer = html.unescape(q['correct_answer'])
        options.append(correct_answer)
        random.shuffle(options)

        option_letter = ['A', 'B', 'C', 'D']
        for letter, option in zip(option_letter, options):
            print(f"  {letter}. {html.unescape(option)} ")
        correct_letter = option_letter[options.index(correct_answer)]
        answer = input(" Your answer: ").strip().upper()
        print()

        if answer == correct_letter:
            print(" Correct! \n")
            score += 1
        else: 
            print(f" Wrong! The correct answer was {correct_letter}.{correct_answer} \n")
    
    print(" Quiz Over! \n")
    print(f" You score {score} out of {len(questions)}. ")

def main():
    print("\n Welcome to The Ultimate Command-Line Trivia Challenge! \n")
    print(" It's great way to test your knowledge! \n")

    settings = get_game_settings()
    questions_list = fetch_questions(settings)
    if questions_list:
        run_quiz(questions_list)
if __name__ == "__main__":
    main()