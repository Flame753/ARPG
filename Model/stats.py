# Standard library imports 
from dataclasses import dataclass

@dataclass
class CapacityStat:
    capacity: int
    regen_speed: float
    
    def __post_init__(self):
        self.current: int = self.capacity

        if self.regen_speed < 0 or self.regen_speed > 1:
            raise ValueError("Regeneration Speed must be a value between 0 and 1.")

    def is_empty(self) -> bool:
        return self.current <= 0
    
    @property
    def regeneration_amount(self) -> int:
        return round(self.regen_speed * self.capacity)

    def restore(self, amount: int=0):
        self.current += amount
        self.current = min(self.capacity, self.current) # Can't go over the capacity
