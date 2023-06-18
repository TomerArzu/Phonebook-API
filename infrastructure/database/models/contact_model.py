from infrastructure.database.db import db


class ContactModel(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)

    address = db.relationship("AddressModel", backref="contacts", lazy='dynamic')
    phone = db.relationship("PhoneModel", backref="contacts", lazy='dynamic')


