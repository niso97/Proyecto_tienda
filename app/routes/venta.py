from flask import Blueprint, render_template
from app import db
from app.models.venta import Venta
from app.models.pedido import Pedido
from app.models.lista_producto import ListaProducto
from app.models.producto import Producto

ventas_bp = Blueprint('ventas_bp', __name__)

def obtener_detalles_venta():
    ventas = Venta.query.all()
    detalles_ventas = []

    for venta in ventas:
        pedido = Pedido.query.get(venta.codigo_pedido)
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        
        productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            productos.append({
                'nombre': producto.nombre,
                'cantidad': item.cantidad
            })

        detalles_ventas.append({
            'codigo_ven': venta.codigo_ven,
            'codigo_pedido': pedido.codigo_ped,
            'total': pedido.total,
            'productos': productos
        })
    
    return detalles_ventas

@ventas_bp.route('/ventas')
def mostrar_ventas():
    detalles_ventas = obtener_detalles_venta()
    return render_template('ventas.html', ventas=detalles_ventas)