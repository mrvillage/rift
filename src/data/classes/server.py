import json

from discord.ext.commands import BadInviteArgument

__all__ = ("Server",)


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
        self.categories = json.loads(self.data[3]) if self.data[3] is not None else None
        self.keywords = json.loads(self.data[4]) if self.data[4] is not None else None
        self.description = self.data[5]
        self.search_args = []
        if self.categories is not None:
            self.search_args.extend(self.categories)
        if self.keywords is not None:
            self.search_args.extend(self.keywords)
        if self.name is not None:
            self.search_args.append(self.name)
        self.search_args = [i.lower() for i in self.search_args]
        if self.id is not None:
            self.search_args.append(str(self.id))

    def __repr__(self):
        return f"{self.name}"
