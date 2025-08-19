from flask import Flask, render_template, request, url_for , jsonify, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
import itertools
from collections.abc import MutableMapping
import json
import pandas as pd
from datetime import datetime
import unidecode
from pretty_html_table import build_table

# Definiendo entorno bajo el cual trabajaremos
entorno = "development"

if entorno == "production":
  current_dir = os.getcwd()
  template_dir = os.path.join(current_dir,'templates')
  static_dir = os.path.join(current_dir,'static')
elif entorno == "development":
  current_dir = os.getcwd()
  template_dir = os.path.join(current_dir,'cobranzas','templates')
  static_dir = os.path.join(current_dir,'cobranzas','static')

app = Flask(__name__, template_folder=template_dir , static_folder=static_dir)
#app = Flask(__name__, template_folder='../cobranzas/templates' ,static_folder='../cobranzas/static')
# en esta ruta de template_folder y static folder en producción da error si no le pones con los dos puntos
# mientras que en desarrollo local da error si le pones ambos puntos delante
# esto debe ser posiblemente debido a que las rutas son distintas en windows y linux

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rufo2324@161.35.184.122:5432/lydemar_peruvian_delimar'
app.config['SECRET_KEY'] = 'your_unique_secret_key'
db = SQLAlchemy(app)

# DEFINING CLASS (MODEL DATABASE)
class Ventas_mayorista(db.Model):
  __tablename__ = 'ventas_mayorista'

  id = db.Column(db.Integer, primary_key=True)
  fecha = db.Column(db.Date)
  cliente = db.Column(db.String(255))
  tipo_de_documento = db.Column(db.String(255))
  numero_documento = db.Column(db.String(255))
  producto = db.Column(db.String(255))
  cantidad = db.Column(db.Integer)
  tipo_medida = db.Column(db.String(255))
  precio_unitario = db.Column(db.Float)
  precio_total = db.Column(db.Float)
  timestamp = db.Column(db.DateTime)
  vendedor = db.Column(db.String(100))
  ubicacion = db.Column(db.String(100))


  def to_dict(self):
    data = {  
      'id': self.id,
      'fecha': self.fecha,
      'cliente': self.cliente,
      'tipo_de_documento': self.tipo_de_documento,
      'numero_documento': self.numero_documento,
      'producto': self.producto,
      'cantidad': self.cantidad,
      'tipo_medida': self.tipo_medida,
      'precio_unitario': self.precio_unitario,
      'precio_total': self.precio_total,
      'timestamp': self.timestamp,
      'vendedor': self.vendedor,
      'ubicacion': self.ubicacion
    }


    return data


class Products(db.Model):
  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  product_name = db.Column(db.String(255))

  def to_dict(self):
    data = {  
      'id': self.id,
      'product_name': self.product_name
    }

    
    return data


class Cobranzas(db.Model):
  __tablename__ = 'cobranzas'

  id = db.Column(db.Integer, primary_key=True)
  fecha = db.Column(db.Date)
  tipo_de_documento = db.Column(db.String(255))
  numero_documento = db.Column(db.String(255))
  medio_pago = db.Column(db.String(255))
  monto = db.Column(db.Integer)
  timestamp = db.Column(db.DateTime)

  def to_dict(self):
    data = {  
      'id': self.id,
      'fecha': self.fecha,
      'tipo_de_documento': self.tipo_de_documento,
      'numero_documento': self.numero_documento,
      'medio_pago': self.medio_pago,
      'monto': self.monto,
      'timestamp': self.timestamp
    }


    return data

class Compras(db.Model):
  __tablename__ = 'compras'

  id = db.Column(db.Integer, primary_key=True)
  fecha = db.Column(db.Date)
  proveedor = db.Column(db.String(255))
  tipo_de_documento = db.Column(db.String(255))
  numero_documento = db.Column(db.String(255))
  producto = db.Column(db.String(255))
  cantidad = db.Column(db.Integer)
  precio_unitario = db.Column(db.Float)
  precio_total = db.Column(db.Float)
  medio_pago = db.Column(db.String(255))
  timestamp = db.Column(db.DateTime)

  def to_dict(self):
    return {
      'id': self.id,
      'fecha': self.fecha,
      'proveedor': self.proveedor,
      'tipo_de_documento': self.tipo_de_documento,
      'numero_documento': self.numero_documento,
      'producto': self.producto,
      'cantidad': self.cantidad,
      'precio_unitario': self.precio_unitario,
      'precio_total': self.precio_total,
      'medio_pago': self.medio_pago,
      'timestamp': self.timestamp
    }

@app.route('/compras', methods=['GET', 'POST'])
def compras():
  if request.method == 'POST':
    fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
    proveedor = request.form['proveedor']
    tipo_de_documento = request.form['tipo_de_documento']
    numero_documento = request.form['numero_documento']
    producto = request.form['producto']
    cantidad = int(request.form['cantidad'])
    precio_unitario = float(request.form['precio_unitario'])
    medio_pago = request.form['medio_pago']
    timestamp = datetime.now()

    compra = Compras(
      fecha=fecha,
      proveedor=proveedor,
      tipo_de_documento=tipo_de_documento,
      numero_documento=numero_documento,
      producto=producto,
      cantidad=cantidad,
      precio_unitario=precio_unitario,
      precio_total=cantidad * precio_unitario,
      medio_pago=medio_pago,
      timestamp=timestamp
    )

    db.session.add(compra)
    db.session.commit()

    flash("Compra registrada correctamente", "success")
    return redirect(url_for('compras'))

  return render_template('compras.html')



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        fecha = request.form['fecha']
        cliente = request.form['cliente']
        tipo_de_documento = request.form['factura_o_nota_de_pedido']
        numero_documento = request.form['n_documento']
        vendedor = request.form['vendedor']
        ubicacion = request.form['ubicacion']

        def contar_productos_completos():
            i = 0
            while True:
                cantidad = request.form.get(f"cantidad_en_cajas_o_sacos-{i}")
                precio_unitario = request.form.get(f"precio_x_caja_o_saco-{i}")
                
                # Si ambos campos están vacíos, consideramos que no hay más productos a registrar
                if not cantidad or not precio_unitario:
                    break
                i += 1
            return i

        cantidad_productos = contar_productos_completos()
        productos = []

        for i in range(cantidad_productos):
            producto = request.form.get(f"producto-{i}")
            cantidad = request.form.get(f"cantidad_en_cajas_o_sacos-{i}")
            tipo_medida = request.form.get(f"tipo_medida-{i}")
            precio_unitario = request.form.get(f"precio_x_caja_o_saco-{i}")

            productos.append({
                'producto': producto,
                'cantidad': cantidad,
                'tipo_medida': tipo_medida,
                'precio_unitario': precio_unitario
            })

        timestamp = datetime.now()

        # Registrar múltiples productos en la base de datos
        for prod in productos:
            venta = Ventas_mayorista(
                fecha=fecha,
                cliente=cliente,
                tipo_de_documento=tipo_de_documento,
                numero_documento=numero_documento,
                producto=prod['producto'],
                cantidad=prod['cantidad'],
                tipo_medida=prod['tipo_medida'],
                precio_unitario=prod['precio_unitario'],
                precio_total=float(prod['cantidad']) * float(prod['precio_unitario']),
                timestamp=timestamp,
                vendedor=vendedor,
                ubicacion=ubicacion
            )
            db.session.add(venta)

        db.session.commit()
        return redirect(url_for('index'))
    else:
        producto = Products.query.with_entities(Products.product_name).all()
        lista_productos = list(itertools.chain(*producto))
        return render_template('index.html', producto=lista_productos)


@app.route('/cobranzas', methods=['GET', 'POST'])
def cobranzas():
  """
  Página para crear una nueva cobranza.
  """

  if request.method == 'POST':
    fecha = request.form['fecha']
    tipo_de_documento = request.form['tipo_de_documento']
    numero_documento = request.form['numero_documento']
    medio_pago = request.form['medio_pago']
    monto = request.form['monto']
    timestamp = datetime.now()

    # Creamos un nuevo registro en la base de datos
    cobranza = Cobranzas(
      fecha=fecha,
      tipo_de_documento=tipo_de_documento,
      numero_documento=numero_documento,
      medio_pago=medio_pago,
      monto=monto,
      timestamp=timestamp
    )
    db.session.add(cobranza)
    db.session.commit()
    flash(f"Cobranza registrada :D", "success")
    # Redirigimos a la página de cobranzas
    return redirect(url_for('cobranzas'))

  else:
    return render_template('cobranzas.html')


# @app.route('/dashboard', methods=['GET'])
# def dashboard():
#   connection = db.engine.connect()

#   sql = text("""
#   SELECT *
#   FROM public.master_ventas_cobranzas 
#   """) 

#   results = connection.execute(sql)

#   # Prepare data to be displayed in the template
#   data = []
#   for row in results:
#       data.append({
#           'numero_documento': row[0],
#           'cliente': row[1],
#           'fecha_venta': row[2],
#           'fecha_ultimo_pago': row[3],
#           'venta_total': row[4],
#           'cobro_total': row[5],
#           'deuda_restante': row[6]
#     })
  
#   # Close the database connection
#   connection.close()

#   # Render the template with the prepared data
#   return render_template('dashboard.html', data=data)

# Iniciar el servidor
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))

