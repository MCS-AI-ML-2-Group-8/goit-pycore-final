from data.email_commands import CreateEmail
from data.phone_commands import CreatePhone


def test_phone_number():
    _ = CreatePhone(phone_number="0000011111")

def test_email():
    _ = CreateEmail(email_address="x@a.co")
