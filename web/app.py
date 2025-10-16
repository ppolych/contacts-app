"""Flask app factory for a simple contacts manager.
Comments are in English as requested.
"""
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

class Person(db.Model):
    __tablename__ = "people"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(200))
    mobile = db.Column(db.String(30))

    def __repr__(self):
        return f"<Person {self.name} {self.surname}>"

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configure app from environment
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://contacts:contacts_pw@db:5432/contacts_db",
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # Ensure tables exist
    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        """Render the quick-create form and a search box."""
        return render_template("index.html")

    @app.post("/create")
    def create():
        """Create a person from form fields."""
        name = request.form.get("name", "").strip()
        surname = request.form.get("surname", "").strip()
        email = request.form.get("email", "").strip().lower()
        address = request.form.get("address", "").strip()
        mobile = request.form.get("mobile", "").strip()

        # Basic validation
        if not (name and surname and email):
            flash("Name, surname and email are required.", "error")
            return redirect(url_for("index"))

        if Person.query.filter_by(email=email).first():
            flash("Email already exists.", "error")
            return redirect(url_for("index"))

        p = Person(name=name, surname=surname, email=email, address=address, mobile=mobile)
        db.session.add(p)
        db.session.commit()
        flash("Contact created successfully.")
        return redirect(url_for("list_people"))

    @app.get("/people")
    def list_people():
        """List all people with a search form."""
        q = request.args.get("q", "").strip()
        people = Person.query
        if q:
            like = f"%{q}%"
            people = people.filter(
                db.or_(
                    Person.name.ilike(like),
                    Person.surname.ilike(like),
                    Person.email.ilike(like),
                    Person.address.ilike(like),
                    Person.mobile.ilike(like),
                )
            )
        people = people.order_by(Person.id.desc()).all()
        return render_template("list.html", people=people, q=q)

    @app.get("/healthz")
    def healthz():
        return {"status": "ok"}, 200

    return app
