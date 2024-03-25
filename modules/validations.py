import re


def val_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern, email):
        return True
    else:
        return False

if __name__ == "__main__":
    correos = ["usuario@example.com", "correo@dominio.co.uk", "incorrecto@@example.com", "sin_arroba.com"]

    for correo in correos:
        print(correo, ":", val_email(correo))