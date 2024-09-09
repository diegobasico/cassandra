# Cassandra
Herramienta de control de costos en obra escrita en Python.
## ¿Cómo funciona?
La estructura de costos en obra se divide en títulos y partidas. Cada partida corresponde a un análisis de precios unitarios, el cual a su vez se relaciona con una lista de insumos y precios. Estos tres elementos se organizan en bases de datos SQLite y son procesados en python. Este análisis de datos conforma todo lo necesario para estimar el presupuesto a la conclusión y gestionar el valor ganado.
## ¿Cómo puedo usarlo?
El proyecto se encuentra en desarrollo. Puedes revisarlo si dominas CLI; el backend funciona pero la interfaz gráfica no ha sido implementada aún. Si dominas PySide6, puedes colaborar.
## Instalación
Por el momento, solo se necesita inicializar el repositorio en un ambiente virtual que contenga python 3.12 y tenga instalados ```openpyxl```, ```pandas``` y ```sqlite3```. La recomendación es usar ```miniconda3``` para resolver dependencias.
