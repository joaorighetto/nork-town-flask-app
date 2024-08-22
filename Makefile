CONTAINER_ID := $(shell docker ps -n 1 -q) # Get the container ID of the last container created	
create-superuser:: 
	docker exec -it $(CONTAINER_ID) flask create-superuser

up::
	docker-compose up --build -d
	
down:: 
	docker-compose down

test:: 
	docker exec -it $(CONTAINER_ID) pytest -s