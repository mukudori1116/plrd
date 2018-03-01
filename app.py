from flask import Flask, render_template
from plrd import Connect

app = Flask(__name__)
con = Connect('test.db')


@app.route('/')
def home():
    return render_template('home.html', title="Home")


@app.route('/library')
def library():
    date_list = [
        "{year}-{month}-{day}".format(
            year=d[:4], month=d[4:6], day=d[6:]
        ) for d in con.ExpList()
    ]
    idate_list = [
        (i+1, date, d_view) for i, (date, d_view)
        in enumerate(zip(con.ExpList(), date_list))]
    return render_template(
        'library.html', title="Library", idate_list=idate_list)


@app.route('/sql')
def db():
    return render_template('sql.html', title="SQL")


@app.route('/analyzer/<date>')
def analyzer(date):
    exp = con.makeExp(date)
    alist = exp.make_alist()
    return render_template('analyzer_list.html', alist=alist.ids, date=date)


# 作業中
# @app.route('/analyzer/<date>/<id>')
# def analyzed(id):


if __name__ == '__main__':
    app.run(debug=True)
