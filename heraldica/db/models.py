from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Campo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    esmalte: str
    pieza_heraldica: Optional[str] = None
    muebles: List["Mueble"] = Relationship(back_populates="campo")


class Mueble(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    campo_id: int = Field(foreign_key="campo.id")
    nombre: str
    campo: Optional[Campo] = Relationship(back_populates="muebles")


class Escudo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    portador: str
    adorno_exterior: Optional[str] = None
    campo_id: int = Field(foreign_key="campo.id")
    campo: Optional[Campo] = Relationship()
