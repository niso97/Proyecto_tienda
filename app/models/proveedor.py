from app import db

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    rut_prov = db.Column(db.String(12), primary_key=True)
    razon_social = db.Column(db.String(100), nullable=True)
    correo = db.Column(db.String(100), nullable=True)
    telefono = db.Column(db.Integer, nullable=True)
    direccion = db.Column(db.String(30), nullable=True)
    representante = db.Column(db.String(30), nullable=True)
    codigo = db.Column(db.String(5), nullable=True)

    def __init__(self, rut_prov, razon_social, correo, telefono, direccion, representante, codigo):
        self.rut_prov = rut_prov
        self.razon_social = razon_social
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.representante = representante
        self.codigo = codigo
