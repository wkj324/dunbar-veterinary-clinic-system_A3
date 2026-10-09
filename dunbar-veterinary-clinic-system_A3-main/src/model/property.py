class Property:
    def __init__(self, name, type, owner: Client):
        self.name = name
        self.type = type
        self.owner = owner
