from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '123456789011', 'price': 500},
        {'id': 2, 'name': 'Xbox', 'barcode': '121314151617', 'price': 900},
        {'id': 3, 'name': 'Camera', 'barcode': '181920212223', 'price': 220}
    ]
    return render_template('market.html', title='Market', items=items)

if __name__ == '__main__':
    app.run(debug=True)
