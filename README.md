This app was developed to present the ability in solving the following challenge:

## Nork-Town Challenge Description

>Nork-Town is a weird place. Crows cawk the misty morning while old men squint. It’s a small town, so the mayor had a bright idea to limit the number of cars a person may possess. One person may have up to 3 vehicles. The vehicle, registered to a person, may have one color: ‘yellow’, ‘blue’ or ‘gray’. And one of three models: ‘hatch’, ‘sedan’ or ‘convertible’. Carford car shop wants a system where they can add car owners and cars. Car owners may not have cars yet; they need to be marked as a sale opportunity. Cars cannot exist in the system without owners.

This repository contains the codebase for the Nork-Town project, which includes a Flask application, Docker setup, and various configuration files.

## Technicalities

The application enforces business rules at the model level using SQLAlchemy's validation and foreign key constraints. Here's how these rules are implemented:

#### 1. Enabling Foreign Key Support for SQLite

SQLite, by default, does not enforce foreign key constraints. To ensure that foreign key constraints are respected, we enable foreign key support explicitly when a connection to the SQLite database is established. This is done using an event listener in the `database.py` file:

```py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()

# Enable foreign key support for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if dbapi_connection.__class__.__module__ == 'sqlite3':
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
```

This way a `Car` can't be created without a valid `owner_id` that references an existing `Person` record.

#### 2. Validating car limit with `validate_owner_car_limit`

The `Car` model includes a validation method `validate_owner_car_limit` to enforce the business rule that an owner cannot have more than three cars. This is implemented using SQLAlchemy's `@validates` decorator:

```py
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.Enum(CarModel), nullable=False)
    color = db.Column(db.Enum(CarColor), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id', ondelete="CASCADE"), nullable=False)

    @validates('owner_id')
    def validate_owner_car_limit(self, key, owner_id):
        owner_cars_count = db.session.query(Car).filter_by(owner_id=owner_id).count()
        if owner_cars_count >= 3:
            raise IntegrityError('Owner cannot have more than 3 cars.', params=None, orig=None)
        return owner_id
```

#### 3. Cascade effect on deleting a person

Additionally, when a `Person` is deleted, all of their related `Car` records are also deleted due to the `CASCADE` option on the foreign key constraint.

## `Makefile`

The `Makefile` provides convenient commands for managing the Docker containers and running custom commands. It includes targets for starting and stopping the Docker containers, as well as creating a superuser and testing the application.

```makefile
CONTAINER_ID := $(shell docker ps -n 1 -q) 

create-superuser:: 
	docker exec -it $(CONTAINER_ID) flask create-superuser

up:: 
	docker-compose up -d --build

down:: 
	docker-compose down

test:: 
	docker exec -it $(CONTAINER_ID) pytest -s

prepare::
		test -r $(ENV_FILE) -o ! -r $(ENV_FILE).example || cp $(ENV_FILE).example $(ENV_FILE)
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

**IMPORTANT!** Full access to the admin interface requires creating a superuser by running the following command:

```bash
make create-superuser
```

This will prompt you to enter a username and password for the superuser.

### Setting `.env` file

To create the necessary `.env` file, run the following command:

```bash
make prepare
```

This will ensure that a `.env` file exists and is readable. If the `.env` file does not exist or is not readable, one will be created from an example file (`.env.example`) which is available and readable, creating a new `.env` file by copying the example file.