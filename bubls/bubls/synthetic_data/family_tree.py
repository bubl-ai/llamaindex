from typing import List, Dict
from typing import Dict


class Person:
    """Represent a person with info about themselves and direct family."""

    def __init__(
        self,
        name: str,
        birth_date: str,
        parents: List[str] = [],
        children: List[str] = [],
        siblings: List[str] = [],
        married: bool = False,
        spouse: str = None,
        alive: bool = True,
        death_date: str = None,
        extra_info: str = "",
    ):
        """Initialize a Person object.

        Args:
            name (str): The name of the person.
            birth_date (str): The birth date of the person
                (format 'YYYY-Month-DD').
            parents (List[str], optional): A list of the person's parents' names.
            children (List[str], optional): A list of the person's children's
                names.
            siblings (List[str], optional): A list of the person's siblings'
                names. Defaults to [].
            married (bool, optional): A boolean indicating whether the person
                is married (True) or not (False). Defaults to False.
            spouse (str, optional): The name of the person's spouse. Defaults
                to None.
            alive (bool, optional): A boolean indicating whether the person is
                alive (True) or deceased (False). Defaults to True.
            death_date (str, optional): The date of death of the person
                (format 'YYYY-Month-DD'). Defaults to None.
            extra_info (str, optional): Use this in case you want to provide
                further information about the individual. Defaults to None.
        """
        self.name: str = name
        self.birth_date: str = birth_date
        self.siblings: List[str] = siblings if siblings is not None else []
        self.parents: List[str] = parents if parents is not None else []
        self.children: List[str] = children if children is not None else []
        self.married: bool = married
        self.spouse: str = spouse if spouse is not None else ""
        self.alive: bool = alive
        self.death_date: str = death_date
        self.extra_info: str = extra_info

    def __str__(self) -> str:
        """Return a string representation of the Person object.

        Returns:
            str: Information about the person.
        """
        alive_status = "Yes" if self.alive else "No"
        death_date_info = (
            f", Death Date: {self.death_date}"
            if not self.alive and self.death_date
            else ""
        )
        married_info = (
            f", Married to: {self.spouse}"
            if self.married and self.spouse
            else ""
        )
        return (
            f"Name: {self.name}, "
            f"Birth Date: {self.birth_date}, "
            f"Parents: {', '.join(self.parents)}, "
            f"Children: {', '.join(self.children)}, "
            f"Siblings: {', '.join(self.siblings)}, "
            f"Married: {self.married}{married_info}, "
            f"Alive: {alive_status}{death_date_info}"
            f", Extra Info: {self.extra_info}"
            "\n"
        )


class Family:
    """A class to represent a family consisting of multiple related persons"""

    def __init__(self, members: Dict[str, Person]):
        """Initialize a Family object.

        Args:
            members (Dict[str, Person]):  A dictionary where keys are names
                and values are Person objects.
        """
        self.members: Dict[str, Person] = members

    def __str__(self) -> str:
        """Return a string representation of the Family object.

        Returns:
            str: Information about all family members.
        """
        family_info = "\n".join(
            str(member) for member in self.members.values()
        )
        return f"Family Members:\n{family_info}"

    def person_information(self, name: str) -> str:
        """Return a string representation of a Person.

        Args:
            name (str): Name of Person

        Returns:
            str: Information about the person.
        """
        return self.members[name].__str__()

    def first_degree_relatives_information(self, name: str) -> str:
        """Return a string representation of a all the first degree
        relatives (parents, children, spuse).

        Args:
            name (str): Name of Person

        Returns:
            str: Information of all first degree relatives.
        """
        info_relatives = []
        for _, member in self.members.items():
            if (
                name in member.parents
                or name in member.children
                or name in member.spouse
            ):
                info_relatives.append(member.__str__())
        return "\n".join(info_relatives)
