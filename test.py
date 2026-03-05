import random

def generate_math_quiz():
    """
    Generates a randomized math quiz with 5 questions per category
    and prints a formatted answer key at the end.
    """
    # Configuration: (Label, Digits, How many numbers to add)
    # Special case "3+2" handled in the logic loop
    categories = [
        ("1) Single digit number addition", 1, 2),
        ("2) Single digit addition of 5", 1, 5),
        ("3) Double digit addition", 2, 2),
        ("4) Double digit addition of 5", 2, 5),
        ("5) 3-digit + 2-digit addition", "3+2", 2),
        ("6) 3-digit addition", 3, 2)
    ]

    quiz_results = []

    print("========================================")
    print("           RANDOM MATH QUIZ             ")
    print("========================================\n")

    for label, digit_type, count in categories:
        print(f"--- {label} ---")
        category_answers = []

        for i in range(1, 6):
            if digit_type == "3+2":
                # Specific rule for 3-digit + 2-digit
                num1 = random.randint(100, 999)
                num2 = random.randint(10, 99)
                numbers = [num1, num2]
            else:
                # General rule based on digit length
                start = 10**(digit_type - 1) if digit_type > 1 else 1
                end = (10**digit_type) - 1
                numbers = [random.randint(start, end) for _ in range(count)]

            question_text = " + ".join(map(str, numbers))
            answer = sum(numbers)
            
            print(f"{i}. {question_text} = _______")
            category_answers.append(f"{i}. {answer}")
        
        quiz_results.append((label, category_answers))
        print() # Spacer between categories

    # --- ANSWER KEY SECTION ---
    print("========================================")
    print("              ANSWER KEY                ")
    print("========================================")
    
    for label, answers in quiz_results:
        print(f"\n{label}:")
        # Displays answers horizontally for a cleaner look
        print("  |  ".join(answers))

if __name__ == "__main__":
    generate_math_quiz()
