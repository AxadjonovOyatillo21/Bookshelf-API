## Get Started
* Base URL: At present this app can be run locally and it hosted by default. Default local url: ``` http://127.0.0.1:5000 ```
* Authentication: This version of API does not require api keys

<br>


## ⚠️ Attention ⚠️
* In Examples we send request using postman <img src="http://cdn.auth0.com/blog/postman-integration/logo.png" alt="postman" width="21px" height="21px"> , you can do it using curl


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
                    "author": "Kel Newport",
                    "id": 1,
                    "rating": 6,
                    "title": "Attention"
                }
            ],
            "success": true,
            "total_books": 2
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
    * Requests: ``` https://127.0.0.1:/5000/books/1 ``` - this endpoint returns book which id is 10
    * Response:
    ```
        {
            "author": "Kel Newport",
            "id": 1,
            "rating": 6,
            "success": true,
            "title": "Attention"
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
                "search": "attention"
            }
        ```
        * Response:
        ```
            {
                "books": [
                    {
                        "author": "Kel Newport",
                        "id": 1,
                        "rating": 6,
                        "title": "Attention"
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
      
## POST /books
* ### General:
    * In this endpoint you can create a new book.
    * You should send request with method post. Your request should include JSON data about new book


    * JSON data should include:
    ```
        "author" - book author
        "title" - book title
        "rating" - book rating
    ```
    * Then API responses data which includes:
    ```
        "books" - all books list,
        "created" - id of new book,
        "success" - True,
        "total_books" - number of all books
    ```


* ### Example:
    * Request: ``` POST/ http://127.0.0.1:5000/books ```
        * Request body:
        ```
            {
                "title": "The Great Alone",
                "author": "Kristin Hannah",
                "rating": "4"
            }
        ```
    * Response:
    ```
        {
            "books": [
                {
                    "author": "Kel Newport",
                    "id": 1,
                    "rating": 6,
                    "title": "Attention"
                },
                {
                    "author": "Kristin Hannah",
                    "id": 2,
                    "rating": 4,
                    "title": "The Great Alone"
                }
            ],
            "success": true,
            "total_books": 2
        }
    ```

* ### ⚠️ Warning
    * If in your request body, in JSON data not includes one of required parametres, API responses 400 error with message 'bad request'
    * Example:
        * Request ``` POST/ http://127.0.0.1:5000/books ```
            * Request body:
            ```
                {
                    "title": "no_title"
                }
            ``` 
            - in this request required "author" parameter

            or

            ```
                {
                    "title": "title_of_book",
                    "author": ""
                }
            ``` 
            - in this request "author" parameter empty

            or 

            ```
                {
                    "author": "author_of_book"
                }
            ``` 
            - "title" parameter required

            ⚠️ "rating" parameter is not required, by default its value equals to zero.
            If "rating" not zero, you can include rating parameter to JSON data
            
        * Response:
        ```
            {
                "error": 400,
                "message": "bad request",
                "success": false
            }
        ```
