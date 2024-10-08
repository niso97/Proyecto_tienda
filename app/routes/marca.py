from flask import Blueprint, request, redirect, url_for, flash, render_template
from app import db
from app.models.marca import Marca
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from app.routes.generador import generar_codigo_marca

marca_bp = Blueprint('marca_bp', __name__)

@marca_bp.route('/marca')
def mostrar_marcas():
    marcas = Marca.query.all()
    return render_template('marca.html', marcas=marcas)

@marca_bp.route('/marca/agregar', methods=['POST'])
def agregar_marca():
    nombre_marca = request.form['nombre_marca']
    descuento = "0"  # Fijar descuento a 0

    if Marca.query.filter_by(nombre=nombre_marca).first():
        flash('La marca ya existe.')
        return redirect(url_for('marca_bp.mostrar_marcas'))
    
    codigo_marca = generar_codigo_marca()
    nueva_marca = Marca(codigo=codigo_marca, nombre=nombre_marca, descuento=descuento)
    
    try:
        db.session.add(nueva_marca)
        db.session.commit()
        flash('Marca agregada con éxito.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al agregar la marca.')
    
    return redirect(url_for('marca_bp.mostrar_marcas'))

@marca_bp.route('/marca/modificar', methods=['POST'])
def modificar_marca():
    codigo_marca = request.form.get('codigo_marca')
    nuevo_nombre_marca = request.form['nuevo_nombre_marca']
    descuento = "0"  # Fijar descuento a 0

    marca = Marca.query.get(codigo_marca)
    if marca:
        marca.nombre = nuevo_nombre_marca
        marca.descuento = descuento
        try:
            db.session.commit()
            flash('Marca actualizada con éxito.')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('Error al actualizar la marca.')
    else:
        flash('Marca no encontrada.')
    
    return redirect(url_for('marca_bp.mostrar_marcas'))

@marca_bp.route('/marca/eliminar/<codigo_marca>', methods=['POST'])
def eliminar_marca(codigo_marca):
    marca = Marca.query.get_or_404(codigo_marca)
    
    try:
        db.session.delete(marca)
        db.session.commit()
        flash('Marca eliminada con éxito.')
    except IntegrityError:
        db.session.rollback()
        flash('No se puede eliminar marca en uso.')
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al eliminar la marca.')
    
    return redirect(url_for('marca_bp.mostrar_marcas'))
