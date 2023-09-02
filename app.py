from flask import Flask, render_template, redirect, request, jsonify
from models import db, Cupcake, connect_db

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secrete"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WTF_CSRF_ENABLED"] = False

db.init_app(app)
connect_db(app)

@app.route("/", methods=["GET"])
def redirect_to_list():
    """Redirect to list of cupcakes"""
    return redirect("/api/cupcakes")

@app.route("/api/cupcakes", methods=["GET"])
def show_all_cupcakes():
    """Display a list of cupcakes"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)



    # cupcakes = Cupcake.query.all()
    # serialized_cupcakes = [{"id": cupcake.id, "flavor": cupcake.flavor, "size": cupcake.size, "rating": cupcake.rating, "image": cupcake.image} for cupcake in cupcakes]
    # return jsonify(cupcakes=serialized_cupcakes)

@app.route("/add-cupcake", methods=["GET","POST"])
def add_cupcake():
    if request.method == "POST":
        data = request.get_json()  # Get JSON data from the request
        new_cupcake = Cupcake(
            flavor=data['flavor'],
            size=data['size'],
            rating=data['rating'],
            image=data.get('image', 'https://tinyurl.com/demo-cupcake')
        )
        db.session.add(new_cupcake)
        db.session.commit()
        serialized_cupcake = {
            "id": new_cupcake.id,
            "flavor": new_cupcake.flavor,
            "size": new_cupcake.size,
            "rating": new_cupcake.rating,
            "image": new_cupcake.image
        }
        return (jsonify(cupcake=serialized_cupcake), 201)
    else:
       return render_template("create_cupcake.html")

if __name__ == "__main__":
    app.run(debug=True)
