from app import db

class Pedido(db.Model):
    __tablename__ = 'pedido'
    codigo_ped = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.Boolean, nullable=True)
    total = db.Column(db.Integer, nullable=True)
    rut_cliente = db.Column(db.String(12), db.ForeignKey('cliente.rut_clie'), nullable=True)

    def __init__(self, estado, total, rut_cliente):
        self.estado = estado
        self.total = total
        self.rut_cliente = rut_cliente
