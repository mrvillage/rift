import asyncio
import json

from ..query import get_document
from .base import Base


class Document(Base):
    def __init__(self, *, data=None, document_id=None):
        if data is None:
            self.data = asyncio.run(get_document(document_id=document_id))
        else:
            self.data = data
        self.id = self.data[0]
        self.name = self.data[1]
        self.url = self.data[2]
        self.categories = (
            json.loads(self.data[3])
            if self.data[3] is not None and self.data[3]
            else None
        )
        self.keywords = (
            json.loads(self.data[4])
            if self.data[4] is not None and self.data[4]
            else None
        )
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
