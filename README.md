Application available at https://car-makes.herokuapp.com/

# setup
```bash
git clone git@github.com:yellowmint/car_makes.git
cd car_makes
pipenv install
```

# start app
```bash
docker-compose up
python manage.py migrate
python manage.py runserver
```

# deploy new version
```bash
heroku container:login
make deploy
```
