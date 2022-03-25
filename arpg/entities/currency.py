# Standard library imports  
from dataclasses import dataclass

# Local application imports
from entities.items import BaseItem 



# Coin Value
COPPER_VALUE = 1
SILVER_VALUE = 10
GOLD_VALUE = 100
PLATINUM_VALUE = 1000

LOW_PURITY = 1
HIGH_PURITY = 5



# Currency
@dataclass(frozen=True)
class Coin(BaseItem):
    weight: int = 0.01

    def __init__(self, *args, **kwargs):
        if type(self) == Coin:
            raise NotImplementedError('Do not instantiate Coin directly')

@dataclass(frozen=True)
class CopperCoin(Coin):
    name: str = 'Copper Coin'
    worth: int = COPPER_VALUE * LOW_PURITY

@dataclass(frozen=True)
class GreaterCopperCoin(CopperCoin):
    name: str = 'Greater Copper Coin'
    worth: int = COPPER_VALUE * HIGH_PURITY

@dataclass(frozen=True)
class SilverCoin(Coin):
    name: str = 'Silver Coin'
    worth: int = SILVER_VALUE * LOW_PURITY

@dataclass(frozen=True)
class GreaterSilverCoin(SilverCoin):
    name: str = 'Greater Silver Coin'
    worth: int = SILVER_VALUE * HIGH_PURITY

@dataclass(frozen=True)
class GoldCoin(Coin):
    name: str = 'Gold Coin'
    worth: int = GOLD_VALUE * LOW_PURITY

@dataclass(frozen=True)
class GreaterGoldCoin(GoldCoin):
    name: str = 'Greater Gold Coin'
    worth: int = GOLD_VALUE * HIGH_PURITY

@dataclass(frozen=True)
class PlatinumCoin(Coin):
    name: str = 'Platinum Coin'
    worth: int = PLATINUM_VALUE * LOW_PURITY

@dataclass(frozen=True)
class GreaterPlatinumCoin(PlatinumCoin):
    name: str = 'Greater Platinum Coin'
    worth: int = PLATINUM_VALUE * HIGH_PURITY
