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

The API will return three error type when requests: <br>
* 400: Bad request 
* 404: Resource not found 
* 405: Method now allowed 

## Endpoints
<br>

## GET /books
* ### General:
    * This endpoint returns books list and their number
    * Results are paginated in groups of 8. Include a request argument to choose page, starting from 1.
* ### Example
    * Request: ```http://127.0.0.1:5000/books``` <br>
    * Response:
    * ```
        {
            "books": [
                {
                    "author": "Keyl Nyuport",
                    "id": 10,
                    "rating": 1,
                    "title": "Diqqat"
                }
            ],
            "success": true,
            "total_books": 1
        }
    ```

    * To get books from other pages: ``` http://127.0.0.1:5000/book?page=2 ```
    ## /book?page=2
    This endpoint returns all books from the second page, if second page doesn't exists it will return books not found
    
<br>

## GET /books/id
* ### General: