# Nork-Town

Nork-Town is a weird place. Crows cawk the misty morning while old men squint. It’s a small town, so the mayor had a bright idea to limit the number of cars a person may possess. One person may have up to 3 vehicles. The vehicle, registered to a person, may have one color: ‘yellow’, ‘blue’ or ‘gray’. And one of three models: ‘hatch’, ‘sedan’ or ‘convertible’. Carford car shop wants a system where they can add car owners and cars. Car owners may not have cars yet; they need to be marked as a sale opportunity. Cars cannot exist in the system without owners.

This repository contains the codebase for the Nork-Town project, which includes a Flask application, Docker setup, and various configuration files.

### `Makefile`

The `Makefile` provides convenient commands for managing the Docker containers and running custom commands. It includes targets for starting and stopping the Docker containers, as well as creating a superuser.

```makefile
CONTAINER_ID := $(shell docker ps -n 1 -q) # Get the container ID of the last container created

up:: 
	docker-compose up -d --build

down:: 
	docker-compose down

create-superuser:: 
	docker exec -it $(CONTAINER_ID) flask create-superuser
```

## Usage

### Starting the Application

To start the application, run the following command:

```bash
make up
```

### Stopping the Application

To stop the application, run the following command:

```bash
make down
```

### Creating a Superuser

To create a superuser, run the following command:

```bash
make create-superuser
```

This will prompt you to enter a username and password for the superuser.



