from unicodedata import numeric

from sqlalchemy import Column, Date, Integer, Numeric, String
from database import Base   

class Transacao(Base):
    __tablename__ = 'transacoes'
    
    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String)
    valor = Column(Numeric(10, 2))
    tipo = Column(String)
    categoria = Column(String)
    data = Column(Date)