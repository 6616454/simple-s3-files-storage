up:
	docker compose -f deploy/docker-compose.yaml up --build

down:
	docker compose -f deploy/docker-compose.yaml down -v && docker network prune --force