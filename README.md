# Open hackAfake API Backend

The hackAfake API Backend serves the hackAfake RestPlus API. 

The server has been written in Python using the Flask microframework, and documented with swagger!

The documentation is available on the [Swagger Autogenerated UI](https://api.hackafake.it).

## How to test

You can locally run the server with Python.

1. Setup a virtualenv

```
$ virtualenv -ppython3 env && source env/bin/activate
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

The hackAfake API Backend code is licensed under [BSD-3-Clause](./LICENSE).

## Contributors

 - [Ludus Russo](https://ludusrusso.cc)
