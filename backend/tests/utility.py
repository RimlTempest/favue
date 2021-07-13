import time
from functools import wraps
from typing import Any, Callable, Type

import psycopg2

# PostgreSQLとの接続が確率されるまで待機する
# 最後まで確率できなかった際は例外をスロー


def do_with_retry(
    catching_exc: Type[Exception],
    reraised_exc: Type[Exception],
    error_msg: str
) -> Callable:  # pragma: no cover
    def outer_wrapper(call: Callable) -> Callable:
        @wraps(call)
        # 接続の確率に失敗するたびインターバルを少しずつ伸ばし最大で30秒と少しの間試行し続ける
        def inner_wrapper(*args: Any, **kwargs: Any) -> Any:
            delay = 0.001
            for i in range(15):
                try:
                    return call(*args, **kwargs)
                except catching_exc:
                    time.sleep(delay)
                    delay *= 2
            else:  # pragma: no cover
                raise reraised_exc(error_msg)

        return inner_wrapper

    return outer_wrapper


@do_with_retry(psycopg2.Error, RuntimeError, "Cannot start postgres server")
def ping_postgres(dsn: str) -> None:  # pragma: no cover
    conn = psycopg2.connect(dsn)
    cur = conn.cursor()
    cur.execute('select pid, state from pg_stat_activity;')
    cur.close()
    conn.close()
