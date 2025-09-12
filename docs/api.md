# API Documentation



| Path / Method  | Description                 | Request (Input)                             | Response (Output)                                                                                                                       | Info                          |
|----------------|-----------------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|
| POST /register | endpoint to a register form | Body: {"username": "...", "password","..."} | (201): user created, response-body: {"id": "...", "username": "..."}<br/>(400): wrong or missing input<br/>(409): username already used | -                             |
| POST /login    | endpoint to a login form    | Body: {"username": "...", "password","..."} | set session cookie<br/>response-body: {"message": "login successful"}<br/>(401): wrong credentials                                      | sets session cookie           |
| POST /logout   | endpoint to logout          | session cookie                              | (200): {"message", "logged out"}                                                                                                        | serverside session delete     |
| GET  /me       | endpoint for identification | session cookie                              | (200): {"id" : ..., "username": "..."}<br/>(401): invalid cookie or no session                                                          | requires valid session cookie |