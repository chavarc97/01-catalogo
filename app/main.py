import fastapi
from app.routes import clientes, productos
from app.db import engine, Base
from app.models import client, product

Base.metadata.create_all(bind=engine)

app = fastapi.FastAPI(title="Microservicio - Catálogo")

app.include_router(clientes.router)
app.include_router(productos.router)

@app.get("/")
def root():
    return {
        "message": "API Catálogo Funcional. Visita /docs para ver los endpoints interactivos."
    }
