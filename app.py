import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

from flask_admin.contrib.sqla import ModelView
from models import db, User, Personaje, Planeta, Vehiculo, Favorite


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/postgres'

# Inicializar la base de datos
db.init_app(app)

# Configurar Flask-Migrate
migrate = Migrate(app, db)

admin = Admin(app, name='Titoshiro Admin', template_mode='bootstrap3', url='/admin')
admin.add_view(ModelView(User, db.session, name='User Admin'))
admin.add_view(ModelView(Personaje, db.session))
admin.add_view(ModelView(Planeta, db.session))
admin.add_view(ModelView(Vehiculo, db.session))
admin.add_view(ModelView(Favorite, db.session))

# Ruta para obtener la lista de usuarios
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():
    personajes = Personaje.query.all()
    return jsonify([personaje.serialize() for personaje in personajes])

@app.route('/personajes/<int:id>', methods=['GET'])
def get_personaje(id):
    personaje = Personaje.query.get(id)
    if not personaje:
        return jsonify({"message": "Personaje no encontrado"}), 404
    return jsonify(personaje.serialize())

@app.route('/planetas', methods=['GET'])
def get_planetas():
    planetas = Planeta.query.all()
    return jsonify([planeta.serialize() for planeta in planetas])

@app.route('/planetas/<int:id>', methods=['GET'])
def get_planeta(id):
    planeta = Planeta.query.get(id)
    if not planeta:
        return jsonify({"message": "Planeta no encontrado"}), 404
    return jsonify(planeta.serialize())

# Rutas para Vehiculos
@app.route('/vehiculos', methods=['GET'])
def get_vehiculos():
    vehiculos = Vehiculo.query.all()
    return jsonify([vehiculo.serialize() for vehiculo in vehiculos])

@app.route('/vehiculos/<int:id>', methods=['GET'])
def get_vehiculo(id):
    vehiculo = Vehiculo.query.get(id)
    if not vehiculo:
        return jsonify({"message": "Vehiculo no encontrado"}), 404
    return jsonify(vehiculo.serialize())

# Ruta para obtener los favoritos de un usuario
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = 1
    # Obtener el usuario de la base de datos
    user = User.query.get(user_id)
    # Verificar si el usuario existe en la base de datos
    if user is None:
        return jsonify({"message": "User not found"}), 404
    # Obtener los favoritos del usuario 
    favorites = user.get_favorites()
    # Devolver los favoritos del usuario 
    return jsonify(favorites), 200







# Ruta para agregar un planeta a los favoritos de un usuario
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet_to_favorites(planet_id):
    user_id = 1
    # Obtener el usuario de la base de datos
    user = User.query.get(user_id)
    # Verificar si el usuario existe en la base de datos
    if user is None:
        return jsonify({"message": "User not found"}), 404
    # Obtener el planeta de la base de datos
    planet = Planeta.query.get(planet_id)
    # Verificar si el planeta existe en la base de datos
    if planet is None:
        return jsonify({"message": "Planet not found"}), 404
    # Agregar el planeta a los favoritos 
    user.add_favorite(planet)
    # Guardar los cambios 
    db.session.commit()

    return jsonify({"message": f"Planet with ID {planet_id} added to favorites"}), 200

@app.route('/favorite/personaje/<int:personaje_id>', methods=['POST'])
def add_personaje_to_favorites(personaje_id):
    user_id = 1
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "personaje not found"}), 404

    personaje = Personaje.query.get(personaje_id)
    if personaje is None:
        return jsonify({"message": "personaje not found"}), 404

    # Agregar el personaje a los favoritos del usuario
    user.add_favorite(personaje)
    # Guardar los cambios en la base de datos
    db.session.commit()

    return jsonify({"message": f"Personaje with ID {personaje_id} added to favorites"}), 200

@app.route('/favorite/personaje/<int:personaje_id>', methods=['DELETE'])
def remove_people_from_favorites(personaje_id):
    user_id = 1
    user = User.query.get(user_id)
    if user is None:
       return jsonify({"message": "personaje not found"}), 404

    personaje = Personaje.query.get(personaje_id)
    if personaje is None:
        return jsonify({"message": "personaje not found"}), 404

    user.remove_favorite(personaje)
    db.session.commit()

    return jsonify({"message": f"Personaje with ID {personaje_id} removed from favorites"}), 200


@app.route('/favorite/planet/<int:id>', methods=['DELETE'])
def remove_planet_from_favorites(id):
    user_id = 1
    user = User.query.get(user_id)
    if user is None:
       return jsonify({"message": "planeta not found"}), 404

    planet = Planeta.query.get(id)
    if planet is None:
        return jsonify({"message": "planeta not found"}), 404

    user.remove_favorite(planet)
    db.session.commit()

    return jsonify({"message": f"Planet with ID {id} removed from favorites"}), 200





if __name__ == "__main__":
    with app.app_context():
        # Crear las tablas si no existen
        db.create_all()
      

    app.run(debug=True)
