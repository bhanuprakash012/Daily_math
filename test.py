import random

def generate_math_quiz():
    # Configuration for each type
    types = [
        ("1) Single digit number addition", (1, 2)),
        ("2) Single digit addition of 5", (1, 5)),
        ("3) Double digit addition", (2, 2)),
        ("4) Double digit addition of 5", (2, 5)),
        ("5) 3-digit + 2-digit addition", "3+2"),
        ("6) 3-digit addition", (3, 2))
    ]

    all_answers = []

    for label, config in types:
        print(f"--- {label} ---")
        category_answers = []
        
        for i in range(1, 6):
            if config == "3+2":
                num1 = random.randint(100, 999)
                num2 = random.randint(10, 99)
                numbers = [num1, num2]
            else:
                digits, count = config
                start = 10**(digits-1) if digits > 1 else 1 # Ensure single digits include 1-9
                end = (10**digits) - 1
                numbers = [random.randint(start, end) for _ in range(count)]
            
            # Create the question string and calculate sum
            question_text = " + ".join(map(str, numbers))
            total = sum(numbers)
            
            print(f"{i}. {question_text} = _______")
            category_answers.append(f"{i}. {total}")
        
        all_answers.append((label, category_answers))
        print()

    # Print the Answer Key Section
    print("=" * 30)
    print("         ANSWER KEY")
    print("=" * 30)
    for label, answers in all_answers:
        print(f"\n{label}:")
        # Print answers in a single line for compactness
        print("  |  ".join(answers))

if __name__ == "__main__":
    generate_math_quiz()