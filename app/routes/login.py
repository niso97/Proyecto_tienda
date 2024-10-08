from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from app import db
from app.models.cliente import Cliente

login_bp = Blueprint('login_bp', __name__)

@login_bp.route('/')
def iniciar():
    return render_template('index.html')

@login_bp.route('/acceso-login', methods=["GET", "POST"])
def login():
    if request.method == 'POST' and 'nombre' in request.form and 'contrasena' in request.form:
        nombre = request.form['nombre']
        contrasena = request.form['contrasena']

        if nombre == 'admin' and contrasena == 'admin123':
            session['logueado'] = True
            session['rut_clie'] = 'admin'
            return redirect(url_for('login_bp.admin'))

        cliente = Cliente.query.filter_by(nombre=nombre, contrasena=contrasena).first()

        if cliente:
            session['logueado'] = True
            session['rut_clie'] = cliente.rut_clie
            return redirect(url_for('login_bp.cliente'))
        else:
            flash('Credenciales Incorrectas')
            return redirect(url_for('login_bp.iniciar'))

    return render_template('index.html')

@login_bp.route('/admin')
def admin():
    if 'logueado' in session and session['rut_clie'] == 'admin':
        return render_template('admin.html')
    return redirect(url_for('login_bp.iniciar'))

@login_bp.route('/cliente')
def cliente():
    if 'logueado' in session and session['rut_clie'] != 'admin':
        return render_template('cliente.html')
    return redirect(url_for('login_bp.iniciar'))
