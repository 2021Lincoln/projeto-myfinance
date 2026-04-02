from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class TransacaoBase(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str
    categoria: str
    data: date

class TransacaoCreate(TransacaoBase):
    pass

class Transacao(TransacaoBase):
    id: int
    class Config:
        from_attributes = True

class TransacaoUpdate(BaseModel):
    descricao: str | None = None
    valor: Decimal | None = None
    tipo: str | None = None
    categoria: str | None = None
    data: date | None = None


class TransacaoDelete(BaseModel):
    id: int

class TransacaoRead(Transacao):
    pass    

class TransacaoList(BaseModel):
    transacoes: list[Transacao]

class TransacaoFilter(BaseModel):
    tipo: str | None = None
    categoria: str | None = None
    data_inicio: date | None = None
    data_fim: date | None = None

class TransacaoSummary(BaseModel):
    total_entradas: Decimal
    total_saidas: Decimal
    saldo: Decimal

class TransacaoCategoriaSummary(BaseModel):
    categoria: str
    total: Decimal

class TransacaoMesSummary(BaseModel):
    mes: str
    total_entradas: Decimal
    total_saidas: Decimal
    saldo: Decimal

class TransacaoAnoSummary(BaseModel):
    ano: int
    total_entradas: Decimal
    total_saidas: Decimal
    saldo: Decimal  

class TransacaoCategoriaMesSummary(BaseModel):
    categoria: str
    mes: str
    total: Decimal


class Config:
        from_attributes = True