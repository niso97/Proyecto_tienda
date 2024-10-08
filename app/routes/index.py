from flask import Blueprint, render_template
from ..models.producto import db, Producto
from ..models.marca import db,  Marca
from sqlalchemy.orm.exc import NoResultFound
index_bp = Blueprint('index_bp', __name__)

@index_bp.route('/')
def index():
    products = Producto.query.all()
    return render_template('index.html', products=products)