# RESTful-API-for-Authentication-and-Authorisation

Command for Installing Packages:
  pip install -r requirements.txt

Command for Running the Server:
  python manage.py runserver

API for User Registartion [POST]:-
  localhost:8000/api/register
register_user.json file contain details of registered user.

API for User Login [POST]:-
  localhost:8000/api/login
Json formats for login is in login_user.json file.
The result of login will be a jwt token.

API for Showing User details after Login [GET]:-
  localhost:8000/api/user

API for Logout [POST]:-
  localhost:8000/api/logout


