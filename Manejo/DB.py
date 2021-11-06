import sqlite3

class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect('fifa.db')
        self.cursor = self.connection.cursor()
        # Se tiene un diccionario con los tipos de datos que se van a insertar en las tablas
        self.types = {'int':'INTEGER',
                 'str':'TEXT',
                 'NoneType':'TEXT',
                 'bool':'TEXT',
                 'list':'TEXT'
        }
    

    def createTablePlayers(self, example):

        sql = '''CREATE TABLE IF NOT EXISTS"players" (
                "id"	INTEGER NOT NULL UNIQUE,
                "club_id"	INTEGER,
                "league_id"	INTEGER,
                "nation_id"	INTEGER'''
        
        keys = example.keys()
        for key in keys:
            if  not key in ['id','attributes','headshot']:
                if isinstance(example[key], (dict,)):
                    # Se crea una nueva tabla si la key es league, club o nation
                    self.createTable(example, key)
                else:
                    value = example[key]
                    #print(key, value)
                    sql += f',"{key}"  {self.types[type(value).__name__]}'
            elif key == 'headshot':
                value = example[key]
                for v in value.keys():
                    sql += f',"{key}_{v}"  {self.types[type(value[v]).__name__]}'
        
        sql += ''',FOREIGN KEY("league_id") REFERENCES "leagues"("id"),
                FOREIGN KEY("nation_id") REFERENCES "nations"("id"),
                FOREIGN KEY("club_id") REFERENCES "clubs"("id"),
                PRIMARY KEY("id"));'''
       
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise e
    
    # Se crean las distintas tablas como lo son ligas, clubes, nacionalidades
    def createTable(self, example, tabla):
        sql = f'''CREATE TABLE IF NOT EXISTS "{tabla}s" (
	            "id"	INTEGER NOT NULL UNIQUE
	            '''

        tab = example[tabla]
        for key in tab:
            value = tab[key]
            if isinstance(value, (dict,)):
                for v in value.keys():
                    t = value[v]
                    if isinstance(t, (dict, )):
                        for p in t.keys():
                            sql += f',"{key}_{v}_{p}"  {self.types[type(t[p]).__name__]}'
                    else:
                        sql += f',"{key}_{v}"  {self.types[type(value[v]).__name__]}'
            elif key != 'id':
                sql += f',"{key}"  {self.types[type(value).__name__]}'
             
        sql += ''',PRIMARY KEY("id"))'''

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise e
    
    # Se crean las tablas que contienen los atributos de los jugadores
    def createTableAttri(self, attribute):
        name = attribute['name']
        sql = f'''CREATE TABLE IF NOT EXISTS "{name}" (
                "id"	INTEGER NOT NULL UNIQUE,
                "id_player"	INTEGER NOT NULL UNIQUE'''


        for key in attribute.keys():
            if key != 'name':
                value = attribute[key]
                sql += f',"{key}"  {self.types[type(value).__name__]}'

        
        sql += ''',
                FOREIGN KEY("id_player") REFERENCES "players"("id"),
                PRIMARY KEY("id" AUTOINCREMENT)
            );'''
        

        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise e
    
    # Retorna una cadena con el formato adecuado si se trata para un entero o un texto
    def intOrStr(self, element, end=False) -> str:
        plus = ','
        if end:
            plus=')'
        if isinstance(element, int):
            return f'{element}{plus}'
        return f"'{element}'{plus}"
    

    def insertPlayer(self, player):
        sql = "INSERT OR IGNORE INTO players ("
        values = 'VALUES ('
        keys = list(player.keys())
        for key in keys:
            if key != 'attributes':
                if key == keys[-1]:
                    sql += f'{key}) '
                    values += self.intOrStr(player[key], end=True)
                elif key in ['league','club','nation']:
                    sql += f'{key}_id,'
                    values += f"{player[key]['id']},"

                    # Se inserta la liga, club y nacionalidad, cada una en su respectiva tabla
                    self.insertToTable(player, key)
                else:
                    if not isinstance(player[key],dict):
                        sql += f'{key},'
                    if not isinstance(player[key],int):
                        if isinstance(player[key], list):
                            value = ''.join(f'{x},' for x in player[key])
                            values += f"'{value}',"
                        elif key == 'id':
                            values += f'{player[key]},'
                        else:
                            value = player[key]
                            if isinstance(value,dict):
                                for v in value.keys():
                                    sql += f'{key}_{v},'
                                    values += self.intOrStr(value[v])
                            else:
                                values += f"'{str(player[key])}',"
                    else:
                        values += f"'{player[key]}',"
            else:
                attributes = player[key]
                for a in attributes:
                    self.insertAttributes(a, player['id'])

        sql += values
        try:
            self.cursor.execute(sql,)
            self.connection.commit()
        except Exception as e:
            raise e

    def insertToTable(self, element, tabla):
        sql = f'''INSERT OR IGNORE INTO {tabla}s ('''
        values = 'VALUES ('
        
        tab = element[tabla]
        # Se recorren cada uno de los atributos del atributo league, nacionalidad o club del jugador
        for key in tab.keys():
            value = tab[key]
            if key == list(tab.keys())[-1]:
                sql += f"{key}) "
                values += self.intOrStr(value, end=True)
            elif isinstance(value, (dict,)):
                for v in value.keys():
                    t = value[v]
                    if isinstance(t, (dict, )):
                        for p in t.keys():
                            sql += f"{key}_{v}_{p},"
                            values += self.intOrStr(t[p])
                    else:
                        sql += f"{key}_{v},"
                        values += self.intOrStr(value[v])
            else:
                sql += f"{key},"
                values += self.intOrStr(value)
             
        sql += values
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise e
    
    # Se separan los atributos que estan en la llave de attributes y se intertan en sus respectivas tablas
    def insertAttributes(self, attribute, player_id):
        name = attribute['name']
        sql = f'''INSERT OR IGNORE INTO "{name}" (
                id_player, '''
        values = f'VALUES ({player_id},'
        for key in attribute.keys():
            # No se insertar el nombre del atributo ya que la tabla tiene dicho nombre
            if key != 'name':
                if key != list(attribute.keys())[-1]:
                    sql += f'{key},'
                    value = attribute[key]
                    values += self.intOrStr(value)
                else:
                    sql += f'{key})'
                    value = attribute[key]
                    values += self.intOrStr(value, end=True)
        sql += values
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            raise e