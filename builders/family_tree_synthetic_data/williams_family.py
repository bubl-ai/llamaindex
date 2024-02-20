from bubls.synthetic_data.family_tree import Person, Family


family_dict = {}

family_dict["Immanuel Williams"] = Person(
    name="Immanuel Williams",
    birth_date="1940-Feb-1",
    children=[
        "Immanuel Williams II",
        "Viviana Williams",
        "Hannah Williams",
        "Edward Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Tessa Johnson",
    alive=False,
    death_date="2005-Aug-17",
)

family_dict["Tessa Johnson"] = Person(
    name="Tessa Johnson",
    birth_date="1944-Jul-19",
    children=[
        "Immanuel Williams II",
        "Viviana Williams",
        "Hannah Williams",
        "Edward Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Immanuel Williams",
    alive=True,
)

family_dict["Immanuel Williams II"] = Person(
    name="Immanuel Williams II",
    birth_date="1962-Mar-9",
    parents=["Immanuel Williams", "Tessa Johnson"],
    children=[
        "Immanuel Williams III",
        "Raphael Williams",
        "Sora Williams",
    ],
    siblings=[
        "Viviana Williams",
        "Hannah Williams",
        "Edward Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Matilda Smith",
    alive=True,
)

family_dict["Matilda Smith"] = Person(
    name="Matilda Smith",
    birth_date="1961-Dec-1",
    children=[
        "Immanuel Williams III",
        "Raphael Williams",
        "Sora Williams",
    ],
    married=True,
    spouse="Immanuel Williams II",
    alive=True,
)

family_dict["Immanuel Williams III"] = Person(
    name="Immanuel Williams III",
    birth_date="1984-Jan-2",
    parents=["Immanuel Williams II", "Matilda Smith"],
    siblings=[
        "Raphael Williams",
        "Sora Williams",
    ],
    alive=True,
)

family_dict["Raphael Williams"] = Person(
    name="Raphael Williams",
    birth_date="1987-Jan-20",
    parents=["Immanuel Williams II", "Matilda Smith"],
    siblings=[
        "Immanuel Williams III",
        "Sora Williams",
    ],
    alive=True,
)

family_dict["Sora Williams"] = Person(
    name="Sora Williams",
    birth_date="1994-Mar-10",
    parents=["Immanuel Williams II", "Matilda Smith"],
    siblings=[
        "Raphael Williams",
        "Immanuel Williams III",
    ],
    alive=True,
)

family_dict["Viviana Williams"] = Person(
    name="Viviana Williams",
    birth_date="1963-Dec-11",
    parents=["Immanuel Williams", "Tessa Johnson"],
    children=["David Williams"],
    siblings=[
        "Immanuel Williams II",
        "Hannah Williams",
        "Edward Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Lalit Wilson",
    alive=False,
    death_date="2010-Nov-1",
)

family_dict["Lalit Wilson"] = Person(
    name="Lalit Wilson",
    birth_date="1960-Dec-21",
    children=["David Williams"],
    married=True,
    spouse="Viviana Williams",
    alive=True,
)

family_dict["David Williams"] = Person(
    name="David Williams",
    birth_date="1988-May-24",
    parents=["Viviana Williams", "Lalit Wilson"],
    alive=True,
)

family_dict["Hannah Williams"] = Person(
    name="Hannah Williams",
    birth_date="1965-Feb-28",
    parents=["Immanuel Williams", "Tessa Johnson"],
    children=[
        "Hannah Williams II",
        "Thalia Williams",
        "Paulo Williams",
    ],
    siblings=[
        "Immanuel Williams II",
        "Viviana Williams",
        "Edward Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Joseph Anderson",
    alive=True,
)

family_dict["Joseph Anderson"] = Person(
    name="Joseph Anderson",
    birth_date="1965-Feb-26",
    children=[
        "Hannah Williams II",
        "Thalia Williams",
        "Paulo Williams",
    ],
    married=True,
    spouse="Hannah Williams",
    alive=True,
)

family_dict["Hannah Williams II"] = Person(
    name="Hannah Williams II",
    birth_date="1996-Jun-14",
    parents=["Hannah Williams", "Joseph Anderson"],
    siblings=[
        "Thalia Williams",
        "Paulo Williams",
    ],
    alive=False,
    death_date="2005-Oct-2",
)

family_dict["Thalia Williams"] = Person(
    name="Thalia Williams",
    birth_date="1998-Oct-27",
    parents=["Hannah Williams", "Joseph Anderson"],
    siblings=[
        "Hannah Williams II",
        "Paulo Williams",
    ],
    alive=True,
)

family_dict["Paulo Williams"] = Person(
    name="Paulo Williams",
    birth_date="2000-Jul-22",
    parents=["Hannah Williams", "Joseph Anderson"],
    siblings=[
        "Thalia Williams",
        "Hannah Williams II",
    ],
    alive=True,
)

family_dict["Edward Williams"] = Person(
    name="Edward Williams",
    birth_date="1967-Apr-21",
    parents=["Immanuel Williams", "Tessa Johnson"],
    children=[
        "Marianne Williams",
    ],
    siblings=[
        "Immanuel Williams II",
        "Viviana Williams",
        "Hannah Williams",
        "Jeremy Williams",
    ],
    married=True,
    spouse="Lizbeth Miller",
    alive=True,
)

family_dict["Lizbeth Miller"] = Person(
    name="Lizbeth Miller",
    birth_date="1966-Aug-11",
    children=[
        "Marianne Williams",
    ],
    married=True,
    spouse="Edward Williams",
    alive=True,
)

family_dict["Marianne Williams"] = Person(
    name="Marianne Williams",
    birth_date="2002-Feb-2",
    parents=["Edward Williams", "Lizbeth Miller"],
    alive=True,
)

family_dict["Jeremy Williams"] = Person(
    name="Jeremy Williams",
    birth_date="1970-Sep-16",
    parents=["Immanuel Williams", "Tessa Johnson"],
    siblings=[
        "Immanuel Williams II",
        "Viviana Williams",
        "Hannah Williams",
        "Edward Williams",
    ],
    married=False,
    alive=True,
)

new_family = Family(family_dict)

if __name__ == "__main__":
    for person in family_dict:
        print(person)
