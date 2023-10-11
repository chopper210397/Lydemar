from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # return "<h1>maryterecita</h1>"
    data ={
        'titulo':'Index',
        'bienvenida':'saludos'
    }
    return render_template('index.html', data=data)

if __name__=='__main__':
    app.run(debug=True , port=5000)