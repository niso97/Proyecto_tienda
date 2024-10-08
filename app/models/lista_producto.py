from app import db

class ListaProducto(db.Model):
    __tablename__ = 'lista_producto'
    codigo_prodpedi = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad = db.Column(db.String(10), nullable=True)
    codigo_producto = db.Column(db.Integer, db.ForeignKey('producto.codigo_prod'), nullable=True)
    codigo_pedido = db.Column(db.Integer, db.ForeignKey('pedido.codigo_ped'), nullable=True)

    def __init__(self, cantidad, codigo_producto, codigo_pedido):
        self.cantidad = cantidad
        self.codigo_producto = codigo_producto
        self.codigo_pedido = codigo_pedido
