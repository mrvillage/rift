import json

from discord.ext.commands import BadInviteArgument


class Document:
    __slots__ = (
        "data",
        "id",
        "name",
        "url",
        "categories",
        "keywords",
        "description",
        "search_args",
    )

    def __init__(self, *, data=None):
        self.data = data
        self.id = self.data[0]
        self.name = self.data[1]
        self.url = self.data[2]
        self.categories = json.loads(self.data[3])
        self.keywords = json.loads(self.data[4])
        self.description = self.data[5]
        self.search_args = self.categories + self.keywords
        self.search_args.append(self.name)
        self.search_args = [i.lower() for i in self.search_args]
        self.search_args.append(self.id)

    def __repr__(self):
        return f"{self.name}"


class Server:
    __slots__ = (
        "data",
        "id",
        "name",
        "invite",
        "categories",
        "keywords",
        "description",
        "search_args",
    )

    def __init__(self, *, data=None):
        self.data = data
        self.id = int(self.data[0])
        self.name = self.data[1]
        try:
            self.invite = self.data[2]
        except BadInviteArgument:
            self.invite = "Invalid Invite"
        self.categories = json.loads(self.data[3])
        self.keywords = json.loads(self.data[4])
        self.description = self.data[5]
        self.search_args = self.categories + self.keywords
        self.search_args.append(self.name)
        self.search_args = [i.lower() for i in self.search_args]
        self.search_args.append(self.id)

    def __repr__(self):
        return f"{self.name}"
