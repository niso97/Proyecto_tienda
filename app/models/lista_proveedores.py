from app import db

class ListaProveedores(db.Model):
    __tablename__ = 'lista_proveedores'
    idlista = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_prod = db.Column(db.Integer, db.ForeignKey('producto.codigo_prod'), nullable=False)
    codigo_proveedor = db.Column(db.String(12), db.ForeignKey('proveedor.rut_prov'), nullable=False)

    def __init__(self, codigo_prod, codigo_proveedor):
        self.codigo_prod = codigo_prod
        self.codigo_proveedor = codigo_proveedor
