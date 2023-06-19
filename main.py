import os

from flask import Flask
from flask_restful import Api

from dotenv import load_dotenv

from application.cached_request_response_handler import CachedRequestResponseHandler
from infrastructure.cache.redis import redis_client
from infrastructure.cache.repositories.redis_cache_repository import RedisRequestResponseCachedRepository
from infrastructure.validators import ContactSchema
from infrastructure.validators.serializers import PagerSerializer
from logger_instance import logger

from application import ContactsHandler

from infrastructure.resources import ContactsResource, ContactResource
from infrastructure.database import db
from infrastructure.database.repositories import DatabaseContactsPersistentRepository

logger.debug("initialize Phonebook app...")



# app factory
def create_app():
    # Flask app
    app = Flask(__name__)

    load_dotenv()

    app.config["API_TITLE"] = "Phonebook REST API"
    app.config["API_VERSION"] = "v1"
    app.config['JSON_SORT_KEYS'] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "postgresql://rise:ing_up@postgres:5432/contacts")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)

    database_contacts_repository = DatabaseContactsPersistentRepository(db)
    cache_request_repository = RedisRequestResponseCachedRepository(redis_client)

    cached_request_response_handler = CachedRequestResponseHandler(
        request_response_cached_repository=cache_request_repository
    )

    contacts_handler = ContactsHandler(
        database_contacts_repository=database_contacts_repository,
        contact_serializer=ContactSchema(),
        pager_serializer=PagerSerializer()
    )

    api.add_resource(
        ContactsResource,
        '/api/v1/contacts',
        resource_class_kwargs={
            'contact_handler': contacts_handler,
            'cached_requests_handler': cached_request_response_handler,
        }
    )

    api.add_resource(
        ContactResource,
        '/api/v1/contact/<string:contact_id>',
        resource_class_kwargs={
            'contact_handler': contacts_handler,
            'cached_requests_handler': cached_request_response_handler,
        }
    )

    return app


# run local
if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
