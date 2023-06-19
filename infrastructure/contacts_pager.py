from math import ceil

from sqlalchemy.orm import subqueryload

from infrastructure.database.models import ContactModel, PhoneModel, AddressModel


class ContactsPager:
    def __init__(self, data_model, page=1, items_per_page=10, first_name_filter=None):
        self._data_model = data_model
        self.page = page
        self.items_per_page = items_per_page
        self.first_name_filter = first_name_filter

    def total_items(self):
        if self.first_name_filter:
            return self._data_model.query.filter(ContactModel.first_name.ilike(self.first_name_filter+'%')).count()
        return self._data_model.query.count()

    def total_pages(self):
        return ceil(self.total_items() / self.items_per_page)

    def next_page_index(self):
        return self.page + 1 if self.page + 1 <= self.total_pages() else None

    def previous_page_index(self):
        return self.page - 1 if self.page - 1 > 0 else None

    def current_page_index(self):
        return self.page

    def get_page_items(self):
        offset = (self.page - 1) * self.items_per_page
        if self.first_name_filter:
            sub_query = ContactModel.query.filter(ContactModel.first_name.ilike(self.first_name_filter+'%')).order_by(ContactModel.id).offset(offset).limit(self.items_per_page).subquery()
        else:
            sub_query = ContactModel.query.order_by(ContactModel.id).offset(offset).limit(self.items_per_page).subquery()
        query = ContactModel.query.join(sub_query, ContactModel.id == sub_query.c.id).join(PhoneModel,
                                                                                           ContactModel.id == PhoneModel.contact_id).join(
            AddressModel, ContactModel.id == AddressModel.contact_id)
        contacts = query.all()
        return contacts
