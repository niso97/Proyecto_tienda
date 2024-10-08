from flask import Blueprint, request, redirect, url_for, flash, render_template
from app import db
from app.models.categoria import Categoria
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.routes.generador import generar_codigo_categoria

categoria_bp = Blueprint('categoria_bp', __name__)

@categoria_bp.route('/categoria')
def mostrar_categoria():
    categoria = Categoria.query.all()
    return render_template('categoria.html', categoria=categoria)

@categoria_bp.route('/categoria/agregar', methods=['POST'])
def agregar_categoria():
    nombre_categoria = request.form['nombre_categoria']
    descuento = "0"  # Fijar descuento a 0

    if Categoria.query.filter_by(nombre=nombre_categoria).first():
        flash('La categoría ya existe.')
        return redirect(url_for('categoria_bp.mostrar_categoria'))
    
    codigo_cat = generar_codigo_categoria()
    nueva_categoria = Categoria(codigo_cat=codigo_cat, nombre=nombre_categoria, descuento=descuento)
    
    try:
        db.session.add(nueva_categoria)
        db.session.commit()
        flash('Categoría agregada con éxito.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al agregar la categoría.')
    
    return redirect(url_for('categoria_bp.mostrar_categoria'))

@categoria_bp.route('/categoria/modificar', methods=['POST'])
def modificar_categoria():
    codigo_cat = request.form.get('codigo_cat')
    nuevo_nombre_categoria = request.form['nuevo_nombre_categoria']
    descuento = "0"  # Fijar descuento a 0

    categoria = Categoria.query.get(codigo_cat)
    if categoria:
        categoria.nombre = nuevo_nombre_categoria
        categoria.descuento = descuento
        try:
            db.session.commit()
            flash('Categoría actualizada con éxito.')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error al actualizar la categoría.')
    else:
        flash('Categoría no encontrada.')
    
    return redirect(url_for('categoria_bp.mostrar_categoria'))

@categoria_bp.route('/categoria/eliminar/<codigo_cat>', methods=['POST'])
def eliminar_categoria(codigo_cat):
    categoria = Categoria.query.get_or_404(codigo_cat)
    
    try:
        db.session.delete(categoria)
        db.session.commit()
        flash('Categoría eliminada con éxito.')
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar categoría en uso.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al eliminar la categoría.')
    
    return redirect(url_for('categoria_bp.mostrar_categoria'))
