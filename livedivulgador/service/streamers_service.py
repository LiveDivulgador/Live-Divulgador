from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import select

from livedivulgador.database.engine import Session
from livedivulgador.database.entities.streamer import Streamer


class StreamersService:
    @staticmethod
    def get_streamers() -> list[Streamer]:
        with Session() as session:
            query = session.query(Streamer).all()

        return query

    @staticmethod
    def get_streamer(twitch_id: int) -> Streamer:
        with Session() as session:
            response = (
                session.query(Streamer)
                .filter(Streamer.twitch_id == twitch_id)
                .all()
            )

        return response

    @staticmethod
    def get_streamer_by_name(streamer_name: str) -> Streamer:
        with Session() as session:
            response = (
                session.query(Streamer)
                .filter(Streamer.name == streamer_name)
                .all()
            )[0]

        return response

    @classmethod
    def create_streamer(cls, streamer: Streamer) -> None:
        with Session() as session:
            existing_streamer = cls.get_streamer(streamer.twitch_id)

            if existing_streamer != []:
                raise SQLAlchemyError("Streamer already exists")

            session.add(streamer)
            session.commit()

    @staticmethod
    def update_streamer(streamer: Streamer) -> None:
        with Session() as session:
            session.merge(streamer)
            session.commit()

    @staticmethod
    def delete_streamer(twitch_id: int) -> None:
        with Session() as session:
            session.query(Streamer).filter(
                Streamer.twitch_id == twitch_id
            ).delete()
            session.commit()

    @staticmethod
    def delete_streamer_by_name(name: str) -> None:
        with Session() as session:
            session.query(Streamer).filter(Streamer.name == name).delete()
            session.commit()

    @staticmethod
    def select_all_by_twitch_id() -> list[Streamer]:
        with Session() as session:
            statement = select(Streamer.twitch_id)
            result = session.execute(statement).all()

        return result

    @staticmethod
    def select_by_twitch_id(twitch_id: int) -> Streamer:
        with Session() as session:
            statement = select(Streamer.twitch_id).where(
                Streamer.twitch_id == twitch_id
            )
            result = session.execute(statement).first()

        return result
