# Running locally
1. Install the requirements and activate the virtualenv (It's assumed that you have Pipenv installed)
```
$ pipenv install
$ pipenv shell
```
2. Run the migrations and create a superuser (SQlite3 is used for the sake of simplicity)
```
$ python manage.py migrate
$ python manage.py createsuperuser
```
3. Run the server
```
$ python manage.py runserver
```

Now, you can access the server at `127.0.0.1:8000`

# Populating DB with the testing data
1. Using the admin page, create several users
2. Active the django shell
```
$ python manage.py shell
```
3. Create a number of payment instances with the aid of the following code
```
>>> from users.models import CustomUser
>>> from payouts.models import Payment
>>> import random
>>> users = CustomUser.objects.all()
>>> for i in range(100):
...     Payment.objects.create(amount=random.randint(0, 10000), author=random.choice(users))
...
>>> exit()
```