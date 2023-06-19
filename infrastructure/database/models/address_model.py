from infrastructure.database.db import db


class AddressModel(db.Model):
    __tablename__ = 'addresses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    street = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(25), nullable=False)

    contact_id = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=False)

    contact = db.relationship('ContactModel', back_populates="address")
