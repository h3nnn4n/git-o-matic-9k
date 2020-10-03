# GIT-O-MATIC-9K

Vroom Vroom. Git-o-matic 9k is a fully automated github user and repository
discovery system. It can act as a data mirror, with some extra features on top,
such as fulltext search.

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
