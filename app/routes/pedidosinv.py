from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.lista_producto import ListaProducto
from app.models.venta import Venta
from app import db

pedidosinv_bp = Blueprint('pedidosinv_bp', __name__)

def agregar_lista_productos(pedidos):
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })

@pedidosinv_bp.route('/admin')
def admin():
    productos = Producto.query.all()
    pedidos = Pedido.query.order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

@pedidosinv_bp.route('/admin/buscar-pedido', methods=['GET'])
def buscar_pedido():
    codigo_ped = request.args.get('codigo_ped')
    pedidos = Pedido.query.filter_by(codigo_ped=codigo_ped).order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    productos = Producto.query.all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

@pedidosinv_bp.route('/admin/mostrar-pedidos', methods=['GET'])
def mostrar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    productos = Producto.query.all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.producto import Producto
from app.models.pedido import Pedido
from app.models.lista_producto import ListaProducto
from app.models.venta import Venta  # Importa la clase Venta
from app import db

pedidosinv_bp = Blueprint('pedidosinv_bp', __name__)

@pedidosinv_bp.route('/admin')
def admin():
    productos = Producto.query.all()
    pedidos = Pedido.query.order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

@pedidosinv_bp.route('/admin/buscar-pedido', methods=['GET'])
def buscar_pedido():
    codigo_ped = request.args.get('codigo_ped')
    pedidos = Pedido.query.filter_by(codigo_ped=codigo_ped).order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    productos = Producto.query.all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

@pedidosinv_bp.route('/admin/mostrar-pedidos', methods=['GET'])
def mostrar_pedidos():
    pedidos = Pedido.query.order_by(Pedido.estado.asc(), Pedido.codigo_ped.desc()).all()
    productos = Producto.query.all()
    for pedido in pedidos:
        lista_productos = ListaProducto.query.filter_by(codigo_pedido=pedido.codigo_ped).all()
        pedido.lista_productos = []
        for item in lista_productos:
            producto = Producto.query.get(item.codigo_producto)
            pedido.lista_productos.append({
                'producto_nombre': producto.nombre,
                'cantidad': item.cantidad
            })
    return render_template('admin.html', productos=productos, pedidos=pedidos)

@pedidosinv_bp.route('/admin/marcar-recogido/<int:codigo_ped>', methods=['POST'])
def marcar_recogido(codigo_ped):
    pedido = Pedido.query.get_or_404(codigo_ped)
    
    # Verificar si el pedido ya está marcado como recogido
    if pedido.estado:
        flash(f'El pedido {codigo_ped} ya está marcado como recogido', 'warning')
        return redirect(url_for('pedidosinv_bp.admin'))
    
    # Marcar el pedido como recogido
    pedido.estado = True

    # Crear una nueva instancia de Venta y guardarla
    nueva_venta = Venta(codigo_pedido=codigo_ped)
    db.session.add(nueva_venta)

    # Actualizar las existencias de los productos en el pedido
    lista_productos = ListaProducto.query.filter_by(codigo_pedido=codigo_ped).all()
    for item in lista_productos:
        producto = Producto.query.get_or_404(item.codigo_producto)
        # Convertir existencias y cantidad a enteros si no lo son
        if isinstance(producto.existencias, str):
            producto.existencias = int(producto.existencias)
        if isinstance(item.cantidad, str):
            item.cantidad = int(item.cantidad)

        producto.existencias -= item.cantidad
        if producto.existencias < 0:
            flash(f'Error: El producto {producto.nombre} tiene existencias insuficientes.', 'danger')
            db.session.rollback()
            return redirect(url_for('pedidosinv_bp.admin'))

    # Confirmar los cambios en la base de datos
    try:
        db.session.commit()
        flash(f'Pedido {codigo_ped} marcado como recogido, venta registrada y existencias actualizadas', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al marcar como recogido el pedido {codigo_ped}: {str(e)}', 'danger')
    
    return redirect(url_for('pedidosinv_bp.admin'))

@pedidosinv_bp.route('/admin/eliminar-pedido', methods=['POST'])
def eliminar_pedido():
    codigo_ped = request.form.get('codigo_ped')

    if not codigo_ped:
        flash('Código de pedido no proporcionado', 'danger')
        return redirect(url_for('pedidosinv_bp.admin'))

    pedido = Pedido.query.get(codigo_ped)
    if not pedido:
        flash('Pedido no encontrado', 'danger')
        return redirect(url_for('pedidosinv_bp.admin'))

    try:
        # Eliminar los productos asociados al pedido en la tabla lista_producto
        ListaProducto.query.filter_by(codigo_pedido=codigo_ped).delete()
        # Eliminar el pedido
        db.session.delete(pedido)
        db.session.commit()
        flash(f'Pedido {codigo_ped} eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el pedido {codigo_ped}', 'danger')
    
    return redirect(url_for('pedidosinv_bp.admin'))