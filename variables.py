from datetime import date

APP_NAME = "Arkane Game Zone"

FONT = ("Arial", 14)
FONT_LARGE = ("Arial", 18, "bold")
FONT_SMALL = ("Arial", 10)
ROW_COUNT = 23
INCOME_ROW_COUNT = 12

SERVICE_TYPES = {
    "1": "PC ",
    "2": "PS5 ",
    "9": "Topup: ",
    "0": "Games: ",
}

SERVICE_MACROS = SERVICE_TYPES | {
    "3": "PS5 2P ",
    "4": "PS5 4P "
}

BS_MONTHS = {
    "Shrawan 2082": (date(year=2025, month=7, day=17), date(year=2025, month=8, day=16)),
    "Bhadra 2082": (date(year=2025, month=8, day=17), date(year=2025, month=9, day=16)),
    "Ashwin 2082": (date(year=2025, month=9, day=17), date(year=2025, month=10, day=17)),
    "Kartik 2082": (date(year=2025, month=10, day=18), date(year=2025, month=11, day=16)),
    "Mangsir 2082": (date(year=2025, month=11, day=17), date(year=2025, month=12, day=15)),
    "Poush 2082": (date(year=2025, month=12, day=16), date(year=2026, month=1, day=14)),
    "Magh 2082": (date(year=2026, month=1, day=15), date(year=2026, month=2, day=12)),
    "Falgun 2082": (date(year=2026, month=2, day=13), date(year=2026, month=3, day=14)),
    "Chaitra 2082": (date(year=2026, month=3, day=15), date(year=2026, month=4, day=13)),
}
