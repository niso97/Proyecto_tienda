from flask import Blueprint, render_template, redirect, url_for, session, request  # Agregar request desde Flask
from ..models.producto import Producto
from ..models.cliente import Cliente

cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/cliente')
def cliente():
    # Obtener todos los productos
    products = Producto.query.all()

    # Obtener el carrito desde la sesión
    cart = session.get('cart', [])

    # Obtener el nombre del cliente si está en la sesión
    nombre_cliente = None
    if 'rut_clie' in session:
        rut_clie = session['rut_clie']
        cliente = Cliente.query.get(rut_clie)
        if cliente:
            nombre_cliente = cliente.nombre

    # Obtener el total_descuento de los argumentos de la URL
    total_descuento = request.args.get('total_descuento', 0, type=float)

    # Renderizar la plantilla con los datos obtenidos
    return render_template('cliente.html', products=products, cart=cart, nombre_usuario=nombre_cliente, total_descuento=total_descuento)
