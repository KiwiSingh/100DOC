from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    def to_dict(self):
        #Method 1. 
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns: # type: ignore
            #Create a new dictionary entry;
            # where the key is the name of the column
            # and the value is the value of the column
            dictionary[column.name] = getattr(self, column.name)
        return dictionary



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random") #type: ignore
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all") # type:ignore
def get_all_cafes():
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")  # type: ignore
def search_cafes():
    query_location = request.args.get("loc")
    query_name = request.args.get("name")

    if query_location:
        result = db.session.execute(
            db.select(Cafe).where(Cafe.location.ilike(f"%{query_location}%")))

    elif query_name:
        result = db.session.execute(
            db.select(Cafe).where(Cafe.name.ilike(f"%{query_name}%")))

    else:
        return jsonify(
            error={"Bad Request": "Please provide either 'loc' or 'name'."}), 400

    all_cafes = result.scalars().all()

    if all_cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

    return jsonify(error={"Not Found": "Sorry partner, ain't nothin' but us chickens here!"}), 404


    

# HTTP GET - Read Record

# HTTP POST - Create Record
@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"), #type:ignore
        map_url=request.form.get("map_url"), #type:ignore
        img_url=request.form.get("img_url"), #type:ignore
        location=request.form.get("loc"),#type:ignore
        has_sockets=bool(request.form.get("sockets")),#type:ignore
        has_toilet=bool(request.form.get("toilet")),#type:ignore
        has_wifi=bool(request.form.get("wifi")),#type:ignore
        can_take_calls=bool(request.form.get("calls")),#type:ignore
        seats=request.form.get("seats"),#type:ignore
        coffee_price=request.form.get("coffee_price"),#type:ignore
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})

# HTTP PUT/PATCH - Update Record
@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    try:
        cafe = db.session.get(Cafe, cafe_id)
    except AttributeError:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        cafe.coffee_price = new_price # type: ignore
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200

# HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api-key")
    if api_key == "ch1ka_fuj1wara":
        try:
            cafe = db.session.get(Cafe, cafe_id)
        except AttributeError:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
        else:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403

if __name__ == '__main__': #type:ignore
    app.run(debug=True)
