from decimal import Decimal, InvalidOperation
import re

MONEY_IDENTIFIER_KEYWORDS = {"biaya", "uang", "nominal", "harga", "tarif", "pagu"}

# Indonesian number to words (terbilang)
TERBILANG_ONES = [
    "", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan"
]

TERBILANG_TENS = [
    "", "sepuluh", "dua puluh", "tiga puluh", "empat puluh",
    "lima puluh", "enam puluh", "tujuh puluh", "delapan puluh", "sembilan puluh"
]

TERBILANG_TEENS = [
    "sepuluh", "sebelas", "dua belas", "tiga belas", "empat belas",
    "lima belas", "enam belas", "tujuh belas", "delapan belas", "sembilan belas"
]


def number_to_words(number):
    """
    Convert number to Indonesian words (terbilang).

    Examples:
        0 -> "nol"
        1 -> "satu"
        2 -> "dua"
        10 -> "sepuluh"
        21 -> "dua puluh satu"
        100 -> "seratus"
        1000 -> "seribu"
    """
    if not isinstance(number, int):
        try:
            number = int(number)
        except (TypeError, ValueError):
            return ""

    if number == 0:
        return "nol"

    if number < 0:
        return f"minus {number_to_words(abs(number))}"

    if number < 10:
        return TERBILANG_ONES[number]

    if number < 20:
        return TERBILANG_TEENS[number - 10]

    if number < 100:
        tens = number // 10
        ones = number % 10
        if ones == 0:
            return TERBILANG_TENS[tens]
        return f"{TERBILANG_TENS[tens]} {TERBILANG_ONES[ones]}"

    if number < 200:
        return f"seratus {number_to_words(number - 100)}"

    if number < 1000:
        hundreds = number // 100
        remainder = number % 100
        if remainder == 0:
            return f"{TERBILANG_ONES[hundreds]} ratus"
        return f"{TERBILANG_ONES[hundreds]} ratus {number_to_words(remainder)}"

    if number < 2000:
        return f"seribu {number_to_words(number - 1000)}"

    if number < 1000000:
        thousands = number // 1000
        remainder = number % 1000
        if remainder == 0:
            return f"{number_to_words(thousands)} ribu"
        return f"{number_to_words(thousands)} ribu {number_to_words(remainder)}"

    if number < 1000000000:
        millions = number // 1000000
        remainder = number % 1000000
        if remainder == 0:
            return f"{number_to_words(millions)} juta"
        return f"{number_to_words(millions)} juta {number_to_words(remainder)}"

    # For larger numbers
    billions = number // 1000000000
    remainder = number % 1000000000
    if remainder == 0:
        return f"{number_to_words(billions)} miliar"
    return f"{number_to_words(billions)} miliar {number_to_words(remainder)}"


def is_money_identifier(name):
    if not name:
        return False

    normalized = str(name).strip().lower()
    tokens = [token for token in re.split(r"[_\W]+", normalized) if token]

    return any(token in MONEY_IDENTIFIER_KEYWORDS for token in tokens)


def format_indonesian_number(value):
    """
    Format angka dengan gaya Indonesia:
    - pemisah ribuan: titik
    - pemisah desimal: koma

    Jika bagian desimal hanya nol, bagian tersebut tidak ditampilkan.
    """
    if value in (None, ""):
        return ""

    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return value

    sign = "-" if decimal_value < 0 else ""
    normalized = format(abs(decimal_value), "f")
    whole_part, _, fraction_part = normalized.partition(".")
    whole_part = f"{int(whole_part):,}".replace(",", ".")

    if fraction_part and any(char != "0" for char in fraction_part):
        return f"{sign}{whole_part},{fraction_part}"

    return f"{sign}{whole_part}"


def parse_localized_decimal(value):
    """
    Parse input angka/currency Indonesia ke Decimal.

    Contoh input yang didukung:
    - 1500000
    - 1.500.000
    - 1.500.000,50
    - Rp1.500.000,50
    """
    if value is None:
        raise ValueError("Value tidak boleh None.")

    normalized = re.sub(r"(?i)(rp|idr)", "", str(value)).strip().replace(" ", "")

    if not normalized:
        raise ValueError("Value kosong.")

    if "," in normalized:
        normalized = normalized.replace(".", "").replace(",", ".")
    elif normalized.count(".") > 1:
        normalized = normalized.replace(".", "")
    elif normalized.count(".") == 1:
        left, right = normalized.split(".")
        if right.isdigit() and len(right) == 3 and left.lstrip("-").isdigit():
            normalized = f"{left}{right}"

    try:
        return Decimal(normalized)
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError("Format angka tidak valid.") from exc

def format_nip(nip):
    """
    Format NIP menjadi: 19830929 201101 1 013
    """
    if not nip:
        return ""

    nip_str = re.sub(r"\D", "", str(nip))  # ambil angka saja

    # Pastikan panjang minimal 18 digit
    if len(nip_str) != 18:
        return nip  # fallback kalau format tidak valid

    return f"{nip_str[0:8]} {nip_str[8:14]} {nip_str[14:15]} {nip_str[15:18]}"
