from app import db

class Venta(db.Model):
    __tablename__ = 'venta'
    codigo_ven = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_pedido = db.Column(db.Integer, db.ForeignKey('pedido.codigo_ped'), nullable=False)

    def __init__(self, codigo_pedido):
        self.codigo_pedido = codigo_pedido