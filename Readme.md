# GIT-O-MATIC-9K

Vroom Vroom. Git-o-matic 9k is a fully automated github user and repository
discovery system. Once the system is seeded with at least one user, an
automated scraper grows the database by following network connections
(followers and following).

This project is powered by `django`, `djangorestframework` and `celery`.

On only and fully functional version is available on
heroku [here](https://secret-gorge-30655.herokuapp.com/github/).
The login and password are `test_user` and `b@t09pp#m`. Please not that the
app is running on a free set of dynos and addons, and as such the performance
may be low. Nevertheless, it is fully working.

The github repository for this project includes a fully functional CI, setup
using github actions. It tests the codebase with `pylint` and runs automated
unit tests. An action automatically prepares a deploy pr if there is new code
on master. Finally, if a merge into the `production` branch happens, it gets
deployed automatically to heroku.

## Periodic tasks

Two periodic tasks are scheduled:

1) The `discovery_scraper`. This runs every hour and fetches new users that are
following or being followed by some user already in the database. If the
database is empty then nothing happens.

2) The `heart_beat_task`. It runs every minute and logs a `"ping"` string. This
can be used to detect that celery and the celery scheduler are running.

This can be changed or new tasks can be added by editing `CELERY_BEAT_SCHEDULE`
on `settings.py`. See
https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html for more
information.

Another way to schedule tasks is to make a `POST` request to `/github/tasks/`
with the paramenter `name` set to the task name. So far only the
`discovery_scraper` task is supported.

## Auto throttle

Git-o-matic-9k contains a throttle system, which uses the rate limit data from
github to prevent running services that will surelly fail. These tasks, instead
of failing, are automatically rescheduled to when then reset quota is reset.
Another useful feature is limiting how much of the quota can be used by the
service, which allows more than one resource intensive application to work on
the same account without starving critical systems of requests.

The system also supports working unauthenticated on the API. Which grately
reduces the system throuput, but allows for a quicker setup and testing.

Tasks are started if there are at least one remaining request in the quota.
However, many tasks require several requests to work. If the request quota is
exausted during a rask, then `HttpErrorExeption` will be raised with an `API
rate limit exceeded` message. The rationale is that it is ok to postpone a
task, but running a task half way through is not. As such, if a task runs out
of request quota during its execution it is properly signicaled as an error.

## Local setup

1) Set up [`pyenv`](https://github.com/pyenv/pyenv) and
  [`pipenv`](https://github.com/pypa/pipenv)
2) Run `pyenv install $(cat .python-version)`
3) Run `pipenv install --dev`
  - If running `pipenv install` fails with an error related to `psycopg2`, then
  running the following before running `pipenv install` again might solve the
  issue, assuming you are on macos and installed openssl with homebrew:
  `LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pipenv install --dev`
4) Ensure that [`rabbitmq`](https://www.rabbitmq.com/) and
  [`postgresql`](https://www.postgresql.org/) are installed. Optionally install
  either [`goreman`](https://github.com/mattn/goreman),
  [`foreman`](https://github.com/theforeman/foreman), or an equivalent.
5) Create a database for the project with `createdb git_o_matic_9k`
6) Create an admin user with: `pipenv run python manage.py createsuperuser
  --email some@mail.com --username admin` and set a password
7) Set up github api key and username with
  `export GITHUB_API_KEY='ultra_secret_key'` and
  `export GITHUB_API_USER='awesome_user'`. Alternativelly, it is possible to
  run the application without setting it, but be aware that the rate limit will
  be reached very quickly
8) Run `goreman -f Procfile.dev`, or equivalent. Alternativelly it the
  following can be used: `pipenv run python manage.py runserver` and `pipenv run
  celery -A git_o_matic_9k  worker --beat --loglevel INFO`

### Testing

Assuming that at least the first 5 steps were followed, the test suite can be
ran with: `pipenv run python manage.py test`

## LICENSE

See [LICENSE](LICENSE)
