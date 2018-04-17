# Open hackafake API

**FIXME**: Use API introspection at <http://hackafake.it:8080/>

 - GET `/counter`

```
{
    "cnt": "integer"
}
```

 - GET `/fakenews?num=10`

```
{
    "fake news": [
        {
            "url": "url",
            "counter": "integer",
            "$uri": "url",
            "users": ["string", "string"],
            "$date": "timestamp"
        }
    ]
}
```

 - GET `/users?num=10`
```
{
    "users": [
        {
            "user": "string",
            "counter": "integer",
            "urls": ["url", "url"] 
        }
    ]
}
```
