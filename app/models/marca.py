from app import db

class Marca(db.Model):
    __tablename__ = 'marca'
    codigo = db.Column(db.String(6), primary_key=True)
    descuento = db.Column(db.String(5), nullable=True)
    nombre = db.Column(db.String(20), nullable=True)

    def __init__(self, codigo, descuento=None, nombre=None):
        self.codigo = codigo
        self.descuento = descuento
        self.nombre = nombre
