class Base:
    async def make_attrs(self, *attrs):
        for attr in attrs:
            await getattr(self, f"_make-{attr}")
