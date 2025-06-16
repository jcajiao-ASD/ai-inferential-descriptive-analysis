"""
Defines custom exceptions related to Pokemon operations.

Classes:
- PokemonNotFoundError: Raised when a Pokemon with a specific identifier is not found.
"""

class PokemonNotFoundError(Exception):
    
    """
    Exception raised when a Pokemon with a specific identifier is not found.

    Attributes
    ----------
    identifier : str | int
        The identifier of the Pokemon that was not found.

    """

    def __init__(self, identifier: str | int):
        """
        Initialize the PokemonNotFoundError with the given identifier.

        Parameters
        ----------
        identifier : str | int
            The identifier of the Pokemon that was not found.
        
        """
        self.identifier = identifier
        super().__init__(f"Pokemon with identifier '{identifier}' not found.")