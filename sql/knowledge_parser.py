import re

from sql.db import cur, connection

separator_regex = "\s*,\s*"
disease_regex = f"\ndisease\(\s*'?(?P<animal>.*?)'?\s*,\s*'?(?P<disease>.*?)'?\s*,\s*'(?P<description>.*)'\)"
simptom_regex = f"\nsimptom\(\s*'?(?P<animal>.*?)'?\s*,\s*'?(?P<disease>.*?)'?\s*,\s*'(?P<simptom>.*)'\)"
tip_regex = f"\ntip\(\s*'?(?P<animal>.*?)'?\s*,\s*'?(?P<short>.*?)'?\s*,\s*'(?P<long>.*)'\)"

FILE = r'D:\Univer\Semestrul VI\Sisteme Expert\Project\knowledge.pl'

with open(FILE) as file:
    content = file.read()


def get_animal_id(animal):
    result = cur.execute(f"SELECT id FROM animal WHERE name = '{animal}';").fetchone()
    return result[0]


def get_disease_id(disease, animal_id):
    result = cur.execute(f"SELECT id FROM disease WHERE name = '{disease}' AND animal_id = '{animal_id}';").fetchone()
    return result[0]


def insert_tips():
    for match in re.findall(tip_regex, content):
        animal, short, long = match
        animal_id = get_animal_id(animal)
        cur.execute(f"INSERT INTO tip (short, long, animal_id) VALUES ('{short}', '{long}', '{animal_id}');")
    connection.commit()


def insert_diseases():
    for match in re.findall(disease_regex, content):
        animal, disease, description = match
        animal_id = get_animal_id(animal)
        cur.execute(
            f"INSERT INTO disease (name, description, animal_id) VALUES ('{disease}', '{description}', '{animal_id}');")
    connection.commit()


def insert_simptoms():
    for match in re.findall(simptom_regex, content):
        animal, disease, simptom = match
        animal_id = get_animal_id(animal)
        disease_id = get_disease_id(disease, animal_id)
        cur.execute(
            f"INSERT INTO simptom (name, disease_id, animal_id) VALUES ('{simptom}', '{disease_id}', '{animal_id}');")
    connection.commit()
