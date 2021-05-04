from ..funcs import get_applicants
from ..funcs import send_message_many
from .. import APIKEY, EMAIL, PASSWORD  # pylint: disable=relative-beyond-top-level
from ..errors import SentError


async def applicant_messages(*, alliance=None):
    try:
        for app in alliance.applicants:
            print(app.id)
    except SentError:
        pass