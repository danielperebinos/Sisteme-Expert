import sqlite3

connection = sqlite3.connect('sql/se.db')
cur = connection.cursor()


def create_tables():
    sql_command = '''
        CREATE TABLE animal (
            id integer PRIMARY KEY AUTOINCREMENT,
            name varchar
        );
    '''
    cur.execute(sql_command)

    sql_command = '''
        CREATE TABLE tip (
            id integer PRIMARY KEY AUTOINCREMENT,
            short text,
            long text,
            animal_id integer
        );
    '''
    cur.execute(sql_command)

    sql_command = '''
            CREATE TABLE disease (
                id integer PRIMARY KEY AUTOINCREMENT,
                name varchar,
                description text,
                animal_id integer
            );
        '''
    cur.execute(sql_command)

    sql_command = '''
            CREATE TABLE simptom (
                id integer PRIMARY KEY AUTOINCREMENT,
                name text,
                animal_id integer,
                disease_id integer
            );
        '''
    cur.execute(sql_command)

    connection.commit()


def get_animals():
    result = [row[0] for row in cur.execute('SELECT name from animal;').fetchall() if len(row)]
    return result if result else []


def get_tips(animal):
    result = cur.execute(
        f"SELECT short, long from tip WHERE animal_id IN (SELECT id FROM animal WHERE name = '{animal}');").fetchall()
    d = []
    for row in result:
        d.append({
            'Short': row[0],
            'Long': row[1],
        })
    return d if d else []


def get_diseases(animal):
    result = cur.execute(
        f"SELECT name, description from disease WHERE animal_id IN (SELECT id FROM animal WHERE name = '{animal}');").fetchall()
    d = []
    for row in result:
        d.append({
            'Disease': row[0],
            'Description': row[1],
        })
    return d if d else []


def get_simptoms(animal):
    result = cur.execute(
        f"SELECT name from simptom WHERE animal_id IN (SELECT id FROM animal WHERE name = '{animal}');").fetchall()
    d = []
    for row in result:
        d.append(row[0])
    return d if d else []


def get_simptoms_of_diseases(animal, disease):
    result = cur.execute(
        f"SELECT name from simptom WHERE animal_id IN (SELECT id FROM animal WHERE name = '{animal}') AND disease_id IN (SELECT id FROM disease WHERE name = '{disease}');").fetchall()
    d = []
    for row in result:
        d.append(row[0])
    return d if d else []


def get_diseases_by_simptoms(animal, simptoms):
    diseases_from_simptom = []
    diseases_simptoms = {}
    diseases = []
    score = {}

    for simptom in simptoms:
        result = cur.execute(
            f"SELECT name from disease WHERE id IN (SELECT disease_id FROM simptom WHERE name = '{simptom}' AND animal_id IN (SELECT id FROM animal WHERE name = '{animal}'));").fetchall()
        diseases_from_simptom += [row[0] for row in result]

        for disease in diseases_from_simptom:
            diseases_simptoms[disease] = [simptom] if diseases_simptoms.get(disease, None) is None else \
                diseases_simptoms[disease] + [simptom]

        diseases += diseases_from_simptom

    for disease in diseases:
        score[disease] = diseases.count(disease)

    return {'diseases_simptoms': diseases_simptoms, 'diseases': list(set(diseases)), 'score': score}


try:
    create_tables()
except:
    pass
