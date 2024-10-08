from app import db

class Factura(db.Model):
    __tablename__ = 'factura'
    id_fact = db.Column(db.Integer, primary_key=True)
    total_pago = db.Column(db.String(20), nullable=True)
    fecha_emision = db.Column(db.DateTime, nullable=True)
    subtotal = db.Column(db.String(20), nullable=True)
    impuestos_aplicables = db.Column(db.String(4), nullable=True)
    rut_proveedor = db.Column(db.String(12), db.ForeignKey('proveedor.rut_prov'), nullable=True)

    def __init__(self, total_pago, fecha_emision, subtotal, impuestos_aplicables, rut_proveedor):
        self.total_pago = total_pago
        self.fecha_emision = fecha_emision
        self.subtotal = subtotal
        self.impuestos_aplicables = impuestos_aplicables
        self.rut_proveedor = rut_proveedor
