from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify 
from ..models.producto import db, Producto
from ..models.pedido import db, Pedido
from ..models.cliente import db, Cliente
from ..models.lista_producto import db, ListaProducto
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError


cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/cliente')
def cliente():
    products = Producto.query.all()
    cart = session.get('cart', [])
    subtotal_pedido = sum(item['precio'] * item['cantidad'] for item in cart)
    total_descuento = sum(item['precio'] * item['cantidad'] * item.get('descuento', 0) / 100 for item in cart)
    total_pedido = subtotal_pedido - total_descuento
    return render_template('cliente.html', products=products, cart=cart, subtotal_pedido=subtotal_pedido, total_descuento=total_descuento, total_pedido=total_pedido)

carrito_bp = Blueprint('carrito_bp', __name__)

@carrito_bp.route('/add_to_cart/<int:codigo_prod>', methods=['POST'])
def add_to_cart(codigo_prod):
    # Function implementation
    product = Producto.query.get_or_404(codigo_prod)
    if 'cart' not in session:
        session['cart'] = []

    # Check if the product is already in the cart
    for item in session['cart']:
        if item['codigo_prod'] == codigo_prod:
            if item['cantidad'] < product.existencias:
                item['cantidad'] += 1
                session.modified = True
                update_cart_totals()
            return redirect(url_for('cliente_bp.cliente'))

    # Calculate discounted price if applicable
    precio_descuento = product.precio
    if product.descuento and int(product.descuento) > 0:
        precio_descuento = product.precio * (1 - int(product.descuento) / 100)

    # Add the product to the cart with initial quantity 1
    if product.existencias > 0:
        session['cart'].append({
            'codigo_prod': product.codigo_prod,
            'nombre': product.nombre,
            'precio': precio_descuento,
            'imagen': url_for('static', filename=f'IMG/productos/{product.imagen}'),
            'cantidad': 1
        })
        session.modified = True

    # Update cart totals
    update_cart_totals()

    return redirect(url_for('cliente_bp.cliente'))



@carrito_bp.route('/remove_from_cart/<int:codigo_prod>', methods=['POST'])
def remove_from_cart(codigo_prod):
    cart = session.get('cart', [])
    updated_cart = [item for item in cart if item['codigo_prod'] != codigo_prod]
    session['cart'] = updated_cart
    session.modified = True
    update_cart_totals()
    return redirect(url_for('cliente_bp.cliente'))

@carrito_bp.route('/change_quantity/<action>/<int:codigo_prod>', methods=['POST'])
def change_quantity(action, codigo_prod):
    if 'cart' in session:
        for item in session['cart']:
            if item['codigo_prod'] == codigo_prod:
                product = Producto.query.get_or_404(codigo_prod)
                if action == 'increase':
                    if item['cantidad'] < product.existencias:
                        item['cantidad'] += 1
                elif action == 'decrease':
                    if item['cantidad'] > 1:
                        item['cantidad'] -= 1
                session.modified = True
                break
    update_cart_totals()
    return redirect(url_for('cliente_bp.cliente'))

@carrito_bp.route('/checkout', methods=['POST'])
def checkout():
    try:
        # Obtener los datos necesarios del carrito y del cliente (puedes obtenerlo desde la sesión)
        cart = session.get('cart', [])
        total_pedido = session.get('total_pedido', 0)
        rut_cliente = session.get('rut_cliente', None)  # Asegúrate de tener el rut del cliente

        # Crear un nuevo pedido
        nuevo_pedido = Pedido(total=total_pedido, rut_cliente=rut_cliente, estado=0)  # Ajusta los valores según tu lógica

        db.session.add(nuevo_pedido)
        db.session.commit()

        # Ahora insertar los productos del carrito en la tabla lista_producto
        for item in cart:
            codigo_producto = item['codigo_prod']
            cantidad = item['cantidad']

            nuevo_item = ListaProducto(codigo_producto=codigo_producto, cantidad=cantidad, codigo_pedido=nuevo_pedido.codigo_ped)  # Ajusta según tu modelo

            db.session.add(nuevo_item)

        db.session.commit()

        # Limpia el carrito después de confirmar el pedido
        session['cart'] = []
        session['total_pedido'] = 0
        session['subtotal_pedido'] = 0
        session['total_descuento'] = 0

        return jsonify({'message': 'Pedido confirmado exitosamente'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Error al confirmar pedido', 'error': str(e)}), 500




@carrito_bp.route('/increase_quantity/<int:codigo_prod>', methods=['POST'])
def increase_quantity(codigo_prod):
    if 'cart' in session:
        for item in session['cart']:
            if item['codigo_prod'] == codigo_prod:
                product = Producto.query.get_or_404(codigo_prod)
                if product and item['cantidad'] < product.existencias:
                    item['cantidad'] += 1
                    session.modified = True
                break
    update_cart_totals()
    return redirect(url_for('cliente_bp.cliente'))

@carrito_bp.route('/decrease_quantity/<int:codigo_prod>', methods=['POST'])
def decrease_quantity(codigo_prod):
    if 'cart' in session:
        for item in session['cart']:
            if item['codigo_prod'] == codigo_prod:
                product = Producto.query.get_or_404(codigo_prod)
                if item['cantidad'] > 1:
                    item['cantidad'] -= 1
                    session.modified = True
                break
    update_cart_totals()
    return redirect(url_for('cliente_bp.cliente'))


@carrito_bp.route('/update_cart_totals', methods=['GET'])
def update_cart_totals():
    subtotal = sum(item['precio'] * item['cantidad'] for item in session.get('cart', []))
    total_descuento = sum(item['precio'] * item['cantidad'] * item.get('descuento', 0) / 100 for item in session.get('cart', []))
    total_pedido = subtotal - total_descuento

    session['subtotal_pedido'] = subtotal
    session['total_descuento'] = total_descuento
    session['total_pedido'] = total_pedido

    return jsonify({
        'subtotal': subtotal,
        'total_descuento': total_descuento,
        'total_pedido': total_pedido
    })
