# API vivelibre-api

API de acceso a los endpoints de la prueba técnica de ViveLibre.

Por defecto escucha en el puerto 8008 y se apoya en una base de datos sqllite en memoria.

Esos y otros parámetros se pueden configurar en ```/src/api/settings.py```


## Maintainer
@schacon83@gmail.com

# Uso

A continuación se describe como utilizar la aplicacion

## Ejecución

Primero necesitamos instalar el entorno virtual.

```
pip install -r requirements.txt
```

Y con esto ya podemos ejecutar la aplicación

```
python src/python
```

## Despliegue

Se hace el build:

```
docker build -f Dockerfile -t vivelibre-api:latest .
```

Se ejecuta:

```
docker run --name vivelibre-api-1 -p 8008:8008 vivelibre-api
```

## Endpoints

### Ejercicio 1:

Inscribir estudiantes en cursos
```
POST /school/courses/<int:course_id>/students/<int:student_id>
```
Obtener la lista de estudiantes en un curso
```
GET /school/courses/<int:course_id>/students
```
Obtener la lista de cursos de un estudiante en particular
```
GET /school/students/<int:student_id>/courses
```
Filtrar los profesores con una edad comprendida entre los 35 y 50 años
```
GET /school/professors?min_age=30&max_age=50
```
Filtrar los estudiantes que estudian 'Engineering'
```
GET /school/students?career=Engineering
```
Además se han añadido otros endpoints para facilitar la consulta de datos

Consulta de registros modificados en el modelo de datos
```
GET /school/logs
```


### Ejercicio 2:

Lanzar proceso de manipulación de datos
```
POST /movies
```