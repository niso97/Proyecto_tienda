from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.cliente import Cliente

usuarios_bp = Blueprint('usuarios_bp', __name__)

@usuarios_bp.route('/usuarios')
def mostrar_usuarios():
     usuarios = Cliente.query.all()
     return render_template('usuarios.html', usuarios=usuarios)