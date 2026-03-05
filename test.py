import random
from datetime import datetime

def generate_quiz_html():
    categories = [
        ("1) Single digit number addition", 1, 2),
        ("2) Single digit addition of 5", 1, 5),
        ("3) Double digit addition", 2, 2),
        ("4) Double digit addition of 5", 2, 5),
        ("5) 3-digit + 2-digit addition", "3+2", 2),
        ("6) 3-digit addition", 3, 2)
    ]

    quiz_html = ""
    timestamp = datetime.now().strftime("%B %d, %Y - %H:%M:%S")

    for label, digit_type, count in categories:
        quiz_html += f"<h3>{label}</h3><ol>"
        
        for _ in range(5):
            if digit_type == "3+2":
                num1 = random.randint(100, 999)
                num2 = random.randint(10, 99)
                numbers = [num1, num2]
            else:
                start = 10**(digit_type - 1) if digit_type > 1 else 1
                end = (10**digit_type) - 1
                numbers = [random.randint(start, end) for _ in range(count)]

            question_text = " + ".join(map(str, numbers))
            answer = sum(numbers)
            
            # Feature: Added a span for the answer and a tiny button for each question
            quiz_html += f"""
            <li>
                {question_text} = <span class="answer-box">_______</span>
                <span class="actual-answer" style="display:none;">{answer}</span>
                <button class="reveal-btn" onclick="revealSingle(this)">Ans</button>
            </li>"""
        
        quiz_html += "</ol>"

    # Final HTML Construction with Interactive Features
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Math Quiz</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background-color: #f9f9f9; }}
            .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ border-bottom: 3px solid #4CAF50; color: #2E7D32; padding-bottom: 10px; }}
            h3 {{ background: #e8f5e9; padding: 10px; border-left: 5px solid #4CAF50; border-radius: 4px; color: #2E7D32; margin-top: 25px; }}
            li {{ margin-bottom: 15px; font-weight: bold; font-size: 1.2em; list-style-position: inside; }}
            .answer-box {{ color: #ccc; }}
            .actual-answer {{ color: #d32f2f; font-weight: 800; border-bottom: 2px solid #d32f2f; margin-right: 10px; }}
            .reveal-btn {{ background: #eee; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; font-size: 0.7em; padding: 2px 8px; vertical-align: middle; }}
            .reveal-btn:hover {{ background: #ddd; }}
            .controls {{ margin: 20px 0; display: flex; gap: 10px; }}
            .main-btn {{ padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }}
            .btn-print {{ background: #2196F3; color: white; }}
            .btn-toggle {{ background: #4CAF50; color: white; }}
            
            /* Print View Optimization */
            @media print {{
                .reveal-btn, .controls, .footer {{ display: none !important; }}
                body {{ background: white; margin: 0; padding: 0; }}
                .container {{ box-shadow: none; border: none; width: 100%; }}
                .actual-answer {{ display: none !important; }} /* Hide answers when printing worksheet */
                .answer-box {{ display: inline !important; color: #000; }}
            }}
            
            .footer {{ margin-top: 50px; font-size: 0.8em; color: #888; text-align: center; border-top: 1px solid #ddd; padding-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 Daily Math Practice</h1>
            <p><strong>Generated on:</strong> {timestamp}</p>
            
            <div class="controls">
                <button class="main-btn btn-toggle" onclick="toggleAll()">Show All Answers</button>
                <button class="main-btn btn-print" onclick="window.print()">Print Worksheet</button>
            </div>

            <div class="quiz-section">
                {quiz_html}
            </div>

            <div class="footer">
                Generated automatically by your Python Script & GitHub Actions.
            </div>
        </div>

        <script>
            function revealSingle(btn) {{
                const answer = btn.previousElementSibling;
                const box = answer.previousElementSibling;
                answer.style.display = "inline";
                box.style.display = "none";
                btn.style.display = "none";
            }}

            function toggleAll() {{
                const answers = document.querySelectorAll('.actual-answer');
                const boxes = document.querySelectorAll('.answer-box');
                const buttons = document.querySelectorAll('.reveal-btn');
                const mainBtn = document.querySelector('.btn-toggle');
                
                const isHidden = answers[0].style.display === "none";
                
                answers.forEach(a => a.style.display = isHidden ? "inline" : "none");
                boxes.forEach(b => b.style.display = isHidden ? "none" : "inline");
                buttons.forEach(bt => bt.style.display = isHidden ? "none" : "inline");
                
                mainBtn.innerText = isHidden ? "Hide All Answers" : "Show All Answers";
            }}
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Successfully generated index.html with Interactive Features!")

if __name__ == "__main__":
    generate_quiz_html()
