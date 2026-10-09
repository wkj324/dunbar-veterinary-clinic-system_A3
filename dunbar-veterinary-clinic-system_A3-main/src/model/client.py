class Client:
    def __init__(self, name, contact_number, email=None, client_type="normal"):
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.client_type = client_type
        self.is_active = True

    def deactivate(self):
        self.is_active = False
