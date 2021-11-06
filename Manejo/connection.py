import requests
import json
def main()-> dict:
    print("ACQUIRING INFORMATION FROM THE INTERNET")
    print("wait....") 
    URL = 'https://www.easports.com/fifa/ultimate-team/api/fut/item?page=1' 
    print('Creating the database....')
    data = requests.get(URL) 

    data = data.json()

    items = data['items']

    player = items[0]

    from DB import DataBase
    dataBase = DataBase()
    dataBase.createTablePlayers(player)
    attributes = player['attributes']
    for a in attributes:
        dataBase.createTableAttri(a)
    for p in items:
        dataBase.insertPlayer(p)    
    dataBase.connection.close()
    print('Database created and filled')

    return items

if __name__ == '__main__':
    main()
