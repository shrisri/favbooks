# Rest API Service



### OBJECTIVE
 The objective of this project is to create a Rest API service which will
- Authenticate user with JWT Tokens
- Perform CRUD Operations for a User's list of Favorite books.
- Check for expired token and re-authenticate
 
### INSTRUCTIONS TO GET STARTED

 1. Download and unzip 'python_rest.zip'<br/>
 2. Goto 'venv' directory <br/>
 3. To install virtualenv, run 'pip install virtualenv'<br/>
 4. To install other pre-requisites, run 'pip install -r req.txt'<br/>
 5. Now run the web service with 'python3 favbooks.py' <br/>
 6. Download Postman or Insomnia to validate the Rest API <br/>
 
 ### INSTRUCTIONS TO TEST THE PROGRAM
 
**TO REGISTER USER** <br/>
METHOD: POST <br/>
URL: http://127.0.0.1:5000/register <br/>
 
 INPUT:
 <pre>
                {
                "name":<_name_>,
                "password":<_password_>
                }
 </pre>
 OUTPUT:
 <pre>
                {
                "message": "registered successfully"
                }
</pre>                  
                            
**FOR USER LOGIN** <br/>
METHOD: GET <br/>
URL: http://127.0.0.1:5000/login <br/>
INPUT: Enter username and password fields using basic authentication <br/>
OUTPUT:
<pre>
                {      
                  "token":  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiI3NDU0YzFhZi02YTE4LTQzYjItYTk1Zi01Njc4NjFjNmYzZTQiLCJleHAiOjE1ODY1OTk2MDF9.2AllM9ZwIxg7sie0lK9JXS6QG6TfnL7TQztZc7vzK0Q"
                 }
 </pre>             
                             
 **TO SEE ALL USERS DETAILS** <br/>
 METHOD: GET <br/>
 URL: http://127.0.0.1:5000/users <br/>
 OUTPUT:
<pre>
        {
                 "users": [
                     {
                      "name": "Shriya",
                       "password": "sha256$hp1j8NG0$34c2800d7b1b9834d4c839cfd8aa4e8572c0529184111c0463d94a8a200d934d",
                        "public_id": "7454c1af-6a18-43b2-a95f-567861c6f3e4"
                     }
                ]
       }                             
    </pre>                         
                             
 **TO ADD FAVOURITE BOOK** <br/>
 METHOD: POST <br/>
 URL: http://127.0.0.1:5000/addfav <br/>
 INPUT:
  <pre>
       {
         "title": <_title_>,"amazon_url": <_amazon_url_>,
         "author": <_author_name_>,
         "genre": <_genre_>
       }
</pre>
Add a new header called 'x-access-tokens' and value as the random token generated during login
OUTPUT:
<pre>
      {
       "message": "new favourite book added"
      }
 </pre>
 
 **TO SEE DETAILS OF ALL FAVOURITE BOOKS** <br/>
 METHOD: GET <br/>
 URL: http://127.0.0.1:5000/favbooks <br/>
 INPUT:  Add a new header called 'x-access-tokens' and value as the random token generated during login

 OUTPUT:
 <pre>
      {
       "your favorite books": [
        {
       "amazon_url": "https://www.amazon.in/Mysterious-Island-Wordsworth-Classics/dp/1840226242/ref=sr_1_1?dchild=1&keywords=mysterious+island&qid=1586598118&sr=8-1",
       "author": "Jules Verne",
        "genre": "Mystery",
         "id": 1,
        "title": "The Mysterious island"
          }
         ]
     }
  </pre>
  
  **TO DELETE FAVOURITE BOOK** <br/>
  METHOD: DELETE <br/>
  URL: http://127.0.0.1:5000/favbooks/<_book_id_><br/>
  INPUT: Add a new header called 'x-access-tokens' and value as the random token generated during login <br/>
  OUTPUT:
  <pre>
          {
          "message": "Book deleted"
          }
   </pre>                          
                             
  **TO UPDATE FAVOURITE BOOK** <br/>
  METHOD: PUT <br/>
  URL: http://127.0.0.1:5000/favbooks/<_book_id_> <br/>
  INPUT:
     <pre>
                {
                  "title": <_title_>,"amazon_url": <_amazon_url_>,
                  "author": <_author_name_>,
                  "genre": <_genre_>
                }
     </pre>
                
 Add a new header called 'x-access-tokens' and value as the random token generated during login <br/>
 OUTPUT: 
     <pre>
            {
              "message": "Book updated"
            }
      </pre>
                             
 
 
