from src.bot.database.entities.streamer import Streamer
from src.bot.database.engine import Session


class StreamersService:
    @staticmethod
    def get_streamers() -> list(Streamer):
        with Session() as session:
            query = session.query(Streamer).all()

        return query

    @staticmethod
    def get_streamer(id) -> Streamer:
        with Session() as session:
            query = session.query(Streamer).filter(Streamer.id == id).first()

        return query

    @staticmethod
    def create_streamer(streamer: Streamer) -> None:
        with Session() as session:
            session.add(streamer)
            session.commit()

    @staticmethod
    def update_streamer(streamer: Streamer) -> None:
        with Session() as session:
            session.merge(streamer)
            session.commit()

    @staticmethod
    def delete_streamer(id) -> None:
        with Session() as session:
            session.query(Streamer).filter(Streamer.id == id).delete()
            session.commit()
