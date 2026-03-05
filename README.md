# 🧮 Daily Math Quiz Generator

![Daily Update](https://img.shields.io/badge/Status-Auto--Updating-green)
[![Run Daily Script](https://github.com/bhanuprakash012/Daily_math/actions/workflows/daily_update.yml/badge.svg)](https://github.com/bhanuprakash012/Daily_math/actions/workflows/daily_update.yml)

A randomized Python script designed to generate math addition worksheets. This repository is automated to update itself once a day using GitHub Actions.

**🔗 [Click here to see today's Quiz!](https://bhanuprakash012.github.io/Daily_math/)**

---

## 🤖 How the Automation Works

This project is more than just a script; it's a self-hosting web app:
* **GitHub Actions:** A workflow wakes up every day at 00:00 UTC.
* **Python Engine:** The `test.py` script runs, generates new numbers, and writes them into `index.html`.
* **GitHub Pages:** The updated HTML is instantly hosted as a live website.

---

## ✨ Quiz Features

The generator creates **5 questions per category** for the following types:

1.  **Single Digit:** Standard $x + y$ format.
2.  **Single Digit (Series of 5):** Adding five single-digit numbers together.
3.  **Double Digit:** Standard $xx + yy$ format.
4.  **Double Digit (Series of 5):** Adding five double-digit numbers together.
5.  **Mixed Digits:** 3-digit number + 2-digit number ($xxx + yy$).
6.  **Triple Digit:** Standard $xxx + yyy$ addition.

---

## 🚀 Local Development

### 1. Prerequisites
Ensure you have **Python 3.x** installed on your machine.

### 2. Run the Script
Clone the repository and run the script using your terminal:
```bash
python test.py
