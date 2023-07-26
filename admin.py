# admin.py
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Personaje, Planeta, Vehiculo, Favorite

def setup_admin(app):
    # Configurar Flask-Admin y agregar tus modelos
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3', url='/admin')
    admin.add_view(ModelView(User, db.session, name='User Admin'))
    admin.add_view(ModelView(Personaje, db.session))
    admin.add_view(ModelView(Planeta, db.session))
    admin.add_view(ModelView(Vehiculo, db.session))
    admin.add_view(ModelView(Favorite, db.session))