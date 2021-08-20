# Test task for StarNavi.

## Users: username "admin", password - "admin"; username - "test_user", password - "test_user".

| **Endpoints** | **Description** |
|---|---|
| http://localhost:8000/api/sign_up/ | Sign up a user. |
| http://localhost:8000/api/login/ | Login. |
| http://localhost:8000/api/token/ | Takes a set of user credentials and returns an access and refresh JSON web token pair to prove the authentication of those credentials. |
| http://localhost:8000/api/refresh_token/ | Takes a refresh type JSON web token and returns an access type JSON web token if the refresh token is valid. |
| http://localhost:8000/api/users/ | Returns all users. |
| http://localhost:8000/api/posts/ | Returns all posts. |
| http://localhost:8000/api/likes/ |  Returns all likes. |
| http://localhost:8000/api/analytics/2021-08-17&2021-08-20 | You can specify any date. Returns the number of likes made in the specified time interval and the number of likes sorted by day |
| http://localhost:8000/api/last_activity/ | Returns the time of the last login and the time of the last activity of the authorized user. |
| http://localhost:8000/api/like/1/ | You can specify any post id. If you use the POST method you add a like to this post, if the DELETE method you remove like from this post. |
