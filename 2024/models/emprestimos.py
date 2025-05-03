from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base, session

class Emprestimos(Base):
    __tablename__ = "emprestimos"

    id:Mapped[int] = mapped_column(primary_key=True)

    livro_id:Mapped[int] = mapped_column(ForeignKey("livros.id"))
    usuario_id:Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    livro = relationship("Livros", back_populates="emprestimos")
    usuario = relationship("Usuarios", back_populates="emprestimos")