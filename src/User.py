class User:
    def __init__(self, id, is_adversary=False) -> None:
        # TODO:
        self.id = id
        self.is_adversary = is_adversary
        self.contacts = []
