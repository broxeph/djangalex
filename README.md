# Huh?
If you're reading this, you're reading the README.

# To do

- Base
    - Add error tracking (Sentry) so broken pages get noticed instead of discovered
- WineApp
    - Add more wines, populate metadata with the usual junk
    - Add 'blog archive' thing for older Shouts & Murmurs posts

# Local setup

1. Initialize virtualenv (Python 3.14, matching `.python-version`)
    - `python3.14 -m venv .venv`
2. Activate venv
    - `. .venv/bin/activate`
3. Install Python requirements
    - `pip3 install -r requirements.txt`
4. Install apt requirements (a local Postgres server; psycopg2-binary needs no build deps)
    - `xargs -a apt-requirements.txt sudo apt-get install`
5. Create Postgres user and database
    1. `sudo -u postgres psql`
    2. `CREATE USER djangalex WITH PASSWORD 'hunter2';` (replace `hunter2` if you dare)
    3. `CREATE DATABASE djangalex OWNER djangalex;`
    4. `\q`
8. Add secrets to env vars
    - (this is another good candidate for moving to Docker, or at least `.bashrc`)
    - `export DATABASE_URL=postgres://djangalex:hunter2@localhost:5432/djangalex`
    - `export SECRET_KEY=hunter2` (or a somewhat more secure password, for you Krebs readers out there)
    - `export DEBUG=True`
    - `export AWS_STORAGE_BUCKET_NAME=foo`
    - `export AWS_ACCESS_KEY_ID=bar`
    - `export AWS_SECRET_ACCESS_KEY=baz`
    - `export DJANGO_SECRET_KEY=baz`
10. Run initial database migration
    - `./manage.py migrate`
11. Create superuser
    - `./manage.py createsuperuser`
12. Run server!
    - `./manage.py runserver`
    - Site should be accessible at `localhost:8000/`

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
