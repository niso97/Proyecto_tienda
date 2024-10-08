from app import db

class ListaFactura(db.Model):
    __tablename__ = 'lista_factura'
    codigo_factprod = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cantidad_producto = db.Column(db.String(10), nullable=True)
    costo = db.Column(db.String(20), nullable=True)
    id_factura = db.Column(db.Integer, db.ForeignKey('factura.id_fact'), nullable=True)
    codigo_producto = db.Column(db.Integer, db.ForeignKey('producto.codigo_prod'), nullable=True)
    vencimiento = db.Column(db.DateTime, nullable=True)

    def __init__(self, cantidad_producto, costo, id_factura, codigo_producto, vencimiento,):
        self.cantidad_producto = cantidad_producto
        self.costo = costo
        self.id_factura = id_factura
        self.codigo_producto = codigo_producto
        self.vencimiento = vencimiento