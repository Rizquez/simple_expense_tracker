# Simple Expense Tracker

## Creacion del entorno de virtual:
python -m virtualenv nombreEntorno

> [!TIP]
Se recomienda la creación de un entorno virtual para optimizar el desarrollo y la ejecución del proyecto.

## Dependencias
pip freeze > requirements.txt  
pip install -r requirements.txt

> [!NOTE]
En la ubicación src/database/ se encuentra creada la BBDD en SQLite donde se almacena la informacion sobre los gastos que el usuario registra en la aplicacion. Acontinuacion se muestra el script para la creacion de la tabla

```
CREATE TABLE IF NOT EXISTS record_expense (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    period DATE,
    amount INTEGER,
    category TEXT,
    note TEXT
);
```

## Contribuciones
Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor haz un 'fork' del repositorio, crea una rama con tus mejoras y envía un 'pull request'.

## Licencia
Este proyecto está bajo una licencia MIT. Consulta el archivo LICENSE para más detalles.
