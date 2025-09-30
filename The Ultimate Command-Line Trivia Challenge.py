import requests
import random
import html

try:
    print("\n Welcome to The Ultimate Command-Line Trivia Challenge! \n")
    print(" It's great way to test your knowledge! \n")
    print(" Let's get started! \n") 
    try:
        question_number = int(input(" How many questions would you like to answer? (1-50): "))

        if not (1 <= question_number <= 50):
            print("Please enter a number between 1 and 50.")
            exit()
    except:
        print("Invalid input. Please enter a valid number for questions.")
        exit()
    print()

    category_dict = {
        "general knowledge": 9,
        "entertainment": 10,
        "science": 17,
        "sports": 21,
        "geography": 22
    }
    Category = str(input(" Choose a category (General Knowledge, Entertainment, Science, Sports, Geography): ")).strip().lower()
    if Category in category_dict:
            category_id = category_dict[Category]
    print()
     
    difficulty = str(input(" Choose a difficulty (easy, medium, hard): ")).strip().lower()

    response = requests.get(f"https://opentdb.com/api.php?amount={question_number}&category={category_id}&difficulty={difficulty}&type=multiple").json()
    questions = response['results']
    if not questions:
        print("No questions available for the selected category and difficulty. Please try again.")
        exit()

    score = 0

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
    

    print(f" You score {score} out of {len(questions)}. ")
except Exception as e:
    print(f"Error fetching questions: {e}")
