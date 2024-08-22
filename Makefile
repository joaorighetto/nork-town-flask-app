CONTAINER_ID := $(shell docker ps -n 1 -q) # Get the container ID of the last container created	
ENV_FILE := .env

create-superuser:: 
	docker exec -it $(CONTAINER_ID) flask create-superuser

up::
	docker-compose up --build -d
	
down:: 
	docker-compose down

test:: 
	docker exec -it $(CONTAINER_ID) pytest -s

prepare::
		test -r $(ENV_FILE) -o ! -r $(ENV_FILE).example || cp $(ENV_FILE).example $(ENV_FILE)