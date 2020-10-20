deploy:
	docker build -t registry.heroku.com/car-makes/web .
	docker push registry.heroku.com/car-makes/web
	heroku container:release -a car-makes web
