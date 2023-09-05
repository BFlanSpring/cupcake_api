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

@app.route("/api/cupcakes/<int:id>")
def get_cupcake(id):
    cupcake_instance = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake_instance.serialize())

@app.route("/api/cupcakes/new", methods=["POST"])
def add_cupcake():
    # Get JSON data from the request
    data = request.get_json()

    print("Received JSON data:", data)  # Add this line for debugging

    # Create a new Cupcake instance
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')
    )

    # Add the new cupcake to the database
    db.session.add(new_cupcake)
    db.session.commit()

    print("Cupcake added to the database:", new_cupcake.serialize())  # Add this line for debugging

    # Return a JSON response with the newly created cupcake data
    return jsonify(cupcake={
        "id": new_cupcake.id,
        "flavor": new_cupcake.flavor,
        "size": new_cupcake.size,
        "rating": new_cupcake.rating,
        "image": new_cupcake.image
    }), 201  # 201 Created status code


@app.route("/api/cupcakes/<int:id>", methods=["PATCH"])
def update_cupcake(id):
    # Get JSON data from the request
    data = request.get_json()

    # Retrieve the cupcake from the database or return a 404 if not found
    cupcake = Cupcake.query.get_or_404(id)

    # Update the cupcake's attributes
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data.get('image', 'https://tinyurl.com/demo-cupcake')

    # Commit the changes to the database
    db.session.commit()

    # Return a JSON response with the newly updated cupcake data
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/<int:id>", methods=["DELETE"])
def delete_cupcake(id):
    # Check if the cupcake with the specified ID exists
    cupcake = Cupcake.query.get(id)

    if cupcake is None:
        # If the cupcake doesn't exist, return a 404 response
        return jsonify({"message": "Cupcake not found"}), 404

    # Delete the cupcake from the database
    db.session.delete(cupcake)
    db.session.commit()

    # Return a JSON response indicating successful deletion
    return jsonify({"message": "Deleted"})



if __name__ == "__main__":
    app.run(debug=True)
