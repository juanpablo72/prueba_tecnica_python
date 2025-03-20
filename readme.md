# 🏗️ **PRUEBA TECNICA DE YOUTOBE CLONE**

Aplicacion de CLONE YOUTOBE EN DJANGO Y POSTGRESQL Y DOCKER

## 💈 requisitos🏗️ 💈

DOCKER,PYTHON, DJANGO ,POSTGRESQL 

###realizado en django y bootstrap

##intalacion 

### clonar repositorio 
```bash
git clone https://github.com/juanpablo72/prueba_tecnica_python.git
```
### dentro del proyecto y docker abierto en terminal
# Construir levantar contenedores (primera vez)
```bash
docker-compose up --build
```

# Levantar servicios en segundo plano
```bash
docker-compose up -d
```
# Detener y eliminar contenedores + volúmenes
```bash
docker-compose down -v
```
# Aplicar generar migraciones
```bash
docker-compose exec web python manage.py makemigrations
```
# Aplicar migraciones
```bash
docker-compose exec web python manage.py migrate
```
# Crear superusuario
```bash
docker-compose exec web python manage.py createsuperuser
```
# PRUEBAS UNITARIAS
#### Ejecutar todos los tests
```bash
docker-compose exec web python manage.py test
```
#### Ejecutar test individuales populary y history
## history
```bash
docker-compose exec web python manage.py test videos.tests.VideoHistoryTests
```
## populary
```bash
docker-compose exec web python manage.py test videos.tests.PopularVideosTestsUnit
```
#Estructura del Proyecto
```bash
    clone_youtobe/
        ├── docker-compose.yml
        ├── .env
        ├── django_app/
        │   ├── Dockerfile
        │   ├── manage.py
        │   ├── requirements.txt (librerias a instalar)
        │   ├── Templates( html)
        │   ├──    User (logica de usuarios)
        │   ├──     videos ( logica de de videos)
        │   └──    clone_youtobe(configuracion del proyecto)
        └── nginx/
            ├── Dockerfile
            └── default.conf

```