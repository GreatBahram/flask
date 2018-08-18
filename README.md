# To Do List - Flask Implementation

**Author**: Bahram Aghaei

**Python Versions**: 3.6+ only

**Extensions that has been used**:
* Flask-Restful
* Flask-JWT
* Flask-SQLAlchemy
* Flask-Bcrypt
* Flask's Blueprint to make the project modular

## Getting Started

Navigate to a directory that you want to work in and clone down this repository.

```
$ git clone https://github.com/GreatBahram/flask.git
```

### For Development

Move into the cloned directory and start a new Python 3 [virtual environment](https://docs.python.org/3/tutorial/venv.html). You should be using Python 3.6 or later.

```
$ cd flask
$ pip3 install -r requirements.txt
$ python3 run.py
```

In your virtual environment, set as environment variables the URL to the Postgres database that you intend to use for development, as well as the `FLASK_APP` environment variable with the path to the repository's `run.py` file.
For something closer to bulletproof, use the absolute path to the file.
Note that on my machine I don't need a username or password to access my postgres databases, but your own results may vary.

```
export DATABASE_URL=sqlite:///database.db
export FLASK_APP=app.py
```

Initialize your database using the provided `initializedb.py` file.
If you want to be able to drop tables before you create them, set an environment variable of `DEVELOPMENT` to `'True'`.

```
$ python initializedb.py
```

In order to run the application, type `flask run`.
If all your stuff is configured properly, your development server should be running on port 5000.
