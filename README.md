# 🧞 Akinator — FastAPI + PostgreSQL + NextJS

## Estructura del proyecto

```
akinator/
├── docker-compose.yml   ← PostgreSQL local
├── backend/
│   ├── app/
│   │   ├── config.py    ← Variables de entorno
│   │   ├── database.py  ← Conexión SQLAlchemy
│   │   ├── models.py    ← Tablas de la BD
│   │   └── main.py      ← Punto de entrada FastAPI
│   ├── seed.py          ← Carga datos iniciales
│   ├── requirements.txt
│   └── .env
└── frontend/            ← NextJS (Fase 3)
```

---

## 🚀 Cómo levantar el proyecto (Fase 1)

### 1. Levantar PostgreSQL con Docker

```bash
docker-compose up -d
```

Verifica que el contenedor esté corriendo:

```bash
docker ps
```

### 2. Crear entorno virtual e instalar dependencias

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Correr el seed (carga los 3 personajes)

```bash
python seed.py
```

### 4. Levantar FastAPI

```bash
uvicorn app.main:app --reload
```

La API estará disponible en: http://localhost:8000
Documentación automática en: http://localhost:8000/docs

---

## 📊 Modelo de datos

### Tabla: personajes

| Campo       | Tipo    | Descripción          |
| ----------- | ------- | -------------------- |
| id          | Integer | PK                   |
| nombre      | String  | Nombre del personaje |
| descripcion | Text    | Descripción breve    |
| imagen_url  | String  | URL de imagen        |

### Tabla: preguntas

| Campo     | Tipo    | Descripción              |
| --------- | ------- | ------------------------ |
| id        | Integer | PK                       |
| texto     | String  | La pregunta              |
| categoria | String  | Categoría (profesion...) |

### Tabla: atributos

| Campo        | Tipo    | Descripción                      |
| ------------ | ------- | -------------------------------- |
| id           | Integer | PK                               |
| personaje_id | Integer | FK → personajes                  |
| pregunta_id  | Integer | FK → preguntas                   |
| valor        | Integer | 1 = Sí, -1 = No, 0 = Más o menos |

---

## 🌐 Deploy

| Servicio      | Plataforma | Notas                             |
| ------------- | ---------- | --------------------------------- |
| Frontend      | Vercel     | Conectar repo → carpeta /frontend |
| Backend       | Render     | Conectar repo → carpeta /backend  |
| Base de datos | Supabase   | Cambiar DATABASE_URL en .env      |
