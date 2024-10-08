from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.producto import Producto

descuentos_bp = Blueprint('descuentos_bp', __name__)

@descuentos_bp.route('/descuentos')
def descuentos():
    productos = Producto.query.all()
    return render_template('descuentos.html', productos=productos)

@descuentos_bp.route('/update_discount', methods=['POST'])
def update_discount():
    data = request.get_json()
    product_code = data['product_code']
    discount = f"{data['discount']}"  # Añade el símbolo % al descuento

    product = Producto.query.filter_by(codigo_prod=product_code).first()
    if product:
        product.descuento = discount
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Producto no encontrado'})