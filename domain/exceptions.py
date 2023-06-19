class PhonebookException(Exception):
    def __init__(self, message, http_status_code=None):
        super().__init__(message)
        self.message = self.args[0]
        self.http_status_code = http_status_code


class ContactNotFoundException(PhonebookException):
    def __init__(self, message, http_status_code=404):
        super(ContactNotFoundException, self).__init__(message, http_status_code)


class ContactCouldNotSaveException(PhonebookException):
    def __init__(self, message, http_status_code=500):
        super(ContactCouldNotSaveException, self).__init__(message, http_status_code)
