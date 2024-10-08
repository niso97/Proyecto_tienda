from app import db

class Categoria(db.Model):
    __tablename__ = 'categoria'
    codigo_cat = db.Column(db.String(30), primary_key=True)
    descuento = db.Column(db.String(3), nullable=True)
    nombre = db.Column(db.String(20), nullable=True)

    def __init__(self, codigo_cat, descuento=None, nombre=None):
        self.codigo_cat = codigo_cat
        self.descuento = descuento
        self.nombre = nombre
