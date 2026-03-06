import random
from datetime import datetime

class MathSection:
    def __init__(self, title, digit_type, numbers_per_q=2, num_questions=5):
        self.title = title
        self.digit_type = digit_type
        self.numbers_per_q = numbers_per_q
        self.num_questions = num_questions

    def _generate_numbers(self):
        """Generates numbers based on the digit_type string or integer."""
        if self.digit_type == "3+2":
            nums = [random.randint(100, 999), random.randint(10, 99)]
        elif self.digit_type == "3+4":
            nums = [random.randint(100, 999), random.randint(1000, 9999)]
        else:
            # Standard logic for uniform digit counts
            d = int(self.digit_type)
            start = 10**(d - 1) if d > 1 else 1
            end = (10**d) - 1
            nums = [random.randint(start, end) for _ in range(self.numbers_per_q)]
        
        random.shuffle(nums)
        return nums

    def render_html(self, section_id):
        """Generates the HTML string for this specific section."""
        html = f"""
        <div class="section" id="section-{section_id}">
            <div class="section-header">
                <h3>{self.title}</h3>
                <div class="section-stats">
                    Score: <span id="score-{section_id}">0</span>/{self.num_questions} | 
                    Time: <span id="time-{section_id}">0s</span>
                </div>
            </div>
            <ol>"""
        
        for q_idx in range(self.num_questions):
            nums = self._generate_numbers()
            question_text = " + ".join(map(str, nums))
            answer = sum(nums)
            
            html += f"""
            <li>
                {question_text} = 
                <input type="number" class="user-input" 
                       data-section="{section_id}" data-qidx="{q_idx}" data-total="{self.num_questions}"
                       onfocus="startSectionTimer({section_id})" onchange="checkAnswer(this, {answer})" placeholder="?">
                <span class="actual-answer" style="display:none; color: #d32f2f; margin-left:10px;">({answer})</span>
                <button class="reveal-btn" onclick="revealSingle(this)">Ans</button>
            </li>"""
        
        html += "</ol></div>"
        return html

class QuizGenerator:
    def __init__(self, sections):
        self.sections = sections
        self.timestamp = datetime.now().strftime("%B %d, %Y - %H:%M:%S")
        self.total_possible = sum(s.num_questions for s in sections)

    def build_page(self, filename="index.html"):
        quiz_body = "".join([s.render_html(i) for i, s in enumerate(self.sections)])
        
        # Using double {{ }} for CSS/JS to escape Python's f-string formatting
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OOP Math Quiz</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 20px; color: #333; background-color: #f0f2f5; }}
                .container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                h1 {{ border-bottom: 3px solid #4CAF50; color: #2E7D32; margin-bottom: 5px; }}
                .section {{ background: #fff; border: 1px solid #ddd; border-radius: 8px; margin-bottom: 25px; padding: 15px; }}
                .section-header {{ display: flex; justify-content: space-between; align-items: center; background: #e8f5e9; padding: 5px 15px; border-radius: 6px; margin-bottom: 10px; }}
                .section-stats {{ font-weight: bold; color: #2E7D32; font-size: 0.9em; }}
                .section.complete {{ border: 2px solid #4CAF50; background-color: #fafffa; }}
                .stats-bar {{ background: #333; color: #fff; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; display: flex; justify-content: space-between; }}
                .user-input {{ width: 100px; padding: 5px; border: 2px solid #ccc; border-radius: 4px; font-size: 1.1em; text-align: center; }}
                .correct {{ border-color: #4CAF50 !important; background-color: #e8f5e9; }}
                .incorrect {{ border-color: #f44336 !important; background-color: #ffebee; }}
                .main-btn {{ padding: 10px 15px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; color: white; background: #4CAF50; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🧮 Daily OOP Math</h1>
                <p><strong>Generated:</strong> {self.timestamp}</p>
                <div class="stats-bar">
                    <span>Total Score: <span id="total-score">0</span> / {self.total_possible}</span>
                    <span>OOP Architecture Ready</span>
                </div>
                <div style="margin-bottom:20px;">
                    <button class="main-btn" onclick="location.reload()">Reset All</button>
                </div>
                {quiz_body}
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

                    const sectionCorrect = document.querySelectorAll('#section-' + sId + ' .user-input.correct').length;
                    document.getElementById('score-' + sId).innerText = sectionCorrect;
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
            f.write(full_html)
        print(f"✅ Created {filename} with OOP!")

# --- CONFIGURATION ---
if __name__ == "__main__":
    # You can now easily add or remove sections by just adding a MathSection object
    my_sections = [
        MathSection("1) Single Digit Addition", 1, 2, 5),
        MathSection("2) Single Digit (5 numbers)", 1, 5, 5),
        MathSection("3) Double Digit Addition", 2, 2, 5),
        MathSection("4) 3-Digit + 2-Digit", "3+2", 2, 5),
        MathSection("5) 3-Digit + 4-Digit", "3+4", 2, 5),
        MathSection("6) 4-Digit Marathon", 4, 2, 5) 
    ]

    quiz = QuizGenerator(my_sections)
    quiz.build_page()
