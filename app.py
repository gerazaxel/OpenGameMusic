from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Z:/OpenGameMusic/OpenGameMusic.db'

db = SQLAlchemy(app)

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tags = db.Column(db.String(200))
    file_path = db.Column(db.String(200), nullable=False)

@app.route('/')
def index():
    tracks = Track.query.all()
    return render_template('index.html', tracks=tracks)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        title = request.form['music-title']
        tags = request.form['tags']
        file = request.files['music-file']
        # Сохраните файл и добавьте запись в базу данных
        track = Track(title=title, tags=tags, file_path=file.filename)
        db.session.add(track)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
