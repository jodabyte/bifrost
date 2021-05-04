docker-build:
	docker-compose -f docker/docker-compose-dev.yml build
	
docker-up:
	docker-compose -f docker/docker-compose-dev.yml up -d

docker-down:
	docker-compose -f docker/docker-compose-dev.yml down -v

docker-clean:
	docker system prune -a --volumes -f