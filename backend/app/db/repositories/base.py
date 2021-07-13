from databases import Database


class BaseRepository:
    """BaseRepository

    データベースコネクションへの参照を保持するだけのクラス

    """

    def __init__(self, db: Database) -> None:
        self.db = db
