import enum


class AssetType(enum.Enum):
    Stock = "Stock"
    Crypto = "Crypto"
    REIT = "REIT"
    IRA = "IRA"
    _401K = "401K"
    HSA = "HSA"
