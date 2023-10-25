from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from collections.abc import MutableMapping

current_dir = os.getcwd()
template_dir = os.path.join(current_dir, 'cobranzas','templates')
static_dir = os.path.join(current_dir, 'cobranzas','static')

app = Flask(__name__, template_folder=template_dir , static_folder=static_dir)
#app = Flask(__name__, template_folder='../cobranzas/templates' ,static_folder='../cobranzas/static')
# en esta ruta de template_folder y static folder en producción da error si no le pones con los dos puntos
# mientras que en desarrollo local da error si le pones ambos puntos delante
# esto debe ser posiblemente debido a que las rutas son distintas en windows y linux

# Rutas
@app.route('/')
def index():
  return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
  fecha = request.form['fecha']
  nombre_cliente = request.form['nombre_cliente']
  factura_o_nota_de_pedido = request.form['factura_o_nota_de_pedido']
  n_documento = request.form['n_documento']
  producto = request.form['producto']
  cantidad_en_cajas_o_sacos = request.form['cantidad_en_cajas_o_sacos']
  precio_x_caja_o_saco = request.form['precio_x_caja_o_saco']
  totales_en_soles = request.form['totales_en_soles']
  pago_a_cuenta_efectivo_yape_transferencia = request.form['pago_a_cuenta_efectivo_yape_transferencia']
  debe = request.form['debe']
  return render_template('submitted.html',
                          fecha=fecha, 
                          nombre_cliente=nombre_cliente, 
                          factura_o_nota_de_pedido=factura_o_nota_de_pedido, 
                          n_documento=n_documento, 
                          producto=producto, 
                          cantidad_en_cajas_o_sacos=cantidad_en_cajas_o_sacos, 
                          precio_x_caja_o_saco=precio_x_caja_o_saco, 
                          totales_en_soles=totales_en_soles, 
                          pago_a_cuenta_efectivo_yape_transferencia=pago_a_cuenta_efectivo_yape_transferencia, 
                          debe=debe)


# Iniciar el servidor
if __name__ == '__main__':
  app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))
