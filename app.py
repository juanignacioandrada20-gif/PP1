from typing import Annotated
from fastapi import  HTTPException, Body, FastAPI, Path, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.title = "App comercio"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "https://127.0.0.1:8000/articulos",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
IntPositivo= Annotated[int, Field(gt=0)]
StrNombre= Annotated[str, Field(min_length=2, max_length=60)]
FloatPrecio= Annotated[float, Field(gt=1000, lt=999999)]
BoolActivo= Annotated[bool,Field(description="¿Disponible?")]

class ArticuloSchema(BaseModel):
    id: Annotated[int, Field(gt=0, description="ID del articuloi", deprecated=True)]
    nombre: StrNombre
    precio: FloatPrecio = 1500
    activo: BoolActivo = True

class ArticuloUptadeSchema(BaseModel):
    nombre: StrNombre
    precio: FloatPrecio = 2000
    activo: BoolActivo = True

NOT_FOUND_RESPONSE = {
    404: {
        "description": "Articulo no encontrado",
        "content": {
            "application/json":{
                "example": {"detail": "Articulo no encontrado"}
            }
        },
    },
}

articulos = [
    {"id": 1, "nombre": "Remeras overside", "precio": 20000, "activo": True},
    {"id": 2, "nombre": "Remeras comunes", "precio": 15000, "activo": True},
    {"id": 3, "nombre": "Buzos", "precio": 40000, "activo": True},
    {"id": 4, "nombre": "Pantalones cargo", "precio": 50000, "activo": True},
    {"id": 5, "nombre": "Bermudas", "precio": 35000, "activo": True},
]

@app.get("/articulos", response_model=list[ArticuloSchema])
async def get_articulos():
    return articulos

@app.get("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema,) 
async def get_articulos_by_id(
    id: Annotated[int, Path(gt=0)],
):
    for articulo in articulos:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")

@app.post("/articulos", response_model=list[ArticuloSchema])
async def agregar_articulo(articulo_nuevo: ArticuloSchema):
    articulos.append(articulo_nuevo.model_dump())
    return articulos

@app.delete("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema,)
async def borrar_articulos(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[bool, Query(description="Mantener registro")] = False,
) -> ArticuloSchema:
    for articulo in articulos:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = (False)
            else:
                articulos.remove(articulo)
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")
    
@app.put("/articulos/{id}", responses=NOT_FOUND_RESPONSE, response_model=ArticuloSchema,)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto. >0")],
    articulo_editar: ArticuloUptadeSchema,
):
    for articulo in articulos:
        if articulo["id"] == id:
            articulo["nombre"] = articulo_editar.nombre
            articulo["precio"] = articulo_editar.precio
            articulo["activo"] = articulo_editar.activo
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")