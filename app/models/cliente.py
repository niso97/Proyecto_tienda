from app import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    rut_clie = db.Column(db.String(12), primary_key=True)
    nombre = db.Column(db.String(30), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    contrasena = db.Column(db.String(20), nullable=True)
    direccion = db.Column(db.String(30), nullable=True)
    edad = db.Column(db.Integer, nullable=True)

    def __init__(self, rut_clie, nombre=None, correo=None, contrasena=None, direccion=None, edad=None):
        self.rut_clie = rut_clie
        self.nombre = nombre
        self.correo = correo
        self.contrasena = contrasena
        self.direccion = direccion
        self.edad = edad
