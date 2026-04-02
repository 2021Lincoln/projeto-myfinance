from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Onde o banco vai ser criado (um arquivo chamado financeiro.db)
SQLALCHEMY_DATABASE_URL = "sqlite:///./financeiro.db"

# 2. O 'motor' que conversa com o banco
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. A sessão que usamos para fazer as consultas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. A base que usaremos para criar nossas tabelas
Base = declarative_base()