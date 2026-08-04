from dataclasses import dataclass, field


@dataclass
class SeatCategory:
    name: str
    price: str
    status: str = "AVAILABLE"


@dataclass
class Show:
    movie: str
    language: str
    format: str
    theatre: str
    screen: str
    date: str
    time: str
    categories: list[SeatCategory] = field(default_factory=list)