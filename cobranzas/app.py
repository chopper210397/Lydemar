from flask import Flask, render_template, request, url_for , jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from collections.abc import MutableMapping
import json
import pandas as pd
from datetime import datetime
import unidecode
from pretty_html_table import build_table

# for production environment
current_dir = os.getcwd()
template_dir = os.path.join(current_dir,'templates')
static_dir = os.path.join(current_dir,'static')

# for development environment
# current_dir = os.getcwd()
# template_dir = os.path.join(current_dir,'cobranzas','templates')
# static_dir = os.path.join(current_dir,'cobranzas','static')

app = Flask(__name__, template_folder=template_dir , static_folder=static_dir)
#app = Flask(__name__, template_folder='../cobranzas/templates' ,static_folder='../cobranzas/static')
# en esta ruta de template_folder y static folder en producción da error si no le pones con los dos puntos
# mientras que en desarrollo local da error si le pones ambos puntos delante
# esto debe ser posiblemente debido a que las rutas son distintas en windows y linux

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rufo2324@161.35.184.122:5432/lydemar_peruvian_delimar'
db = SQLAlchemy(app)

# class Ventas_tienda_productores(db.Model):
#   __tablename__ = 'ventas_tienda_productores'

#   id = db.Column(db.Integer, primary_key=True)
#   fecha = db.Column(db.Date)
#   producto = db.Column(db.String(255))
#   cantidad = db.Column(db.Integer)
#   medida = db.Column(db.String(255))
#   precio_unitario = db.Column(db.Float)
#   precio_total = db.Column(db.Float)
#   cliente = db.Column(db.String(255))
#   timestamp = db.Column(db.DateTime)

#   def to_dict(self):
#     data = {  
#       'id': self.id,
#       'fecha': self.fecha,
#       'producto': self.producto,
#       'cantidad': self.cantidad,
#       'medida': self.medida,
#       'precio_unitario': self.precio_unitario,
#       'precio_total': self.precio_total,
#       'cliente': unidecode.unidecode(self.cliente)
#     }

#     # Convertir el timestamp a un formato JSON compatible
#     data['timestamp'] = self.timestamp.strftime('%Y-%m-%dT%H:%M:%S')

#     return data

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
      'timestamp': self.timestamp
    }


    return data



# Rutas
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  fecha = request.form['fecha']
  cliente = request.form['cliente']
  tipo_de_documento = request.form['factura_o_nota_de_pedido']
  numero_documento = request.form['n_documento']
  producto = request.form['producto']
  cantidad = request.form['cantidad_en_cajas_o_sacos']
  tipo_medida = request.form['tipo_medida']
  precio_unitario = request.form['precio_x_caja_o_saco']
  precio_total = request.form['totales_en_soles']
  timestamp = datetime.now()

  # Creamos un nuevo registro en la base de datos
  venta = Ventas_mayorista(
                fecha=fecha, 
                cliente=cliente,
                tipo_de_documento=tipo_de_documento,
                numero_documento=numero_documento,
                producto=producto,
                cantidad=cantidad,
                tipo_medida=tipo_medida,
                precio_unitario=precio_unitario,
                precio_total=precio_total,
                timestamp=timestamp
                )
  db.session.add(venta)
  db.session.commit()
  
  return render_template('submitted.html',
                          fecha=fecha, 
                          cliente=cliente,
                          tipo_de_documento=tipo_de_documento,
                          numero_documento=numero_documento,
                          producto=producto,
                          cantidad=cantidad,
                          tipo_medida=tipo_medida,
                          precio_unitario=precio_unitario,
                          precio_total=precio_total
                          )


@app.route('/ventas', methods=['GET'])
def raa():
  ventas = Ventas_mayorista.query.all()
  return render_template('ventas.html', ventas=ventas)

# Iniciar el servidor
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))

# @app.route('/read-data', methods=['GET'])
# def read_data():
#   # Obtener todos los registros
#   ventas = Ventas_mayorista.query.all()

#   # Convertir los registros a un formato JSON
#   ventas_json = []
#   for venta in ventas:
#     try:
#       ventas_json.append(venta.to_dict())
#     except Exception as e:
#       print(e)

#   # Crear un DataFrame de pandas a partir de los datos JSON
#   df = pd.DataFrame(ventas_json)

#   # Generar el código HTML de la tabla
#   html_table_blue_light = build_table(df, 'blue_light')

#   # Devolver los resultados
#   return html_table_blue_light

#   # Devolver los resultados
#   #return jsonify(ventas_json)

