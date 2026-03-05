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
    total_questions = len(categories) * 5

    for idx, (label, digit_type, count) in enumerate(categories):
        quiz_html += f"""
        <div class="section" id="section-{idx}">
            <div class="section-header">
                <h3>{label}</h3>
                <div class="section-stats">
                    Score: <span id="score-{idx}">0</span>/5 | 
                    Time: <span id="time-{idx}">0s</span>
                </div>
            </div>
            <ol>"""
        
        for q_idx in range(5):
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
            
            quiz_html += f"""
            <li>
                {question_text} = 
                <input type="number" 
                       class="user-input" 
                       data-section="{idx}" 
                       data-qidx="{q_idx}"
                       onfocus="startSectionTimer({idx})"
                       onchange="checkAnswer(this, {answer})" 
                       placeholder=" ">
                <span class="actual-answer" style="display:none; color: #d32f2f; margin-left:10px;">({answer})</span>
                <button class="reveal-btn" onclick="revealSingle(this)">Ans</button>
            </li>"""
        
        quiz_html += "</ol></div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Math Quiz - Precision Training</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background-color: #f0f2f5; }}
            .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            h1 {{ border-bottom: 3px solid #4CAF50; color: #2E7D32; margin-bottom: 5px; }}
            
            .section {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 25px; padding: 15px; transition: 0.3s; }}
            .section-header {{ display: flex; justify-content: space-between; align-items: center; background: #e8f5e9; padding: 5px 15px; border-radius: 6px; margin-bottom: 10px; }}
            .section-stats {{ font-weight: bold; color: #2E7D32; font-size: 0.9em; }}
            .section.complete {{ border: 2px solid #4CAF50; background-color: #fafffa; }}
            
            .stats-bar {{ background: #333; color: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; display: flex; justify-content: space-between; }}
            .user-input {{ width: 80px; padding: 5px; border: 2px solid #ccc; border-radius: 4px; font-size: 1em; text-align: center; }}
            .correct {{ border-color: #4CAF50 !important; background-color: #e8f5e9; }}
            .incorrect {{ border-color: #f44336 !important; background-color: #ffebee; }}
            
            .controls {{ margin: 20px 0; display: flex; gap: 10px; }}
            .main-btn {{ padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; color: white; }}
            .btn-toggle {{ background: #4CAF50; }}
            .btn-reset {{ background: #f44336; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 Daily Math Practice</h1>
            <p><strong>Generated:</strong> {timestamp}</p>
            
            <div class="stats-bar">
                <span>Total Score: <span id="total-score">0</span> / {total_questions}</span>
                <span id="overall-status">Take your time between sections!</span>
            </div>

            <div class="controls">
                <button class="main-btn btn-toggle" onclick="toggleAll()">Show Answers</button>
                <button class="main-btn btn-reset" onclick="resetWorksheet()">Reset All</button>
                <button class="main-btn btn-print" onclick="window.print()">Print Worksheet</button>
            </div>

            <div class="quiz-section">
                {quiz_html}
            </div>
        </div>

        <script>
            let sectionTimers = {{}}; 
            let sectionIntervals = {{}};

            function startSectionTimer(sId) {{
                // Only start if not already running and not previously finished
                if (!sectionIntervals[sId]) {{
                    sectionTimers[sId] = 0;
                    sectionIntervals[sId] = setInterval(() => {{
                        sectionTimers[sId]++;
                        document.getElementById('time-' + sId).innerText = sectionTimers[sId] + "s";
                    }}, 1000);
                }}
            }}

            function checkAnswer(input, correct) {{
                const sId = input.getAttribute('data-section');
                const qIdx = input.getAttribute('data-qidx');

                if (input.value == "") {{
                    input.classList.remove('correct', 'incorrect');
                }} else if (parseInt(input.value) === correct) {{
                    input.classList.add('correct');
                    input.classList.remove('incorrect');
                }} else {{
                    input.classList.add('incorrect');
                    input.classList.remove('correct');
                }}

                updateScores(sId);

                // If it's the last question of the section (Index 4)
                if (qIdx == "4") {{
                    if (input.value !== "") {{
                        clearInterval(sectionIntervals[sId]);
                        sectionIntervals[sId] = "FINISHED";
                        document.getElementById('section-' + sId).classList.add('complete');
                    }}
                    // DO NOT jump to the next input if we just finished a section
                    return; 
                }}

                // Otherwise, focus jump to the next input in the SAME section
                const allInputs = Array.from(document.querySelectorAll('.user-input'));
                const currentIndex = allInputs.indexOf(input);
                if (currentIndex < allInputs.length - 1) {{
                    allInputs[currentIndex + 1].focus();
                }}
            }}

            function updateScores(sId) {{
                const sectionCorrect = document.querySelectorAll('#section-' + sId + ' .user-input.correct').length;
                document.getElementById('score-' + sId).innerText = sectionCorrect;

                const totalCorrect = document.querySelectorAll('.user-input.correct').length;
                document.getElementById('total-score').innerText = totalCorrect;
            }}

            function resetWorksheet() {{
                if(confirm("This will reset all timers and scores. Continue?")) {{
                    location.reload();
                }}
            }}

            function revealSingle(btn) {{
                const ans = btn.previousElementSibling;
                ans.style.display = "inline";
                btn.style.display = "none";
            }}

            function toggleAll() {{
                const answers = document.querySelectorAll('.actual-answer');
                const isHidden = answers[0].style.display === "none";
                answers.forEach(a => a.style.display = isHidden ? "inline" : "none");
            }}
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Successfully generated!")

if __name__ == "__main__":
    generate_quiz_html()
