# Dependencias
Para poder ejecutar adecuadamente cada uno de los puntos es necesario instalar los modulos usados, para ello usar el siguiente comando en la carpeta raiz:
```
pip install -r requirements.txt    
```

## Algoritmia
Una vez instaladas las dependencias se puede ejecutar el codigo del punto de algoritmia, estando en la raiz de la carpeta Algoritmia simplemente se ejecuta el siguiente comando:
```
pytest -v   #-v agrega mas verbosidad a lo que se mostrara de la prueba
```
## Manejo de Python
Para la parte de manejo de Python simplemente se ejecuta el siguiente comando, estando ubicado en la carpeta manejo:
```
python main.py
```
De esta forma se adquieren los datos de la API, se crea la base de datos con los datos adquiridos y luego utilice Flask para generar la ruta GET que permita ver los
datos extraídos
