from typing import Callable, Type

from app.db.repositories.base import BaseRepository
from databases import Database
from fastapi import Depends
from starlette.requests import Request


def get_database(request: Request) -> Database:
    """get_database

        FastAPIのステートを返却する関数

        Args:
            request (Request): リクエストを受け取る

        Returns:
            Database: FastAPI ステートのdbを返却する
    """
    return request.app.state._db


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    """get_repository

        Repo_type パラメータを持ち get_repo という別の関数を返します

        Args:
            Repo_type (Type[BaseRepository]): Type[BaseRepository]を受け取る

        Returns:
            Callable: get_repoを返却
    """
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        """get_repo

        db パラメータがありget_database関数で返される

        Args:
            db (Database = Depends(get_database)): db パラメータを受け取る

        Returns:
            Type[BaseRepository]: get_database関数に返却
        """
        return Repo_type(db)
    return get_repo
