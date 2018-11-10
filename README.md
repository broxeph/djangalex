# Huh?
If you're reading this, you're reading the README.

# To do

- Base
    - Specify role with `DJANGO_SETTINGS_MODULE`, e.g. `dev.py`
    - Move manual setup to Python script (or better, to Docker!)
    - Move app templates to base templates directory
- Home
    - Add dynamic subtitles
        - Founding member, Interesting Times Gang, etc.
- WineApp
    - Add tests for logged-in user wine recommendations
    - Add more wines, populate metadata with the usual junk
    - Serve uploaded wine images with S3
    - Add 'blog archive' thing for older Shouts & Murmurs posts
    - Shrink larger images, use one-column layout for xs viewports

# Local setup

1. Initialize virtualenv    
    - `python3 -m virtualenv .venv`
2. Activate venv
    - `. .venv/bin/activate`
3. Install Python requirements
    - `pip3 install -r requirements.txt`
4. Install apt requirements
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

1. Install Heroku CLI
    - `sudo snap install --classic heroku`
2. Set Heroku env vars, if necessary
    - Can be done from Heroku GUI or `heroku config:set FOO=bar`
3. Do the jawn!
    - `git push heroku master`
