import random
from datetime import datetime

class MathSection:
    """Represents a single category of math problems."""
    def __init__(self, label, digit_type, count=2, num_questions=5):
        self.label = label
        self.digit_type = digit_type
        self.count = count
        self.num_questions = num_questions

    def generate_question(self):
        """Logic for generating numbers based on the digit_type."""
        if self.digit_type == "3+2":
            numbers = [random.randint(100, 999), random.randint(10, 99)]
        elif self.digit_type == "3+4":
            numbers = [random.randint(100, 999), random.randint(1000, 9999)]
        else:
            # Standard digit logic
            start = 10**(self.digit_type - 1) if self.digit_type > 1 else 1
            end = (10**self.digit_type) - 1
            numbers = [random.randint(start, end) for _ in range(self.count)]

        random.shuffle(numbers)
        return numbers, sum(numbers)

class QuizGenerator:
    """Manages the assembly and rendering of the full HTML quiz."""
    def __init__(self, categories):
        self.categories = categories
        self.timestamp = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        self.total_possible = sum(c.num_questions for c in categories)

    def generate_quiz_html(self):
        quiz_html = ""
        for idx, cat in enumerate(self.categories):
            quiz_html += f"""
            <div class="section" id="section-{idx}">
                <div class="section-header">
                    <h3>{cat.label}</h3>
                    <div class="section-stats">
                        Score: <span id="score-{idx}">0</span>/{cat.num_questions} | 
                        Time: <span id="time-{idx}">0s</span>
                    </div>
                </div>
                <ol>"""
            
            for q_idx in range(cat.num_questions):
                nums, answer = cat.generate_question()
                question_text = " + ".join(map(str, nums))
                
                quiz_html += f"""
                <li>
                    {question_text} = 
                    <input type="number" class="user-input" 
                           data-section="{idx}" data-qidx="{q_idx}" data-total="{cat.num_questions}"
                           onfocus="startSectionTimer({idx})" onchange="checkAnswer(this, {answer})" placeholder="?">
                    <span class="actual-answer" style="display:none; color: #d32f2f; margin-left:10px;">({answer})</span>
                    <button class="reveal-btn" onclick="revealSingle(this)">Ans</button>
                </li>"""
            quiz_html += "</ol></div>"
        return quiz_html

    def save(self, filename="index.html"):
        body_content = self.generate_quiz_html()
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Daily Math Challenge</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background-color: #f0f2f5; }}
                .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                h1 {{ border-bottom: 3px solid #4CAF50; color: #2E7D32; margin-bottom: 5px; }}
                .section {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 25px; padding: 15px; }}
                .section-header {{ display: flex; justify-content: space-between; align-items: center; background: #e8f5e9; padding: 5px 15px; border-radius: 6px; margin-bottom: 10px; }}
                .section-stats {{ font-weight: bold; color: #2E7D32; font-size: 0.9em; }}
                .section.complete {{ border: 2px solid #4CAF50; background-color: #fafffa; }}
                .stats-bar {{ background: #333; color: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; display: flex; justify-content: space-between; }}
                .user-input {{ width: 110px; padding: 5px; border: 2px solid #ccc; border-radius: 4px; font-size: 1.1em; text-align: center; }}
                .correct {{ border-color: #4CAF50 !important; background-color: #e8f5e9; }}
                .incorrect {{ border-color: #f44336 !important; background-color: #ffebee; }}
                .main-btn {{ padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; color: white; background: #4CAF50; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧮 Daily Math Practice</h1>
                <p><strong>Generated:</strong> {self.timestamp}</p>
                <div class="stats-bar">
                    <span>Total Score: <span id="total-score">0</span> / {self.total_possible}</span>
                    <span>Section-based timing enabled</span>
                </div>
                <div style="margin-bottom:20px;">
                    <button class="main-btn" onclick="location.reload()">Reset All</button>
                </div>
                {body_content}
            </div>
            <script>
                let sectionTimers = {{}}; 
                let sectionIntervals = {{}};

                function startSectionTimer(sId) {{
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
                    const qIdx = parseInt(input.getAttribute('data-qidx'));
                    const totalInSec = parseInt(input.getAttribute('data-total'));

                    if (input.value == "") {{
                        input.classList.remove('correct', 'incorrect');
                    }} else if (parseInt(input.value) === correct) {{
                        input.classList.add('correct');
                        input.classList.remove('incorrect');
                    }} else {{
                        input.classList.add('incorrect');
                        input.classList.remove('correct');
                    }}

                    document.getElementById('score-' + sId).innerText = document.querySelectorAll('#section-' + sId + ' .user-input.correct').length;
                    document.getElementById('total-score').innerText = document.querySelectorAll('.user-input.correct').length;

                    if (qIdx === totalInSec - 1 && input.value !== "") {{
                        clearInterval(sectionIntervals[sId]);
                        sectionIntervals[sId] = "FINISHED";
                        document.getElementById('section-' + sId).classList.add('complete');
                        return;
                    }}

                    const allInputs = Array.from(document.querySelectorAll('.user-input'));
                    const currentIndex = allInputs.indexOf(input);
                    if (currentIndex < allInputs.length - 1) allInputs[currentIndex + 1].focus();
                }}

                function revealSingle(btn) {{
                    btn.previousElementSibling.style.display = "inline";
                    btn.style.display = "none";
                }}
            </script>
        </body>
        </html>
        """
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_template)
        print(f"✅ Generated {filename}")

# --- CONFIGURATION (Modular Section List) ---
if __name__ == "__main__":
    # Restored all previous categories and added the new ones
    categories = [
        MathSection("1) Single digit number addition", 1, 2, 5),
        MathSection("2) Single digit addition of 5", 1, 5, 5),
        MathSection("3) Double digit addition", 2, 2, 5),
        MathSection("4) Double digit addition of 5", 2, 5, 5),
        MathSection("5) 3-digit + 2-digit addition", "3+2", 2, 5),
        MathSection("6) 3-digit addition", 3, 2, 5),
        MathSection("7) 3-digit + 4-digit addition", "3+4", 2, 5),
        MathSection("8) 4-digit addition", 4, 2, 5)
    ]

    quiz = QuizGenerator(categories)
    quiz.save()
