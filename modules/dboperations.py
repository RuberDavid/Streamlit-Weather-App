import sqlite3
import os




def db_cursor( db_file):
    """

    Parameters
    ----------
    db_file

    Returns
        cur: cursor to de database
        if not, returns None
    -------

    """
    try:
        con = sqlite3.connect( db_file )
        return con.cursor()
    except sqlite3.Error as e:
        print(str(e)) # TODO: context manager for closing conection
        return None


def create_users_table(db_file):
    with sqlite3.connect(db_file) as con:
        con.execute("CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY, name TEXT, email TEXT , latitude REAL, longitude REAL, temperature REAL , weather_code TEXT )")
      # con.execute("CREATE TABLE IF NOT EXISTS weather( user_id integer, ..., FOREIGN KEY(user_id) REFERENCES users()") ) # TODO

def select_all_users(db_file):
    with sqlite3.connect(db_file) as con:
        cur = con.execute("SELECT * FROM users")
        column_names = [x[0] for x in cur.description]
        results = cur.fetchall()
        return column_names, results
#def insert_into_users(name: str, email: str, temperature: float ,  ):

def insert_into_users(db_file, fields:tuple):
    with sqlite3.connect(db_file) as con:
        sql = """ INSERT INTO users (name,email, latitude, longitude, temperature, weather_code)
              VALUES (?,?,?,?,?,?)"""
        con.execute(sql, fields)



if __name__ == "__main__":
    import pandas as pd
    DB_FILENAME = 'weather.db'
    create_users_table(DB_FILENAME)
    select_all_users(DB_FILENAME)

#    print(module_dir)
    name = 'Oscar'
    email = 'oscar.fenix@gmail.com'
    latitute = 19.85
    longitude = 56
    weather = 8.4
    weather_code = "cloudy"

    insert_into_users(DB_FILENAME,(name, email, latitute, longitude, weather, weather_code))
    column_names, results = select_all_users(DB_FILENAME)
    print(results)
    df = pd.DataFrame(results, columns=column_names)
    print(df)
#   r'''INSERT INTO user_data VALUES (''' +'\'{}\''.format(nombre) + ''', ''' +'\'{}\''.format(email) + ''', ''' +'{}'.format(latitute) + ''', ''' +'{}'.format(longitude) + ''', ''' +'\'{}\''.format(weather) + ''')'''

#    nombre = 'Oscar'
#    email = 'oscar.fenix@gmail.com'
#    latitute = 19.85
#    longitude = 56
#    weather = 'El clima de hoy es'
#    r'''INSERT INTO user_data VALUES (''' +'\'{}\''.format(nombre) + ''', ''' +'\'{}\''.format(email) + ''', ''' +'{}'.format(latitute) + ''', ''' +'{}'.format(longitude) + ''', ''' +'\'{}\''.format(weather) + ''')'''

#    create_data()

#    try:
#        insert_data('Oscar', 'oscar.fenix@gmail.com', 19.85, 56, 'El clima de hoy es')
#    except sqlite3.OperationalError:
