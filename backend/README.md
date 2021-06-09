## Get Started
* Base URL: At present this app can be run locally and it hosted by default. Default local url: ``` http://127.0.0.1:5000 ```
* Authentication: This version of API does not require api keys

<br>

## Error Handling
Errors are returned as JSON objects in folloving format:
```
    {
        "error": 404,
        "message": "resource not found",
        "success": false
    }
```

The API will return three error type when requests:
    * 400: Bad request
    * 404: Resource not found
    * 405: Method now allowed