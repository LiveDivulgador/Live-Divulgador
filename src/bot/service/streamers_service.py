from src.bot.database.entities.streamer import Streamer
from src.bot.database.engine import Session


class StreamersService:
    @staticmethod
    def get_streamers() -> list[Streamer]:
        with Session() as session:
            query = session.query(Streamer).all()

        return query

    @staticmethod
    def get_streamer(twitch_id) -> Streamer:
        with Session() as session:
            response = (
                session.query(Streamer)
                .filter(Streamer.twitch_id == twitch_id)
                .all()
            )

        return response

    @classmethod
    def create_streamer(cls, streamer: Streamer) -> None:

        # TODO: validar se já existe no banco de dados antes da criação
        with Session() as session:
            existing_streamer = cls.get_streamer(streamer.twitch_id)

            if existing_streamer != []:
                raise Exception("Streamer already exists")

            session.add(streamer)
            session.commit()

    @staticmethod
    def update_streamer(streamer: Streamer) -> None:
        with Session() as session:
            session.merge(streamer)
            session.commit()

    @staticmethod
    def delete_streamer(twitch_id) -> None:
        with Session() as session:
            session.query(Streamer).filter(
                Streamer.twitch_id == twitch_id
            ).delete()
            session.commit()
