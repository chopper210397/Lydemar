from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
  name = "Juan Pérez"
  return render_template('C:\Users\chopper\Documents\Lydemar\cobranzas\index.html', name=name)

if __name__ == "__main__":
  app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))