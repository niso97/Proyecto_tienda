from app import db

class Producto(db.Model):
    __tablename__ = 'producto'
    codigo_prod = db.Column(db.Integer, primary_key=True)
    precio = db.Column(db.Integer, nullable=True)
    existencias = db.Column(db.Integer, nullable=True, default=0)  # Asegurar que existencias inicie en 0
    marca = db.Column(db.String(20), nullable=True)
    descuento = db.Column(db.Integer, nullable=True, default='0')  # Asegurar que descuento inicie en '0'
    nombre = db.Column(db.String(20), nullable=True)
    categoria = db.Column(db.String(30), db.ForeignKey('categoria.codigo_cat'), nullable=True)
    imagen = db.Column(db.String(255), nullable=True)

    def __init__(self,codigo_prod, precio=None, existencias=None, marca=None, descuento=None, nombre=None, categoria=None, imagen=None):
        self.codigo_prod = codigo_prod
        self.precio = precio
        self.existencias = existencias
        self.marca = marca
        self.descuento = descuento
        self.nombre = nombre
        self.categoria = categoria
        self.imagen = imagen
