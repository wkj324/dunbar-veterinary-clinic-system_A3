class Client:
    _id_counter = 1
    def __init__(self, name, phone, email):
        self.id = Client._id_counter
        Client._id_counter += 1
        self.name = name
        self.phone = phone
        self.email = email
