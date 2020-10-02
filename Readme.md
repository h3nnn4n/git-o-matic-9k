# GIT-O-MATIC-9K

Vrum vrum

# Local setup

If running `pipenv install` fails with an error related to `psycopg2`, then
running the following before running `pipenv install` again might solve the
issue, assuming you are on macos and installed openssl with homebrew:
```
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"
```

# LICENSE

See [LICENSE](LICENSE)
