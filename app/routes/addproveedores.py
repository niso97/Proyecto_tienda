from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.proveedor import Proveedor
from app import db
from app.routes.rut import validar_rut  # Importar la función validar_rut
from app.routes.generador import generar_codigo_proveedor  # Importar la función de generación de código

addproveedores_bp = Blueprint('addproveedores_bp', __name__)

@addproveedores_bp.route('/proveedores')
def registro():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@addproveedores_bp.route('/registrar', methods=['POST'])
def addproveedores():
    if request.method == 'POST':
        rut_prov = request.form['rut_prov']
        razon_social = request.form['razon_social']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        representante = request.form['representante']

        # Validar el RUT
        if not validar_rut(rut_prov):
            flash('El RUT ingresado no es válido')
            return redirect(url_for('addproveedores_bp.registro'))
        
        # Verificar si el rut_prov ya está registrado
        proveedor = Proveedor.query.filter_by(rut_prov=rut_prov).first()
        
        if proveedor:
            flash('Este RUT ya ha sido registrado')
        else:
            # Generar el código único de proveedor
            codigo_proveedor = generar_codigo_proveedor()
            
            nuevo_proveedor = Proveedor(
                rut_prov=rut_prov,
                razon_social=razon_social,
                correo=correo,
                telefono=telefono,
                direccion=direccion,
                representante=representante,
                codigo=codigo_proveedor  # Asignar el código generado
            )
            db.session.add(nuevo_proveedor)
            db.session.commit()
            flash('Añadido Exitosamente')
        return redirect(url_for('addproveedores_bp.registro'))

@addproveedores_bp.route('/modificar/<rut_prov>')
def get_proveedor(rut_prov):
    proveedor = Proveedor.query.filter_by(rut_prov=rut_prov).first()
    return render_template('modificar_proveedor.html', proveedor=proveedor)

@addproveedores_bp.route('/actualizar/<rut_prov>', methods=['POST'])
def actualizar_proveedor(rut_prov):
    if request.method == 'POST':
        rut_prov_nuevo = request.form['rut_prov']
        razon_social = request.form['razon_social']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        representante = request.form['representante']
        
        proveedor = Proveedor.query.filter_by(rut_prov=rut_prov).first()
        if proveedor:
            # Validar el nuevo RUT
            if not validar_rut(rut_prov_nuevo):
                flash('El nuevo RUT ingresado no es válido')
                return redirect(url_for('addproveedores_bp.get_proveedor', rut_prov=rut_prov))
            
            proveedor.rut_prov = rut_prov_nuevo
            proveedor.razon_social = razon_social
            proveedor.correo = correo
            proveedor.telefono = telefono
            proveedor.direccion = direccion
            proveedor.representante = representante
            
            db.session.commit()
            flash('Proveedor actualizado correctamente')
        
        return redirect(url_for('addproveedores_bp.registro'))

@addproveedores_bp.route('/eliminar/<string:rut_prov>')
def eliminar_proveedor(rut_prov):
    proveedor = Proveedor.query.filter_by(rut_prov=rut_prov).first()
    if proveedor:
        db.session.delete(proveedor)
        db.session.commit()
        flash('Proveedor eliminado exitosamente')
    return redirect(url_for('addproveedores_bp.registro'))
