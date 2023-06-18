import os

from flask import Flask
from flask_restful import Api
from logger_instance import logger

from application import ContactsHandler

from infrastructure.resources import ContactsResource, ContactResource
from infrastructure.database import DatabaseContactsRepository, db


logger.debug("initialize Phonebook app...")
# Flask app
app = Flask(__name__)


# app factory
def create_app():
    app.config["API_TITLE"] = "Phonebook REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # app.config[
    #     "OPENAPI_SWAGGER_UI_URL"
    # ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    database_contacts_repository = DatabaseContactsRepository(db)

    contacts_handler = ContactsHandler(
        database_contacts_repository=database_contacts_repository,
    )

    api.add_resource(
        ContactsResource,
        '/api/v1/contacts',
        resource_class_kwargs={
            'handler': contacts_handler,
        }
    )

    api.add_resource(
        ContactResource,
        '/api/v1/contact/<string:contact_id>',
        resource_class_kwargs={
            'handler': contacts_handler,
        }
    )

    return app


# run local
if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
