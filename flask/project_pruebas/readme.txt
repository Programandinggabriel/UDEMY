Exportar flask variable entorno 
    export FLASK_APP=ruta_aplicacion_app

COMANDOS QUE SE INSTALAN AL MOMENTO DE INSTALAR FLASK-MIGRATE
PARA GENERAR MIGRACIONES DE LOS MODELOS QUE SE HAYAN CREADO
    flask db --> muestra los comandos habilitados para manipular la bd
    flask db init --> inicia carpeta de MIGRACIONES
    flask db migrate -m 'Migracion del modelo abc...' (este genera una tb en la bd URI CONFIGURADA para sqlalchemy)
    flask db upgrade --> aplica cambios a la base de datos
    flask db downgrade --> revierte cambios en el upgrade mas reciente
    flask db history --> muestra history de migraciones hechas
    flask db show --> muestra el history mas detallado