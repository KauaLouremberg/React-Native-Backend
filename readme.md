
---

# Inicializando

### 
```md
 - Crie o Ambiente Virtual e rode os comandos a seguir
````

---

# Comandos

### 
```md
 - Baixar requisitos - pip install -r requirements.txt
 - sudo apt update
 - sudo apt install postgresql postgresql-contrib
 - python manage.py migrate
````

# Como rodar

Uvicorn Necessario para uso de websocket (Obrigatorio!)
```md
 - uvicorn backend.asgi:application --reload --host 0.0.0.0 --port 8000
````

# Criar SuperUser

```md
 - python manage.py createsuperuser;
````
