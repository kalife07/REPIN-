# REPIN'

**A personalized fitness coaching web app.** Answer a few questions about your body, your training habits and your goal, and REPIN' builds you a complete plan: a daily calorie and macro target, two weekly workout split options with exercises, sets, reps and starting weights, the date you can expect to reach your goal weight, and an optimal wake-up time.

---

## Table of contents

- [Features](#features)
- [How it works](#how-it-works)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the app](#running-the-app)
- [API reference](#api-reference)
- [Troubleshooting](#troubleshooting)

---

## Features

### 🍽️ Nutrition plan
- **Daily calorie target**: your maintenance calories (BMR from the Mifflin-St Jeor equation × an activity multiplier), adjusted up or down for your goal.
- **Macronutrients**: protein, fat and carbohydrates in grams.
- **Other daily targets**: fiber, sugar limit, sodium limit and water intake.

### 🏋️ Workout plan
- **Two split options** matched to how often you train (Full-Body, Upper-Lower, Push-Pull-Legs, Arnold Split, plus cardio for twice-a-day training).
- **Exercises for every day** with sets, reps and rest time based on your training focus:

  | Focus    | Reps  | Sets | Rest   |
  |----------|-------|------|--------|
  | Strength | 6-8   | 2-3  | 3m     |
  | Muscle   | 12-15 | 3    | 1m     |
  | Both     | 8-12  | 2-3  | 1m 30s |

- **Suggested starting weights** for each exercise, scaled to your body weight.

### 🎯 Goal tracking
- **Target date** for reaching your goal weight, based on the pace you choose:

  | Pace   | Change per week |
  |--------|-----------------|
  | Slow   | 0.25 kg         |
  | Medium | 0.5 kg          |
  | Fast   | 1 kg            |

### 😴 Sleep
- **Optimal wake-up time**, calculated from your bedtime for 8.5 hours of sleep.

---

## How it works

REPIN' has two parts that run side by side:

| Part         | Technology              | Runs on                 | Role |
|--------------|-------------------------|-------------------------|------|
| **Frontend** | HTML, CSS, JavaScript   | `http://localhost:8000` | Collects your answers and displays your plan on a dashboard |
| **Backend**  | Python, Flask           | `http://127.0.0.1:5000` | Does all the calculations and returns them as JSON |

You fill in a short 3-step form (personal info → training & goals → sleep), and the frontend sends your answers to the backend API. The results are shown on a dashboard, and you can start over at any time with **Recalculate**.

---

## Project structure

```
REPIN-/
├── app/                    # Backend (Flask API)
│   ├── app.py              # Entry point: creates the Flask app and starts the server
│   ├── routes.py           # API endpoints
│   ├── nutrition.py        # Calorie and macronutrient calculations
│   ├── workout.py          # Split selection, exercises and starting weights
│   ├── goals.py            # Time and date to reach the goal weight
│   ├── sleep.py            # Wake-up time calculator
│   ├── models.py           # Exercice class
│   └── config.py           # Shared constants
├── frontend/               # Frontend (static website)
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── assets/             # Logo and loading animation
├── requirements.txt        # Python packages needed by the backend
└── README.md
```

---

## Requirements

- **Python 3.10 or newer** ([download](https://www.python.org/downloads/))
- **pip**, Python's package installer (included with Python)
- A modern web browser (Chrome, Firefox, Safari, Edge)

Python packages used by the backend (listed in [`requirements.txt`](requirements.txt)):

| Package           | Purpose |
|-------------------|---------|
| `flask`           | Web server and API |
| `flask-cors`      | Lets the frontend (port 8000) call the backend (port 5000) |
| `python-dateutil` | Date calculations for the goal date |

---

## Installation

1. **Get the code**

   ```bash
   git clone <repository-url>
   cd REPIN-
   ```

   Or download the ZIP from GitHub and unzip it.

2. **(Optional) Create a virtual environment** to keep the packages isolated from the rest of your system

   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS / Linux
   venv\Scripts\activate         # Windows
   ```

3. **Install the Python packages**

   ```bash
   pip install -r requirements.txt
   ```

> On some systems the commands are `python3` and `pip3` instead of `python` and `pip`.

---

## Running the app

You need **two terminals**, both opened in the project's root folder (`REPIN-`).

**Terminal 1: start the backend**

```bash
python -m app.app
```

You should see `Running on http://127.0.0.1:5000`. Keep this terminal open.

**Terminal 2: start the frontend**

```bash
python -m http.server 8000 --directory frontend
```

**Open the app** by going to [http://localhost:8000](http://localhost:8000) in your browser, then click **CREATE YOUR PLAN**. 💪

To stop either server, press `Ctrl + C` in its terminal.

> ⚠️ Run the backend with `python -m app.app` from the project root. Running `python app/app.py` or running it from inside the `app/` folder will not work.

---

## API reference

All endpoints accept a JSON body via `POST` and return JSON. Base URL: `http://127.0.0.1:5000`.

Accepted values:
- `gender`: `male`, `female`
- `activity`: `sedentary`, `lightly active`, `active`, `very active`, `extra active`
- `goal`: `cut`, `bulk`, `maintain`
- `loss_speed`: `slow`, `medium`, `fast`
- `plan`: `strength`, `muscle`, `both`
- `bed_time`: an hour followed by `am` or `pm`, e.g. `"10 pm"`

| Endpoint                 | Body | Returns |
|--------------------------|------|---------|
| `/api/nutrition-plan`    | `age`, `gender`, `weight` (kg), `height` (cm), `activity`, `goal`, `loss_speed` | `goal_calories`, `macronutrients` (protein, fat, carbs in g), `other_info` (fiber, sugar, sodium, water) |
| `/api/workout-plan`      | `weight` (kg), `plan`, `activity` | `option_1` and `option_2`, each with a split `name` and a `schedule` (a list of days, each a list of exercises) |
| `/api/time-to-goal`      | `current_weight`, `final_weight` (kg), `loss_speed` | `weeks_to_goal` |
| `/api/date-to-goal`      | `current_weight`, `final_weight` (kg), `loss_speed` | `target_date`, e.g. `"12 MAR 2027"` |
| `/api/sleep-calculator`  | `bed_time` | `wake_up_time`, e.g. `"6:30 am"` |

**Example**

```bash
curl -X POST http://127.0.0.1:5000/api/sleep-calculator \
     -H "Content-Type: application/json" \
     -d '{"bed_time": "10 pm"}'
```

```json
{ "wake_up_time": "6:30 am" }
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Install the packages (see [Installation](#installation)). If you use a virtual environment, make sure it is activated. |
| `Port 5000 is in use by another program` (macOS) | AirPlay Receiver uses port 5000. Turn it off in **System Settings → General → AirDrop & Handoff → AirPlay Receiver**. |
| The plan never loads after clicking **Generate Plan** | Make sure the backend is running in Terminal 1, then check it for error messages. |
| `localhost:8000` shows a list of files instead of the app | Start the frontend with `--directory frontend`, as shown above. |
| Images are missing | Make sure the `assets/` folder is inside `frontend/`. |

---

⚠️ **Disclaimer:** REPIN' gives general fitness and nutrition estimates. It is not medical advice. Consult a healthcare professional before starting a new diet or training program.
