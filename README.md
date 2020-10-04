# ikai-server
This is the code for the backend of the app [ikai](https://github.com/mhk19/ikai). <br /> It is based on the Django REST framework.
It holds the data of the users registered on the ikai app and is used to query different requests regarding information about users.
## Setup
1. Clone the repository and create a python3 virtual environment in the root of the project <br />
```virtualenv env``` <br />
Now, activate the virtual environment using ```source/bin/activate```
2. Now run the command: <br />
``` pip3 install -r requiements.txt ``` <br />
3. Now go inside to ikai-server/ikai-server and run:
``` python3 manage.py makemigrations
    python3 manage.py migrate
    python3 manage.py runserver 
```
## API Endpoints
/users/chatrooms -> fetches all verfied chatrooms for the authenticated user <br />
/users/accept?user=<username> -> authenticated user accepts request of specified user <br />
users/pending -> gets all friend requests of authenticated user <br />
users/search?query=<searchquery> => searches for all users in database with a username and return their status and relatiionshop with authenticated user
