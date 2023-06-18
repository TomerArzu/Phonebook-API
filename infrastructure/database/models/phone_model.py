from infrastructure.database import db


class PhoneModel(db.Model):
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), nullable=False)
    number = db.Column(db.String(13), nullable=False)

    contact_id = db.Column(db.Integer, db.ForeignKey('Contacts.id'), nullable=False)

    contact = db.relationship('ContactModel', backref="phones")
