from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base, session

class Livros(Base):
    __tablename__ = "livros"

    id:Mapped[int] = mapped_column(primary_key=True)
    nome:Mapped[str]
    emprestimos = relationship("Emprestimos", back_populates="livro")