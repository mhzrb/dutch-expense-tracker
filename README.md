# 💶 Dutch Expense Tracker

A Django expense tracker built for keeping monthly spending under control —
categories tailored for life in the Netherlands (rent, grocery, transport,
insurance), monthly charts, and budget alerts.

100% free to run — SQLite by default, no paid API required.

## Why I built this

I'm currently applying to companies here in the Netherlands and settling
into a new budget rhythm — rent, groceries, insurance, transport all add up
differently than what I was used to. I wanted a simple, focused tool built
specifically around Dutch expense categories instead of a generic finance
app, and building it myself meant I could shape it exactly around how I
actually track spending.

## Screenshots

<!-- Add your own screenshots here — see "Adding screenshots" below -->
![Dashboard](screenshots/dashboard.jpg)
![Expense list](screenshots/expense-list.jpg)

## Features

- User accounts (sign up / log in) — each user only sees their own data
- Add / edit / delete expenses with category, amount, date, note
- Categories: Rent, Grocery, Transport, Insurance, Utilities, Healthcare, Entertainment, Other
- Dashboard with:
  - This month's total spend
  - Spending-by-category doughnut chart
  - Last 6 months trend line chart
  - Monthly budget vs. remaining balance
- Filter expense list by category
- Django admin panel included for quick data management

## Tech Stack

- Django 5
- SQLite (default, zero config) — swappable to PostgreSQL
- Bootstrap 5 + Chart.js (via CDN, no build step)

## Installation

### Prerequisites
- Python 3.10+

### Setup

```bash
git clone https://github.com/<your-username>/dutch-expense-tracker.git
cd dutch-expense-tracker

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# open .env and set SECRET_KEY (see comment in the file for how to generate one)

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/ access
python manage.py runserver
```

Open [http://localhost:8000](http://localhost:8000), sign up, and start logging expenses.

## Switching to PostgreSQL (optional, still free)

1. Install Postgres locally, or use a free-tier host like [Neon](https://neon.tech) or [Supabase](https://supabase.com).
2. Uncomment `psycopg2-binary` in `requirements.txt` and `pip install -r requirements.txt` again.
3. Set `DATABASE_URL=postgres://user:password@host:5432/dbname` in `.env`.
4. Run `python manage.py migrate`.

## Project Structure

```
expensetracker/       # Django project settings, root urls
expenses/
  models.py            # Expense, MonthlyBudget
  views.py              # dashboard, CRUD views, budget view
  forms.py              # ModelForms + signup form
  urls.py               # app routes
  templates/expenses/   # Bootstrap templates
```

## Deploying

Free options: [Railway](https://railway.app), [Render](https://render.com), or
[Fly.io](https://fly.io) all have free tiers that work well with Django +
SQLite/Postgres + `gunicorn` (already in requirements.txt).

## What I learned building this

- Structuring a Django project around multiple models with a real
  relationship (`Expense` and `MonthlyBudget` both tied to `User`) and
  keeping queries scoped per-user
- Aggregating data with Django's ORM (`Sum`, `values().annotate()`) to
  power the dashboard instead of pulling everything into Python
- Wiring up Chart.js against server-rendered data (passing querysets into
  templates as JSON) without a separate frontend framework
- Handling environment-based configuration (`.env`, `DATABASE_URL`
  switching between SQLite and Postgres) the way a real deployed app would

## Adding screenshots

1. Run the app locally and get it into a good state (a few sample expenses, budget set).
2. Take screenshots of the dashboard and expense list (in Ubuntu: `Shift+PrtScn` to select an area, or the Screenshot app from the Activities menu).
3. Inside the project folder, create a folder for them:
   ```bash
   mkdir screenshots
   ```
4. Save your screenshots there as `dashboard.png` and `expense-list.png` (or update the filenames in this README to match whatever you name them).
5. Commit and push as usual:
   ```bash
   git add screenshots/
   git commit -m "Add screenshots"
   git push
   ```
   GitHub will automatically render them in this README since the paths above already point to `screenshots/`.

## License

MIT
