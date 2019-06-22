import sqlite3
from flask import Flask, g, jsonify, render_template, abort
import time

DATABASE = "names.db"
LIMIT = 1000

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
        db.enable_load_extension(True)
        db.load_extension('./levenshtein')
        db.enable_load_extension(False)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/name/<name>', methods=['GET'])
def name(name):
    c = get_db().cursor()

    if "-" in name:
        sex = name[-1]
        name = name[:-2]
        c.execute("""SELECT rowid, * FROM names
                     WHERE name == ? AND sex == ?
                     COLLATE NOCASE""", (name, sex,))
    else:
        c.execute("""SELECT rowid, * FROM names
                     WHERE name == ?
                     COLLATE NOCASE""", (name, ))

    found = c.fetchone()

    if found:
        rowid = found["rowid"]
        page = (rowid // LIMIT) + 1
        offset = rowid % LIMIT

        c.execute("""SELECT * FROM names
                     WHERE LEVENSHTEIN(name, :name) <= 2 AND rowid != :rowid
                     ORDER BY LEVENSHTEIN(name, :name) ASC,
                              qty DESC""", {"name": name, "rowid": rowid})
        similar_names = c.fetchall()
        result = {
            "name": found["name"],
            "sex": found["sex"],
            "page": page,
            "offset": offset,
            "similar_names": similar_names
        }
        return jsonify(result)
    else:
        abort(404)

@app.route('/api/names/<int:page>', methods=['GET'])
def names(page):
    c = get_db().cursor()

    c.execute("""SELECT count(*) FROM names""")
    total = c.fetchone()["count(*)"]
    pages = total / LIMIT

    page = page - 1
    c.execute("""SELECT rowid, * FROM names
                 WHERE rowid >= ? AND rowid <= ?
                 ORDER BY rowid ASC""", ((page * LIMIT) + 1, ((page + 1) * LIMIT)))
    names = c.fetchall()

    return jsonify(names)

@app.route('/', defaults={'page': '1'})
@app.route('/<page>')
def page_page(page):
    return render_template('nomes_js.html')

if __name__ == '__main__':
    app.run(debug=True)
