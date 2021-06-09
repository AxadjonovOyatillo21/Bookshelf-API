## Get Started
* Base URL: At present this app can be run locally and it hosted by default. Default local url: ``` http://127.0.0.1:5000 ```
* Authentication: This version of API does not require api keys

<br>


# ⚠️ Attention ⚠️
* In Examples we send request using postman<img src="http://cdn.auth0.com/blog/postman-integration/logo.png" alt="postman" width="21px" height="21px">, you can do it using curl


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
    ```
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

## GET /books/{book_id}
* ### General:
    * This endpoint returns specific book
* ### Example
    * Requests: ``` https://127.0.0.1:/5000/books/10 ``` - this endpoint returns book which id is 10
    * Response:
    ```
        {
            "author": "Keyl Nyuport",
            "id": 10,
            "rating": 1,
            "success": true,
            "title": "Diqqat"
        }
    ```

* ### ⚠️ Warning
    * If you in your request enter a book id which does not exists in database, API returns error with message books not found
    * Example:
        * Request: ``` http://127.0.0.1:5000/books/121221212 ```
        * Response:
        ```
            {
                "message": "books not found",
                "success": false
            }
        ```
## POST /books/search
* ### General:
    * This endpoint returns searching resulsts
    * You should request to this endpoint with post method. ⚠️ request body should include JSON data which includes 'search' key and value
* ### Example:
    * Request: ``` POST/ 127.0.0.1:5000/books/search ``` 
        * Request body:
        ``` 
            {
                "search": "diqqat"
            }
        ```
        * Response:
        ```
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
* ### ⚠️ Warning
    * If you send empty request or request which not includes important value, API responses 400 erorr with message 'bad request'
    * Example:
        * Request: ``` POST/ http://127.0.0.1:5000/books/search ```
            * Request body:
            ```
                {
                    "uncorrect_key": "uncorrect_value"
                }
            ```
            or empty request body:
            ```
                {}
            ```
            * Response:
            ```
                {
                    "error": 400,
                    "message": "bad request",
                    "success": false
                }
            ```      
      
