# 🧠 MEDNEXAI TrackHub

> **The story:** Our mentor used to ask us to post daily progress reports in a WhatsApp group. It was chaotic — messages got buried, nobody could track progress, and there was no accountability. This app fixes that.

**TrackHub** is a structured daily report submission platform built for learning communities. Students submit reports, peers see each other's progress, and mentors get a clean analytics dashboard — no more WhatsApp chaos.

---

## 🌍 Live Demo
👉 [mednexai-trackhub.com](https://mednexai-trackhub.onrender.com/)

---

## ✨ Features

- 🔐 **Invite-only registration** — mentor controls who joins
- 📝 **Daily report submission** — structured form (hours, tasks, discipline score)
- 🌍 **Peer feed** — see what your community is building every day
- 🔥 **Streak tracking** — how many days in a row you've submitted
- 📊 **Mentor dashboard** — charts, consistency stats, team overview
- 👨‍💼 **Admin panel** — generate invite codes, manage users

---

## 🗂️ Project Structure (explained simply)

Think of the project like a house. Each folder is a room with a specific job.

```
mednexai_trackhub/
│
├── config/                  ← The BRAIN of the project
│   ├── settings/
│   │   ├── base.py          ← Settings that apply everywhere
│   │   ├── dev.py           ← Extra settings for your laptop (development)
│   │   └── prod.py          ← Settings for the live server (production)
│   ├── urls.py              ← The RECEPTIONIST — decides which page to show
│   └── wsgi.py              ← The DOOR — how the server connects to Django
│
├── accounts/                ← Everything about USERS
│   ├── models.py            ← What a user looks like (username, role, etc.)
│   ├── forms.py             ← The registration form + invite code check
│   ├── views.py             ← What happens when you visit login/register page
│   ├── urls.py              ← Links for /login, /logout, /register
│   └── admin.py             ← How users appear in the admin panel
│
├── reports/                 ← Everything about REPORTS
│   ├── models.py            ← What a report looks like (day, hours, tasks...)
│   ├── forms.py             ← The report submission form + validation
│   ├── views.py             ← What happens when you submit/view reports
│   ├── urls.py              ← Links for /submit, /feed, /dashboard
│   ├── utils.py             ← Helper functions (streak calc, stats, charts)
│   └── admin.py             ← How reports + invite codes appear in admin
│
├── templates/               ← The FACE of the app (HTML pages)
│   ├── base.html            ← The main layout (navbar, footer) — all pages use this
│   ├── accounts/
│   │   ├── login.html       ← Login page
│   │   └── register.html    ← Registration page
│   └── reports/
│       ├── submit.html      ← Report submission form page
│       ├── feed.html        ← Peer progress feed page
│       └── dashboard.html   ← Mentor analytics dashboard page
│
├── tests/                   ← QUALITY CHECKS (automated tests)
│   ├── conftest.py          ← Test setup (creates dummy users for testing)
│   └── test_main.py         ← 11 tests covering all major features
│
├── requirements/            ← List of packages the project needs
│   ├── base.txt             ← Packages needed everywhere
│   ├── dev.txt              ← Extra packages for development
│   └── prod.txt             ← Extra packages for production
│
├── manage.py                ← Django's command tool (you run this for everything)
├── render.yaml              ← Instructions for deploying to Render.com
├── Procfile                 ← Tells the server how to start the app
└── pytest.ini               ← Configuration for running tests
```

---

## 🧠 How the Code Flows (super simple)

When someone visits a page, this is what happens:

```
Browser request
      ↓
config/urls.py         ← "Which app handles this URL?"
      ↓
reports/urls.py        ← "Which specific view handles it?"
      ↓
reports/views.py       ← "Get the data, process it"
      ↓
reports/models.py      ← "Talk to the database"
      ↓
templates/reports/feed.html   ← "Show it to the user"
      ↓
Browser response
```

---

## 🚀 Run It Locally (on your own laptop)

### Step 1 — Get the code
```bash
git clone https://github.com/celpha2svx/mednexAi_Trackhub.git
cd mednexAi_Trackhub
```

### Step 2 — Create a virtual environment
A virtual environment is like a clean room just for this project's packages.

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You'll know it worked when you see `(venv)` at the start of your terminal line.

### Step 3 — Install packages
```bash
pip install -r requirements/dev.txt
```

### Step 4 — Set up your environment file
```bash
cp .env.example .env
```
Open `.env` and change `SECRET_KEY` to any random string of letters and numbers.

### Step 5 — Set up the database
```bash
python manage.py migrate
```

### Step 6 — Create an admin account
```bash
python manage.py createsuperuser
```
Pick any username and password — this is your mentor account.

### Step 7 — Run the server
```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** in your browser. You're live! 🎉

### Step 8 — Set yourself as mentor + generate invite codes
1. Go to http://127.0.0.1:8000/admin
2. Login with your superuser account
3. Click **Users** → click your username → change Role to `mentor` → Save
4. Click **Invite Codes** → tick any checkbox → Action: "Generate 10 new invite codes" → Go
5. Share codes with your students so they can register

---

## 🧪 Run the Tests
```bash
python -m pytest tests/ -v
```
You should see **11 tests passing**. If any fail, something broke — fix it before pushing.

---

## 🛠️ How to Add a New Feature (step by step)

Let's say you want to add a **"Like" button on reports**. Here's the exact process:

**1. Fork the repo** on GitHub (click Fork button top right)

**2. Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/mednexAi_Trackhub.git
```

**3. Create a new branch** — never work directly on main
```bash
git checkout -b feature/like-button
```

**4. Add your database model** in `reports/models.py`
```python
class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
```

**5. Create and run the migration**
```bash
python manage.py makemigrations
python manage.py migrate
```

**6. Add a view** in `reports/views.py`

**7. Add a URL** in `reports/urls.py`

**8. Update the template** in `templates/reports/feed.html`

**9. Write a test** in `tests/test_main.py`

**10. Push and open a Pull Request**
```bash
git add .
git commit -m "add like button on reports"
git push origin feature/like-button
```
Then go to GitHub and click **"Compare & pull request"**

---

## 💡 Ideas for New Features (good first issues)

These are features the community can build — great for beginners:

| Feature | Difficulty | Where to start |
|---|---|---|
| Comment on a report | ⭐ Beginner | Add `Comment` model in `reports/models.py` |
| Weekly leaderboard | ⭐ Beginner | Add a view in `reports/views.py` |
| Mentor generate codes from dashboard (not admin) | ⭐ Beginner | Add button in `reports/views.py` + `dashboard.html` |
| Email notification when report is submitted | ⭐⭐ Intermediate | Django email + settings |
| WhatsApp notification via Twilio | ⭐⭐ Intermediate | Twilio API in `reports/utils.py` |
| REST API (so mobile app can connect) | ⭐⭐⭐ Advanced | Add Django REST Framework |
| Mobile app (React Native) | ⭐⭐⭐ Advanced | Connects to the API above |

---

## 🤝 Contributing

1. Fork the project
2. Create your branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run the tests (`python -m pytest tests/ -v`) — all must pass
5. Commit (`git commit -m "describe what you did"`)
6. Push (`git push origin feature/your-feature`)
7. Open a Pull Request on GitHub

Please keep code clean and simple. Comment anything that isn't obvious.

---

## 🏗️ Built With

- **Django 5** — Python web framework
- **SQLite** (local) / **PostgreSQL** (production)
- **Tailwind CSS** (via CDN) — styling
- **Chart.js** — mentor dashboard charts
- **WhiteNoise** — serving static files
- **Render.com** — deployment
- **pytest** — automated testing

---

## 👨‍💻 Built By

**Ademuyiwa Afeez** — built this to solve a real problem in the MEDNEXAI learning community.

> *"The best projects come from scratching your own itch."*

---

## 📄 License

MIT License — free to use, modify, and share. Just give credit. 🙏
