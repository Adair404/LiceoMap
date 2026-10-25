import re

_CLEAN = re.compile(r"[.\s]")
_FORMAT = re.compile(r"^\d{7,8}-[0-9K]$")


def check_digit(body: str) -> str:
    total, factor = 0, 2
    for digit in reversed(body):
        total += int(digit) * factor
        factor = factor + 1 if factor < 7 else 2
    remainder = 11 - total % 11
    if remainder == 11:
        return "0"
    if remainder == 10:
        return "K"
    return str(remainder)


def normalize_rut(value: str) -> str | None:
    """Devuelve el RUT como 12345678-9 (sin puntos) o None si es inválido."""
    cleaned = _CLEAN.sub("", value or "").upper()
    if "-" not in cleaned and len(cleaned) >= 8:
        cleaned = f"{cleaned[:-1]}-{cleaned[-1]}"
    if not _FORMAT.match(cleaned):
        return None
    body, verifier = cleaned.split("-")
    return cleaned if check_digit(body) == verifier else None
