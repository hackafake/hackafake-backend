# hackafake-backend

The HACKAFAKE API Backend serves the HACKAFAKE RestPlus API.

The documentation of the API exposed by HACKAFAKE is available at <https://api.hackafake.it>.

The server is written in Python using the [Flask](http://flask.pocoo.org/) microframework, and documented with the [Swagger Tools](https://swagger.io/).

## How to test the server

You can locally run the server with Python.

1. Setup a virtualenv

    ```
    $ python3 -m venv env && source env/bin/activate
    ```

2. Install dependencies

    ```
    (env)$ pip install -r requirements.txt
    ```

3. Test the server

    ```
    $(env) python manage.py runserver
    ```

## License

The HACKAFAKE API Backend code is licensed under [BSD-3-Clause](LICENSE).

## Contributors

 - [Ludus Russo](https://ludusrusso.cc)
 - [Gianpaolo Macario](https://gmacario.gitub.io)

 <!-- EOF -->
