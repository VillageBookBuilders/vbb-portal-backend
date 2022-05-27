# vbb

VBB Booking Portal Backend

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=b4a8e079838e&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create an **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy vbb

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd vbb
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Local Setup

Add `export DJANGO_READ_DOT_ENV_FILE=True` to your `.bashrc` or `.zshrc` file

create a `.env` file based on `.env_example` (run `cp .env_example .env`)

#### Setup DB

- create database: `createdb vbb`
- run migrations: `python manage.py migrate`

##### Seeding

run `python manage.py seed` to add seeds

- Seed Users:
  ** NOTE ABOUT USERS: ** `User === Human`. Each User then has one or many profiles: `user.mentor_profile`, `user.student_profile`
  The users below only have a profile under their given user. All mentors also belong to an `Organization`

  - All Passwords: `123`
  - Students
    ```
    "username": "test_student1",
    "username": "test_student2",
    "username": "test_student3",
    "username": "test_student4",
    "username": "test_student5",
    "username": "test_student6",
    ```
  - Mentors
    ```
    "email": "test_mentor1@test.com",
    "email": "test_mentor2@test.com",
    "email": "test_mentor3@test.com",
    "email": "test_mentor4@test.com",
    "email": "test_mentor5@test.com",
    "email": "test_mentor6@test.com",
    ```

  languages from [Annexare/Countries repo](from: https://github.com/annexare/Countries)

#### Setup Caddy

[Caddy](https://caddyserver.com/docs/getting-started) is the proxy service we use to connect the backend app and the frontend app and allows us to serve the same service as a single domain rather than sub domains

- install with `brew install caddy`
- start with either:
  `caddy run --config /full/path/to/vbb/repository/Caddyfile` ( this will start the service and end when the terminal is closed )
  or
  `caddy start --config /full/path/to/vbb/repository/Caddyfile` ( this will start the service and end only when you run `caddy stop`)

#### Cert file if needed ( this is only needed if you don't use the default `https://vbb.local`)

[Following this Medium article](https://medium.com/@devahmedshendy/traditional-setup-run-local-development-over-https-using-caddy-964884e75232)

- install mkcert `brew install mkcert` and after `mkcert -install`
- Make a directory to store our certificates, I used `~/.config/local-certs/`
- run `mkcert "localhost.vbb.org"` or what ever host you'd prefer
- Cert locations will then be `~/.config/local-certs/localhost.vbb.org.pem` and `~/.config/local-certs/localhost.vbb.org-key.pem`

Caddy Setup Continued

- run `caddy trust`

MacOS instructions:

- Add `vbb.local` or `localhost.vbb.org` to your `/private/etc/hosts` file.
  Your `hosts` file should look something like:

  ```bash
  127.0.0.1	localhost localhost.vbb.org vbb.local
  ```

**NOTES**

- If you're using Insomnia you'll need to disable checking for SSL certificates
- If you're using Firefox you will need to restart Firefox to allow local ssl certificates to reload

- Start both the backend under it's directory ( `python manage.py runserver`) and the frontend under it's ( `yarn start`)

- You will want to close the browser window the frontend automatically opens
- Navigate to: `https://.vbb.local/`
- You should see the landing page
