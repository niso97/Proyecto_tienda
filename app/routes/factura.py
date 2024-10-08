from flask import Blueprint, request, redirect, url_for, flash, render_template
from app import db
from app.models.proveedor import Proveedor
from app.models.lista_factura import ListaFactura
from app.models.factura import Factura
from app.models.producto import Producto
from app.models.lista_proveedores import ListaProveedores
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.routes.rut import validar_rut

factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/factura')
def mostrar_factura():
    factura = Factura.query.all()
    return render_template('factura.html', factura=factura)

@factura_bp.route('/agregar_factura', methods=['POST'])
def agregar_factura():
    rut_proveedor = request.form.get('rut_proveedor')
    fecha_emision = request.form.get('fecha_emision')
    codigo_productos = request.form.getlist('codigo_producto[]')
    cantidad_productos = request.form.getlist('cantidad_producto[]')
    costo_productos = request.form.getlist('costo_producto[]')
    fecha_vencimientos = request.form.getlist('fecha_vencimiento[]')

    try:
        # Paso 1: Validar RUT del proveedor y verificar existencia en la tabla de proveedores
        rut_valido = validar_rut(rut_proveedor)
        if not rut_valido:
            flash('Rut del proveedor inválido')
            return redirect(url_for('factura_bp.mostrar_factura'))

        proveedor = Proveedor.query.filter_by(rut_prov=rut_proveedor).first()
        if not proveedor:
            flash('Rut del proveedor no encontrado en la base de datos')
            return redirect(url_for('factura_bp.mostrar_factura'))

        # Paso 2: Validar y verificar existencia de códigos de productos
        productos = []
        for codigo_prod in codigo_productos:
            if not codigo_prod.isdigit():
                flash(f'Código de producto {codigo_prod} inválido')
                return redirect(url_for('factura_bp.mostrar_factura'))

            producto = Producto.query.filter_by(codigo_prod=int(codigo_prod)).first()
            if not producto:
                flash(f'Producto con código {codigo_prod} no encontrado')
                return redirect(url_for('factura_bp.mostrar_factura'))
            productos.append(producto)

        # Validar datos numéricos y fechas
        for cantidad, costo, vencimiento in zip(cantidad_productos, costo_productos, fecha_vencimientos):
            if not cantidad.isdigit():
                flash(f'Cantidad {cantidad} inválida')
                return redirect(url_for('factura_bp.mostrar_factura'))
            if not costo.replace('.', '', 1).isdigit():
                flash(f'Costo {costo} inválido')
                return redirect(url_for('factura_bp.mostrar_factura'))
            try:
                datetime.strptime(vencimiento, '%Y-%m-%d')
            except ValueError:
                flash(f'Fecha de vencimiento {vencimiento} inválida')
                return redirect(url_for('factura_bp.mostrar_factura'))

        # Validar fecha de emisión
        try:
            fecha_emision_dt = datetime.strptime(fecha_emision, '%Y-%m-%d')
        except ValueError:
            flash('Fecha de emisión inválida')
            return redirect(url_for('factura_bp.mostrar_factura'))

        # Paso 3: Insertar datos en la tabla factura
        total_pago = sum(float(costo) * int(cantidad) for costo, cantidad in zip(costo_productos, cantidad_productos))
        subtotal = total_pago / 1.19
        impuestos_aplicables = '19'

        nueva_factura = Factura(
            total_pago=str(total_pago),
            fecha_emision=fecha_emision_dt,
            subtotal=str(subtotal),
            impuestos_aplicables=impuestos_aplicables,
            rut_proveedor=rut_proveedor
        )
        db.session.add(nueva_factura)
        db.session.commit()

        # Paso 4: Insertar datos en la tabla lista_factura y actualizar existencias
        for codigo_prod, cantidad, costo, vencimiento in zip(codigo_productos, cantidad_productos, costo_productos, fecha_vencimientos):
            nueva_lista_factura = ListaFactura(
                cantidad_producto=cantidad,
                costo=costo,
                id_factura=nueva_factura.id_fact,
                codigo_producto=int(codigo_prod),
                vencimiento=datetime.strptime(vencimiento, '%Y-%m-%d')
            )
            db.session.add(nueva_lista_factura)

            # Actualizar existencias del producto
            producto = Producto.query.filter_by(codigo_prod=int(codigo_prod)).first()
            producto.existencias += int(cantidad)

        db.session.commit()

        # Paso 5: Insertar datos en la tabla lista_proveedores
        for codigo_prod in codigo_productos:
            nueva_lista_proveedores = ListaProveedores(
                codigo_prod=int(codigo_prod),
                codigo_proveedor=rut_proveedor
            )
            db.session.add(nueva_lista_proveedores)

        db.session.commit()

        flash('Factura registrada exitosamente')
        return redirect(url_for('factura_bp.mostrar_factura'))

    except SQLAlchemyError as e:
        db.session.rollback()
        flash('Error al registrar la factura: ' + str(e))
        return redirect(url_for('factura_bp.mostrar_factura'))
