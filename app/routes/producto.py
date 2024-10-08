from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from app import db
from werkzeug.utils import secure_filename
import os
from app.models.producto import Producto
from sqlalchemy.exc import SQLAlchemyError
from app.routes.generador import generar_codigo_producto

producto_bp = Blueprint('producto_bp', __name__)

@producto_bp.route('/producto')
def mostrar_producto():
    try:
        productos = Producto.query.all()
        return render_template('producto.html', productos=productos)
    except SQLAlchemyError as e:
        error_msg = "Error al obtener los productos de la base de datos."
        flash(error_msg, 'error')
        return redirect(url_for('index_bp.mostrar_index'))

@producto_bp.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        try:
            nombre_producto = request.form['nombre_producto']
            precio = request.form['precio']
            marca = request.form['marca']
            codigo_categoria = request.form['codigo_categoria']

            if 'imagen' in request.files:
                imagen = request.files['imagen']
                if imagen.filename != '':
                    imagen_nombre = secure_filename(imagen.filename)
                    imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], imagen_nombre)
                    imagen.save(imagen_path)
                else:
                    flash('Debe seleccionar una imagen válida.', 'error')
                    return redirect(url_for('producto_bp.mostrar_producto'))
            else:
                flash('No se recibió ninguna imagen.', 'error')
                return redirect(url_for('producto_bp.mostrar_producto'))

            producto_existente = Producto.query.filter_by(nombre=nombre_producto).first()
            if producto_existente:
                flash('Ya existe un producto con este nombre.', 'error')
                return redirect(url_for('producto_bp.mostrar_producto'))

            # Generar código único para el producto
            codigo_prod = generar_codigo_producto()

            nuevo_producto = Producto(
                codigo_prod=codigo_prod,  # Asignar el código generado
                precio=precio,
                marca=marca,
                descuento='0',  # Asegurar que descuento inicie en '0'
                nombre=nombre_producto,
                categoria=codigo_categoria,
                imagen=imagen_nombre,
                existencias=0  # Asegurar que existencias inicie en 0
            )
            
            db.session.add(nuevo_producto)
            db.session.commit()

            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('producto_bp.mostrar_producto'))

        except SQLAlchemyError as e:
            flash('Error al agregar el producto.', 'error')
            return redirect(url_for('producto_bp.mostrar_producto'))

@producto_bp.route('/eliminar_producto/<int:codigo_prod>', methods=['POST'])
def eliminar_producto(codigo_prod):
    try:
        producto = Producto.query.get(codigo_prod)
        db.session.delete(producto)
        db.session.commit()

        flash('Producto eliminado correctamente.', 'success')
        return redirect(url_for('producto_bp.mostrar_producto'))

    except SQLAlchemyError as e:
        flash('Error al eliminar el producto.', 'error')
        return redirect(url_for('producto_bp.mostrar_producto'))

@producto_bp.route('/modificar_producto', methods=['POST'])
def modificar_producto():
    if request.method == 'POST':
        try:
            codigo_prod = request.form['codigo_prod']
            producto = Producto.query.get(codigo_prod)

            if not producto:
                flash('Producto no encontrado.', 'error')
                return redirect(url_for('producto_bp.mostrar_producto'))

            nombre_producto = request.form.get('nombre_producto_mod')
            precio = request.form.get('precio_mod')
            marca = request.form.get('marca_mod')
            codigo_categoria = request.form.get('codigo_categoria_mod')
            imagen = request.files.get('imagen_mod')

            if nombre_producto:
                producto.nombre = nombre_producto
            if precio:
                producto.precio = precio
            if marca:
                producto.marca = marca
            if codigo_categoria:
                producto.categoria = codigo_categoria
            if imagen and imagen.filename != '':
                imagen_nombre = secure_filename(imagen.filename)
                imagen_path = os.path.join(current_app.config['UPLOAD_FOLDER'], imagen_nombre)
                imagen.save(imagen_path)
                producto.imagen = imagen_nombre

            db.session.commit()

            flash('Producto modificado correctamente.', 'success')
            return redirect(url_for('producto_bp.mostrar_producto'))

        except SQLAlchemyError as e:
            flash('Error al modificar el producto.', 'error')
            return redirect(url_for('producto_bp.mostrar_producto'))
