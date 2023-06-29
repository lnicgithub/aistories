from flask import Flask, render_template
from articles_data import Articles 

Articles = Articles()

app = Flask(__name__)
debug = True
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/articles')
def articles():
    
    return render_template('articles.html', articles = Articles)

if __name__ == '__main__':
    app.run(debug=debug)
