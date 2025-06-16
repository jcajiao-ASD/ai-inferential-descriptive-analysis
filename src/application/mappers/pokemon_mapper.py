"""
Define the module contains the PokemonMapper class.

It's responsible for converting external Pokemon API responses
into domain Pokemon entities.
"""

from typing import Any

from src.domain.entities.pokemon import Pokemon


class PokemonMapper:
    
    """
    Mapper class responsible for converting external Pokemon API responses.

    Into domain Pokemon entities.
    """

    @staticmethod
    def from_pokeapi_response(data: dict[str, Any]) -> Pokemon:
        """
        Transform a PokeAPI response dictionary into a Pokemon domain entity.

        Args:
            data: Dictionary containing Pokemon data from the PokeAPI response.
                 Expected to have 'id', 'name', and 'types' keys.

        Returns:
            Pokemon: A Pokemon domain entity with the extracted data.
                    Contains id, name, and a list of Pokemon types.

        """
        types_list: list[str] = []
        if "types" in data and isinstance(data["types"], list):
            for type_info in data["types"]:
                if (
                    isinstance(type_info, dict)
                    and "type" in type_info
                    and isinstance(type_info["type"], dict)
                    and "name" in type_info["type"]
                ):
                    types_list.append(type_info["type"]["name"])

        return Pokemon(id=data.get("id"), name=data.get("name"), types=types_list)
