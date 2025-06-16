"""
Defines the Pokemon entity.

The Pokemon entity represents a Pokemon with attributes such as
id, name, and types.
"""

from dataclasses import dataclass, field


@dataclass
class Pokemon:
    
    """
    Represents a Pokemon entity.

    Attributes
    ----------
    id : int
        The unique identifier for the Pokemon.
    name : str
        The name of the Pokemon.
    types : list[str]
        The types associated with the Pokemon.

    """

    id: int
    name: str
    types: list[str] = field(default_factory=list)
