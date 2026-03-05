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
            
            # Feature: Input box + Check Logic
            quiz_html += f"""
            <li>
                {question_text} = 
                <input type="number" class="user-input" onchange="checkAnswer(this, {answer})" placeholder="?">
                <span class="actual-answer" style="display:none; color: #d32f2f; margin-left:10px;">({answer})</span>
                <button class="reveal-btn" onclick="revealSingle(this)">Ans</button>
            </li>"""
        
        quiz_html += "</ol>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Daily Math Quiz Pro</title>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background-color: #f0f2f5; }}
            .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); position: relative; }}
            h1 {{ border-bottom: 3px solid #4CAF50; color: #2E7D32; }}
            h3 {{ background: #e8f5e9; padding: 10px; border-left: 5px solid #4CAF50; border-radius: 4px; }}
            
            /* Input Styling */
            .user-input {{ width: 80px; padding: 5px; border: 2px solid #ccc; border-radius: 4px; font-size: 1em; text-align: center; }}
            .correct {{ border-color: #4CAF50 !important; background-color: #e8f5e9; }}
            .incorrect {{ border-color: #f44336 !important; background-color: #ffebee; }}
            
            /* Widgets Styling */
            #widget-panel {{ position: fixed; top: 20px; right: 20px; background: #333; color: white; padding: 15px; border-radius: 8px; width: 180px; display: none; z-index: 1000; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
            .widget-btn {{ background: #555; border: none; color: white; padding: 5px; cursor: pointer; border-radius: 3px; font-size: 0.8em; margin: 2px; }}
            .widget-display {{ font-family: monospace; font-size: 1.4em; text-align: center; margin: 10px 0; color: #4CAF50; }}
            
            .controls {{ margin: 20px 0; display: flex; gap: 10px; flex-wrap: wrap; }}
            .main-btn {{ padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; color: white; }}
            .btn-print {{ background: #2196F3; }}
            .btn-toggle {{ background: #4CAF50; }}
            .btn-widget {{ background: #673AB7; }}

            @media print {{
                .controls, .reveal-btn, #widget-panel, .user-input, .footer {{ display: none !important; }}
                .actual-answer {{ display: none !important; }}
                body {{ background: white; }}
                .container {{ box-shadow: none; }}
            }}
            .footer {{ margin-top: 40px; text-align: center; font-size: 0.8em; color: #888; }}
        </style>
    </head>
    <body>
        <div id="widget-panel">
            <div style="font-size: 0.9em; border-bottom: 1px solid #555; padding-bottom: 5px;">Timer / Stopwatch</div>
            <div id="timer-display" class="widget-display">00:00</div>
            <div style="text-align:center;">
                <button class="widget-btn" onclick="startStopwatch()">Start SW</button>
                <button class="widget-btn" onclick="startTimer(5)">Timer 5m</button>
                <button class="widget-btn" onclick="resetWidget()" style="background:#f44336;">Reset</button>
            </div>
        </div>

        <div class="container">
            <h1>🧮 Daily Math Practice</h1>
            <p>Generated on: {timestamp}</p>
            
            <div class="controls">
                <button class="main-btn btn-toggle" onclick="toggleAll()">Show All Answers</button>
                <button class="main-btn btn-widget" onclick="toggleWidget()">Toggle Timer Tool</button>
                <button class="main-btn btn-print" onclick="window.print()">Print Mode</button>
            </div>

            <div class="quiz-section">
                {quiz_html}
            </div>

            <div class="footer">
                Automated Math Quiz Generator
            </div>
        </div>

# Replace the <script> section in your test.py with this:
        <script>
            let timerInterval;
            let seconds = 0;

            function checkAnswer(input, correct) {
                if (input.value == "") {
                    input.classList.remove('correct', 'incorrect');
                    return;
                }
                
                // 1. Check if correct
                if (parseInt(input.value) === correct) {
                    input.classList.add('correct');
                    input.classList.remove('incorrect');
                } else {
                    input.classList.add('incorrect');
                    input.classList.remove('correct');
                }

                // 2. Jump to next question
                // Find all inputs on the page
                const allInputs = Array.from(document.querySelectorAll('.user-input'));
                const currentIndex = allInputs.indexOf(input);
                
                // If there is a next input, move the cursor there
                if (currentIndex < allInputs.length - 1) {
                    allInputs[currentIndex + 1].focus();
                }
            }

            // Keep your existing timer/stopwatch functions below...
            function revealSingle(btn) {
                const ans = btn.previousElementSibling;
                ans.style.display = "inline";
                btn.style.display = "none";
            }

            function toggleAll() {
                const answers = document.querySelectorAll('.actual-answer');
                const isHidden = answers[0].style.display === "none";
                answers.forEach(a => a.style.display = isHidden ? "inline" : "none");
            }

            function toggleWidget() {
                const panel = document.getElementById('widget-panel');
                panel.style.display = (panel.style.display === 'block') ? 'none' : 'block';
            }

            function formatTime(s) {
                let mins = Math.floor(s / 60);
                let secs = s % 60;
                return (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
            }

            function startStopwatch() {
                resetWidget();
                timerInterval = setInterval(() => {
                    seconds++;
                    document.getElementById('timer-display').innerText = formatTime(seconds);
                }, 1000);
            }

            function startTimer(minutes) {
                resetWidget();
                seconds = minutes * 60;
                document.getElementById('timer-display').innerText = formatTime(seconds);
                timerInterval = setInterval(() => {
                    seconds--;
                    document.getElementById('timer-display').innerText = formatTime(seconds);
                    if (seconds <= 0) {
                        clearInterval(timerInterval);
                        alert("Time is up!");
                    }
                }, 1000);
            }

            function resetWidget() {
                clearInterval(timerInterval);
                seconds = 0;
                document.getElementById('timer-display').innerText = "00:00";
            }
        </script>
    </body>
    </html>
    """

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Successfully generated!")

if __name__ == "__main__":
    generate_quiz_html()

