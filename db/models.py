from sqlalchemy import (
    BigInteger,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "member"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)

    levels: Mapped[list["Level"]] = relationship(
        back_populates="member", cascade="all, delete-orphan"
    )


class Guild(Base):
    __tablename__ = "guild"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)
    formula: Mapped[str] = mapped_column(String, default="50x")

    levels: Mapped[list["Level"]] = relationship(
        back_populates="guild", cascade="all, delete-orphan"
    )


class Level(Base):
    __tablename__ = "level"

    id_member: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("member.id", ondelete="CASCADE"), primary_key=True
    )
    id_guild: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("guild.id", ondelete="CASCADE"), primary_key=True
    )
    level: Mapped[int] = mapped_column(default=0)
    xp: Mapped[int] = mapped_column(default=0)

    guild: Mapped["Guild"] = relationship(back_populates="levels")
    member: Mapped["Member"] = relationship(back_populates="levels")
