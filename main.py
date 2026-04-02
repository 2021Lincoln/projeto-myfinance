from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI() 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/transacoes/", response_model=schemas.Transacao)
def criar_transacao(transacao: schemas.TransacaoCreate, db: Session = Depends(get_db)):
    db_transacao = models.Transacao(**transacao.dict())
    db.add(db_transacao)
    db.commit()
    db.refresh(db_transacao)
    return db_transacao


@app.get("/transacoes/", response_model=list[schemas.Transacao])
def listar_transacoes(db: Session = Depends(get_db)):
    return db.query(models.Transacao).order_by(models.Transacao.data.desc()).all()

@app.get("/resumo/")
def obter_resumo(db: Session = Depends(get_db)):
    receitas = db.query(func.sum(models.Transacao.valor)).filter(models.Transacao.tipo == 'Receita').scalar() or 0
    despesas = db.query(func.sum(models.Transacao.valor)).filter(models.Transacao.tipo == 'Despesa').scalar() or 0
    return {
        "total_receitas": float(receitas),
        "total_despesas": float(despesas),
        "saldo": float(receitas - despesas)
    }

@app.get("/transacoes/filtro/", response_model=List[schemas.Transacao])
def filtrar_transacoes(
    tipo: Optional[str] = None, 
    categoria: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    query = db.query(models.Transacao)
    if tipo:
        query = query.filter(models.Transacao.tipo == tipo)
    if categoria:
        query = query.filter(models.Transacao.categoria == categoria)
    return query.all()

# 2. Rota de Resumo por Categoria (Usa seu TransacaoCategoriaSummary)
@app.get("/resumo/categorias/", response_model=List[schemas.TransacaoCategoriaSummary])
def resumo_por_categoria(db: Session = Depends(get_db)):
    resultado = db.query(
        models.Transacao.categoria,
        func.sum(models.Transacao.valor).label("total")
    ).filter(models.Transacao.tipo == "Despesa").group_by(models.Transacao.categoria).all()
    
    return [{"categoria": r[0], "total": r[1]} for r in resultado]



@app.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int, db: Session = Depends(get_db)):
    db_trans = db.query(models.Transacao).filter(models.Transacao.id == transacao_id).first()
    if not db_trans:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(db_trans)
    db.commit()
    return {"status": "removido"}