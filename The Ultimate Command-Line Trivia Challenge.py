import requests
import random
import html

response = requests.get("https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple").json()
questions = response['results'] 

score = 0
for i, q in enumerate(questions, 1):
    print(f" Question {i}: {html.unescape(q['question'])} ")
    options = (f"A.{q['incorrect_answers'][0]}     B.{q['incorrect_answers'][1]} \n C.{q['incorrect_answers'][2]}     D.{q['correct_answer']}")
    print(options)
    answer = input(" Your answer: \n").strip().upper()

    if answer == 'D':
        print(" Correct! \n")
    else: 
        print(f" Wrong! \n")

    score += (answer == 'D')
    

print(f" You score {score} out of 10. ")

