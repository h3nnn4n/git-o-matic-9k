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

## Documentation

The API is in fully explorable on a browser by using the `djangorestframework`.
Additionally, a `swagger` and `redoc` documentations are available under
[`/github/swagger`](https://secret-gorge-30655.herokuapp.com/github/swagger/)
and [`/github/redoc/`](https://secret-gorge-30655.herokuapp.com/github/redoc/).

The code is also full documented with doc strings.

## Endpoints

The root endpoint plus four model endpoints make part of the git-o-matic-9k API:

### Root: [`/github/`](https://secret-gorge-30655.herokuapp.com/github/)
The api root. It lists and hyperlinks all other endpoints. For example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/developers/\?page\=42
```

returns

```json
{
    "developers": "https://secret-gorge-30655.herokuapp.com/github/developers/",
    "repositories": "https://secret-gorge-30655.herokuapp.com/github/repositories/",
    "rate_limit": "https://secret-gorge-30655.herokuapp.com/github/rate_limit/",
    "tasks": "https://secret-gorge-30655.herokuapp.com/github/tasks/"
}
```

### Developers: [`/github/developers/`](https://secret-gorge-30655.herokuapp.com/github/developers/)
This endpoint exposes a list of all developers (that were synced). All
relations are hyperlinked. Supports pagination. For example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/developers/\?page\=42
```

returns

```json
{
    "count": 1348,
    "next": "https://secret-gorge-30655.herokuapp.com/github/developers/?page=43",
    "previous": "https://secret-gorge-30655.herokuapp.com/github/developers/?page=41",
    "results": [
        {
            "github_id": "14107257",
            "login": "nordcloud",
            "name": "Nordcloud Engineering",
            "location": "Helsinki, London, Munich, Oslo, Poznań, Stockholm, Malmo, Copenhagen",
            "bio": "Nordcloud Engineering and Open Source. ",
            "company": null,
            "email": "info@nordcloud.com",
            "created_at": "2015-09-03T09:31:50Z",
            "updated_at": "2020-09-01T19:36:57Z",
            "followers_count": 0,
            "following_count": 0,
            "public_gists": 0,
            "public_repos": 44,
            "followers": ["..."],
            "following": ["..."],
            "starred_repositories": ["..."],
            "repositories": [
                "https://secret-gorge-30655.herokuapp.com/github/repositories/6049bd29-5039-421c-8bb8-1464b0c97a06/",
                "..."
            ]
        },
    ]
}
```

Passing an developer/user `uuid` to this endpoint fetches a single user. Example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/developers/4f8e76e8-c068-4f21-a36d-a46c4d221c1d/
```

returns

```json
{
    "github_id": "7543345",
    "login": "h3nnn4n",
    "name": "Renan S Silva",
    "location": "Brazil",
    "bio": "One Renan to code it all. ",
    "company": "JobScore",
    "email": "uber.renan@gmail.com",
    "created_at": "2014-05-10T15:45:24Z",
    "updated_at": "2020-10-02T23:44:43Z",
    "followers_count": 62,
    "following_count": 4,
    "public_gists": 16,
    "public_repos": 164,
    "followers": [
        "https://secret-gorge-30655.herokuapp.com/github/developers/bdea3017-63ce-444c-b758-d3204122f7c5/",
        "...",
    ],
    "following": [
        "https://secret-gorge-30655.herokuapp.com/github/developers/8d909acc-6419-4c69-a24c-69470b28d35f/",
        "...",
    ],
    "starred_repositories": [
        "https://secret-gorge-30655.herokuapp.com/github/repositories/89fdc037-b4f8-47ce-a7fa-2f2dc0713524/",
        "...",
    ],
    "repositories": [
        "https://secret-gorge-30655.herokuapp.com/github/repositories/39f44062-1d70-4d6e-9479-cd2439adf03b/",
        "...",
    ]
}
```

Filters are also supported and fully docummented at the
[`/github/swagger`](https://secret-gorge-30655.herokuapp.com/github/swagger/)
page.

### Repositories: [`/github/repositories/`](https://secret-gorge-30655.herokuapp.com/github/repositories/)
This endpoint exposes a list of all repositories (that were synced). All
relations are hyperlinked. For example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/repositories/
```

returns

```json
{
    "count": 1191,
    "next": "https://secret-gorge-30655.herokuapp.com/github/repositories/?page=2",
    "previous": null,
    "results": [
        {
            "owner": "https://secret-gorge-30655.herokuapp.com/github/developers/153b11f4-d0f8-4f78-a652-e13521d09436/",
            "github_id": "299566089",
            "owner_github_id": "15267120",
            "name": "MazeGenerator",
            "full_name": "89netraM/MazeGenerator",
            "description": "A collection of algorithms for generating mazes",
            "homepage": "",
            "language": "Rust",
            "created_at": "2020-09-29T09:20:44Z",
            "updated_at": "2020-10-04T10:20:43Z",
            "has_downloads": true,
            "has_issues": true,
            "has_pages": false,
            "has_projects": true,
            "has_wiki": true,
            "private": false,
            "archived": false,
            "disabled": false,
            "stargazers": [
                "https://secret-gorge-30655.herokuapp.com/github/developers/87eee21b-09a7-4fac-9c24-79a1bbf22796/",
                "..."
            ],
            "stargazers_count": 52,
            "subscribers_count": 1,
            "watchers_count": 52,
            "open_issues_count": 0
        },
}
```

It is possible to fetch data about a single `uuid` by passing it to the endpoint. For example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/repositories/d1a4bbb5-e6ad-426a-8303-8f132cb6fcf5/
```

returns

```json
{
    "owner": "https://secret-gorge-30655.herokuapp.com/github/developers/4f8e76e8-c068-4f21-a36d-a46c4d221c1d/",
    "github_id": "76605426",
    "owner_github_id": "7543345",
    "name": "garapa",
    "full_name": "h3nnn4n/garapa",
    "description": "A gameboy emulator, written in C with an optional tetris AI and Julia API",
    "homepage": "",
    "language": "C",
    "created_at": "2016-12-15T23:52:01Z",
    "updated_at": "2019-04-21T22:41:47Z",
    "has_downloads": true,
    "has_issues": true,
    "has_pages": false,
    "has_projects": true,
    "has_wiki": true,
    "private": false,
    "archived": false,
    "disabled": false,
    "stargazers": [
        "https://secret-gorge-30655.herokuapp.com/github/developers/5bd1a553-5059-48bc-b055-bfe04e98cd61/",
        "..."
    ],
    "stargazers_count": 12,
    "subscribers_count": 4,
    "watchers_count": 12,
    "open_issues_count": 0
}
```

Filters are also supported and fully docummented at the
[`/github/swagger`](https://secret-gorge-30655.herokuapp.com/github/swagger/)
page.

### Rate Limiting: [`/github/rate_limit/`](https://secret-gorge-30655.herokuapp.com/github/rate_limit/)
This endpoint exposes the rate limit data of the underlying github api key.
There may be no data, if no requests to the github API have been made by the
service. Each request updated this record. If no api keys are configured, then
this record will reflect the rate limits for an unauthenticated user. The
record, if it exists, will always have id `1`.  Example:

```bash
curl -H 'Accept: application/json; indent=4' -u test_user:b@t09pp#m https://secret-gorge-30655.herokuapp.com/github/rate_limit/
```

returns

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "https://secret-gorge-30655.herokuapp.com/github/rate_limit/1/",
            "rate_limit": 5000,
            "rate_remaining": 1749,
            "rate_reset_raw": 1601853380,
            "rate_reset": "2020-10-04T23:16:20Z"
        }
    ]
}
```

### Tasks: [`/github/tasks/`](https://secret-gorge-30655.herokuapp.com/github/tasks/)
Endpoint for listing available actions and triggering them. A `GET` request
lists the tasks, a `POST` requests triggers it.

Acceptable actions are:

1) `full_profile_sync`: Action for for triggering a full sync of a
developer. This updates the developer record, the followers and
following lists, starred repositories, fetches all of the developer's
repositories and its stargazer. Requires `username` to be set with a
valid github username.

2) `full_repository_sync`: Endpoint for triggering a full sync of a
repository. This fetches and updates the repository and its owner.
Stargazers are also created and updated. Requires `username` to be set
with a valid github username. Requires `repo_name` to be set with a
valid github repository name (not including the username, e.g.
`garapa` and not `h3nnn4n/garapa`).

3) `discovery_scraper`: Triggers the discovery scrapper. This by default
picks 5 users where the following, followers or repository count if out
of date and runs a full sync.

Make a post to this endpoint to trigger the action. e.g. a post with
`name=full_repository_sync`, `username=h3nnn4n` and `repo_name=garapa`
will fetch and sync the repository `h3nnn4n/garapa` asyncronously.

On a successfull `POST` request a response with code 200 and message
`{'success': 'yes'}` will be sent.

In case of failure, a response with code 406 will be sent with `'success': 'no'` and
an appropriate error message. For example:
`{'success': 'no', 'error': 'Missing repo_name. Provide a valid repository name'}`

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
`discovery_scraper`, `full_profile_sync` and `full_repository_sync` tasks are
supported.

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

## Testing

Assuming that at least the first 5 steps were followed, the test suite can be
ran with: `pipenv run python manage.py test`

## LICENSE

See [LICENSE](LICENSE)
