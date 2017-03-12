from flask import Flask, render_template, abort

app = Flask(__name__)

PRODUCTS = {
    'iphone': {
        'name': 'iPhone 5S',
        'category': 'Phones',
        'price': 699,
    },
    'galaxy': {
        'name': 'Samsung Galaxy 5',
        'category': 'Phones',
        'price': 649,
    },
    'ipad-air': {
        'name': 'iPad Air',
        'category': 'Tablets',
        'price': 649,
    },
    'ipad-mini': {
        'name': 'iPad Mini',
        'category': 'Tablets',
        'price': 549
    }
}

@app.route('/')
def default():
    return render_template('home.html', products=PRODUCTS)

@app.route('/home')
def home():
    return render_template('home.html', products=PRODUCTS)

@app.route('/product/<key>')
def product(key):
    product = PRODUCTS.get(key)
    if not product:
        abort(404)
    return render_template('product.html', product=product)

@app.route('/teams')
def teams():
    return render_template('teams.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/searchteam')
def searchteam():
    return render_template('searchteam.html')

@app.route('/searchproject')
def searchproject():
    return render_template('searchproject.html')

if __name__ == "__main__":
    app.run(debug=True)