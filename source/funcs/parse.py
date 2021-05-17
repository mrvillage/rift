from bs4 import BeautifulSoup
from .utils import convert_number


async def parse_alliance_bank(content):
    soup = BeautifulSoup(content, "html.parser")
    tables = soup.find_all(class_="nationtable")
    table = tables[0]
    contents = [i for i in table.contents if i != "\n"]
    data = {}
    for content in contents[1:]:
        data[content.contents[0].contents[1].strip(" ").lower()] = await convert_number(content.contents[1].contents[0])
    return data