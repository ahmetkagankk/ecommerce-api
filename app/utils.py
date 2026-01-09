

# epostanın basit, temel formatta kontrlünü yapar bu kısım

def validate_email(email: str) -> bool:
    return "@" in email and "." in email

