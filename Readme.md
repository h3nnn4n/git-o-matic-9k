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

### Endpoints

Four endpoints make part of the git-o-matic-9k API:

1) `/github/developers/`: This endpoint exposes a list of all developers (that
were synced). All relations are hyperlinked. For example:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
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
                "http://127.0.0.1:8000/github/developers/b136112b-3ff0-47d3-bbaa-01471666fbe4/",
                "..."
            ],
            "following": [
                "http://127.0.0.1:8000/github/developers/6bd3c1ef-f820-41ed-b937-ff026cb45c4c/",
                "..."
            ],
            "starred_repositories": [
                "http://127.0.0.1:8000/github/repositories/21ffcb9d-136c-4def-944f-73716e63b00e/",
                "..."
            ],
            "repositories": [
                "http://127.0.0.1:8000/github/repositories/e9d7a3f4-bd8c-4c32-bc7a-7442a61aecb0/",
                "..."
            ]
        }
    ]
}
```

Passing an developer/user `uuid` to this endpoint fetches a single user. Example:

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
        "http://127.0.0.1:8000/github/developers/b136112b-3ff0-47d3-bbaa-01471666fbe4/",
        "..."
    ],
    "following": [
        "http://127.0.0.1:8000/github/developers/6bd3c1ef-f820-41ed-b937-ff026cb45c4c/",
        "..."
    ],
    "starred_repositories": [
        "http://127.0.0.1:8000/github/repositories/21ffcb9d-136c-4def-944f-73716e63b00e/",
        "..."
    ],
    "repositories": [
        "http://127.0.0.1:8000/github/repositories/e9d7a3f4-bd8c-4c32-bc7a-7442a61aecb0/",
        "..."
    ]
}
```

Filters are also supported and fully docummented at the
[`/github/swagger`](https://secret-gorge-30655.herokuapp.com/github/swagger/)
page.

2) `/github/repositories/`: This endpoint exposes a list of all repositories
(that were synced). All relations are hyperlinked. For example:

```json
{
    "count": 982,
    "next": "http://127.0.0.1:8000/github/repositories/?page=4",
    "previous": "http://127.0.0.1:8000/github/repositories/?page=2",
    "results": [
        {
            "owner": "http://127.0.0.1:8000/github/developers/6222c4b4-d70e-4c70-ad7b-ee79685dac86/",
            "github_id": "300252307",
            "owner_github_id": "9753063",
            "name": "papers",
            "full_name": "h31nr1ch/papers",
            "description": null,
            "homepage": null,
            "language": null,
            "created_at": "2020-10-01T11:19:43Z",
            "updated_at": "2020-10-01T12:13:55Z",
            "has_downloads": true,
            "has_issues": true,
            "has_pages": false,
            "has_projects": true,
            "has_wiki": true,
            "private": false,
            "archived": false,
            "disabled": false,
            "stargazers": ["..."],
            "stargazers_count": 0,
            "subscribers_count": 1,
            "watchers_count": 0,
            "open_issues_count": 0
        },
    ]
}
```

It is possible to fetch data about a single `uuid` by passing it to the endpoint.

```json
{
    "owner": "http://127.0.0.1:8000/github/developers/f895512a-4a85-4784-aac8-2dc1fd4781a7/",
    "github_id": "37652385",
    "owner_github_id": "20063",
    "name": "cargo-edit",
    "full_name": "killercup/cargo-edit",
    "description": "A utility for managing cargo dependencies from the command line.",
    "homepage": "http://killercup.github.io/cargo-edit/",
    "language": "Rust",
    "created_at": "2015-06-18T10:12:57Z",
    "updated_at": "2020-10-04T16:09:24Z",
    "has_downloads": true,
    "has_issues": true,
    "has_pages": true,
    "has_projects": true,
    "has_wiki": false,
    "private": false,
    "archived": false,
    "disabled": false,
    "stargazers": [
        "http://127.0.0.1:8000/github/developers/d2616208-be58-4a4d-ab62-b5d487588101/",
        "..."
    ],
    "stargazers_count": 1421,
    "subscribers_count": 19,
    "watchers_count": 1421,
    "open_issues_count": 50
}
```

Filters are also supported and fully docummented at the
[`/github/swagger`](https://secret-gorge-30655.herokuapp.com/github/swagger/)
page.

3) `/github/rate_limit/`: This endpoint exposes the rate limit data of the
underlying github api key. There may be no data, if no requests to the github
API have been made by the service. Each request updated this record. If no api
keys are configured, then this record will reflect the rate limits for an
unauthenticated user. The record, if it exists, will always have id `1`.
Example:

```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "url": "http://127.0.0.1:8000/github/rate_limit/1/",
            "rate_limit": 5000,
            "rate_remaining": 1749,
            "rate_reset_raw": 1601853380,
            "rate_reset": "2020-10-04T23:16:20Z"
        }
    ]
}
```

4) `/github/tasks/`: Endpoint for listing available actions and triggering
them. A `GET` request lists the tasks, a `POST` requests triggers it.

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

### Testing

Assuming that at least the first 5 steps were followed, the test suite can be
ran with: `pipenv run python manage.py test`

## LICENSE

See [LICENSE](LICENSE)
