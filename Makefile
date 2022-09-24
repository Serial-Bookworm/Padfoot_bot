build:
	docker compose up --build -d --remove-orphans -t padfoot_bot_latest

up:
	docker compose up -d

down:
	docker compose down

show_logs:
	docker compose logs

down-v:
	docker compose down -v