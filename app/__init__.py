import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/juanperico'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Clave secreta para sesiones
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', '123')

    # Configuración de la carpeta de subida de imágenes
    app.config['UPLOAD_FOLDER'] = 'C:/xampp/htdocs/Tienda2/app/static/IMG/productos'
    
    # Configurar la carpeta de templates y static
    app.config['TEMPLATES_AUTO_RELOAD'] = True  # Opcional: recargar automáticamente plantillas en desarrollo
    app.template_folder = 'templates'
    app.static_folder = 'static'
    
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Inicializar la base de datos
    db.init_app(app)

    with app.app_context():
        from .models import producto  # Importa tus modelos aquí
        db.create_all()  # Crea las tablas en la base de datos

    from app.routes.carrito import carrito_bp
    app.register_blueprint(carrito_bp, url_prefix='/')

    # Importar blueprints de rutas
    from app.routes.factura import factura_bp
    app.register_blueprint(factura_bp, url_prefix='/')

    from app.routes.index import index_bp
    app.register_blueprint(index_bp)

    from app.routes.cliente import cliente_bp
    app.register_blueprint(cliente_bp)

    from app.routes.addproveedores import addproveedores_bp
    app.register_blueprint(addproveedores_bp, url_prefix='/')

    from app.routes.pedidosinv import pedidosinv_bp
    app.register_blueprint(pedidosinv_bp, url_prefix='/')

    from app.routes.login import login_bp
    app.register_blueprint(login_bp, url_prefix='/')

    from app.routes.registro import registro_bp
    app.register_blueprint(registro_bp, url_prefix='/')

    from app.routes.producto import producto_bp
    app.register_blueprint(producto_bp, url_prefix='/')
    
    from app.routes.categoria import categoria_bp
    app.register_blueprint(categoria_bp, url_prefix='/')

    from app.routes.marca import marca_bp
    app.register_blueprint(marca_bp, url_prefix='/')

    from app.routes.descuentos import descuentos_bp
    app.register_blueprint(descuentos_bp, url_prefix='/')

    from app.routes.venta import ventas_bp
    app.register_blueprint(ventas_bp, url_prefix='/')

    from app.routes.usuarios import usuarios_bp
    app.register_blueprint(usuarios_bp, url_prefif='/')
    
    return app
