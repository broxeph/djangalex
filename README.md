# Huh?
If you're reading this, you're reading the README.

# To do

- Base
    - Add error tracking (Sentry) so broken pages get noticed instead of discovered
- WineApp
    - Add more wines, populate metadata with the usual junk
    - Add 'blog archive' thing for older Shouts & Murmurs posts

# Local setup

1. Create and activate a virtualenv (Python 3.14, matching `.python-version`)
    - `python3.14 -m venv .venv`
    - `. .venv/bin/activate`
2. Install Python requirements
    - `pip install -r requirements.txt`
3. Set env vars (a good candidate for `.bashrc` or a `.env` loader)
    - `export DEBUG=True`
    - `export DJANGO_SECRET_KEY=hunter2` (anything; it only matters in production)
    - `export DATABASE_URL=sqlite:///db.sqlite3`
    - With `DEBUG=True`, uploads go to a local `media/` directory and analytics are off, so no AWS or
      Google keys are needed. Production reads `AWS_*` and `GA_MEASUREMENT_ID` from Heroku config vars.
4. Migrate, create an admin user, run the tests
    - `./manage.py migrate`
    - `./manage.py createsuperuser`
    - `./manage.py test`
5. Run the server
    - `./manage.py runserver`
    - Site is at `localhost:8000/`; WineApp at `localhost:8000/wineapp/`

Production runs Postgres, so if you'd rather match it locally:

1. Install it: `xargs -a apt-requirements.txt sudo apt-get install`
2. Create a user and database in `sudo -u postgres psql`:
    - `CREATE USER djangalex WITH PASSWORD 'hunter2';`
    - `CREATE DATABASE djangalex OWNER djangalex;`
3. `export DATABASE_URL=postgres://djangalex:hunter2@localhost:5432/djangalex`

# Deployment

1. Install Heroku CLI (snap is no longer supported)
    - `curl https://cli-assets.heroku.com/install.sh | sh`
2. Set Heroku env vars, if necessary
    - Can be done from Heroku GUI or `heroku config:set FOO=bar`
3. Do the jawn!
    - `git push origin master`
    - The Heroku app auto-deploys from GitHub `master`, so every push to it is a production deploy
    - Runs `python manage.py migrate` as the release step (see `Procfile`)
4. Dependabot opens one grouped PR a month for Python package updates (see `.github/dependabot.yml`)
    - Merging it deploys, so run `./manage.py test` on the branch first
