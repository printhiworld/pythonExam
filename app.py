from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
app = Flask("app")
app.config.from_pyfile("default_config.py")
app.config.from_envvar("APP_SETTINGS", silent=True)


db = SQLAlchemy(app)


class Note(db.Model):
    """
    модель записи
    id = формируется автоматически
    name = строка
    date = строка
    wish = строка
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    date = db.Column(db.String(1000))
    wish = db.Column(db.String(1000))


with app.app_context():
    db.create_all()


@app.route("/")
def get():
    """
    :return: возвращает все записи
    """
    notes = Note.query.all()
    response = {
        "friends": [{"name": note.name,
                   "date": note.date,
                   "wish": note.wish,} for note in notes],
    }
    return jsonify(response)


@app.route("/post", methods=["POST"])
def post():
    """
    проверяет наличие необходимых полей и существование в базе, в случае нехватки данных возвращает ошибку
    :return: возвращает созданную запись
    """
    note_data = request.json
    if not note_data or "name" not in note_data or "date" not in note_data or "wish" not in note_data:
        return jsonify({"error": "invalid_request"}), 400

    try:
        note = Note(
            name=note_data["name"],
            date=note_data["date"],
            wish=note_data["wish"],
        )
        db.session.add(note)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "already_exists"}), 400

    return jsonify([{"name": note.name,
                   "date": note.date,
                   "wish": note.wish,}]), 200


@app.route("/put/<int:pk>", methods=["PUT"])
def put(pk):
    """
    принимает первичный ключ из запроса, проверяет наличие всех подей, в случае нехватки данных возвращает ошибку
    :param pk: int
    :return: возвращает отредактированную запись
    """
    note_data = request.json
    note = Note.query.get(pk)
    if not note_data or "name" not in note_data or "date" not in note_data or "wish" not in note_data:
        return jsonify({"error": "invalid_request"}), 400

    try:
        note.name = note_data.get("name")
        note.date = note_data.get("date")
        note.wish = note_data.get("wish")
        db.session.add(note)
        db.session.commit()
    except IntegrityError:
        return jsonify({"error": "already_exists"}), 400

    return jsonify([{"name": note.name,
                   "date": note.date,
                   "wish": note.wish,}]), 200


@app.route("/delete/<int:pk>", methods=["DELETE"])
def delete(pk):
    """
    принимает первичный ключ из запроса и удаляет запись
    :param pk: int
    :return: text "deleted"
    """
    note = Note.query.get(pk)

    db.session.delete(note)
    db.session.commit()
    return jsonify("deleted"), 200


if __name__ == "__main__":
    app.run(debug=True)
