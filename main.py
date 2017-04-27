from flask import Flask, request, redirect, render_template, flash, abort
app = Flask(__name__)
app.secret_key = 'myReallysecretKey'

blogs = [
    {'title': 'Blog1', 'text': 'Hello World', 'id': 1},
    {'title': 'Blog Ciccio', 'text': 'Ciao Ciao Bambolina', 'id': 2},
]


def generate_id():
    try:
        return blogs[-1]['id'] + 1
    except IndexError:
        return 1


@app.errorhandler(404)
def get_not_found(*args, **kw):
    flash('Blog Not Found!', 'danger')
    return redirect('/')


def search_blog(blogid):
    try:
        blogid = int(blogid)
    except ValueError:
        abort(404)
    
    for index, b in enumerate(blogs):
        if b['id'] == blogid:
            return index
    abort(404)


@app.route('/blog/<blogid>')
def blog(blogid):
    index = search_blog(blogid)
    return render_template('detail.html', blog=blogs[index])
    
    
@app.route('/blog/<blogid>/update', methods=['GET', 'POST'])
def update(blogid):
    index = search_blog(blogid)
    
    if request.method == 'POST':
        if not request.form['text'] or not request.form['title']:
            flash('Please, all fields are required', 'warning')
            return redirect('/blog/{}/update'.format(blogid))
        blogs[index]['title'] = request.form['title']
        blogs[index]['text'] = request.form['text']
        flash('Good job man!', 'success')
        return redirect('/blog/{}'.format(blogid))
    return render_template('create.html', mode='update', blog=blogs[index])


@app.route('/blog/<blogid>/remove', methods=['POST'])
def remove(blogid):
    index = search_blog(blogid)
    blogs.remove(blogs[index])
    flash('Blog Removed!', 'success')
    return redirect('/')


@app.route('/')
def index():
    return render_template('index.html', blogs=blogs)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        if not request.form['text'] or \
                not request.form['title']:
            flash('Please, all fields are required', 'warning')
            return redirect('/create')
        blog = {"title": request.form['title'],
                "text": request.form['text'],
                "id": generate_id()}
        blogs.append(blog)
        flash('Fuck Yeah!', 'success')
        return redirect('/')
        
    else:
        return render_template('create.html', mode='create', blog={})

if __name__ == '__main__':
    counter = 1
    app.run(debug=True, host='0.0.0.0')

