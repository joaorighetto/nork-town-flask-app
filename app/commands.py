from app.models import User
from app.database import db


def register_commands(app):
    @app.cli.command('create-superuser')
    def create_superuser():
        """Create a superuser."""
        username = input('Username: ')
        password = input('Password: ')
        
        user = User(username=username, is_admin=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        print(f'Superuser {username} created successfully.')