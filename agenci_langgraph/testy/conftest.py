"""Wspólne części testów agentów LangGraph."""

from __future__ import annotations

import subprocess
import sys
import time
import urllib.request

import pytest

from agenci_langgraph.testy.model_zastepczy import ModelZastepczy
from agenci_langgraph.wspolne import KATALOG

PORTY_APLIKACJI = (8765, 8766)
CZEKANIE_NA_APLIKACJE_S = 10.0


def odpowiada(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/stan", timeout=1) as odpowiedz:
            return odpowiedz.status == 200
    except OSError:
        return False


@pytest.fixture(scope="session")
def aplikacja():
    """Buildy, na których skrypty uruchamiają testy. Działającej aplikacji fixture nie rusza;
    brakujące buildy uruchamia na czas testów."""
    procesy = [
        subprocess.Popen([sys.executable, "app/serwer.py", "--port", str(port)], cwd=KATALOG,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for port in PORTY_APLIKACJI if not odpowiada(port)
    ]
    koniec = time.monotonic() + CZEKANIE_NA_APLIKACJE_S
    while not all(odpowiada(port) for port in PORTY_APLIKACJI):
        if time.monotonic() > koniec:
            for proces in procesy:
                proces.terminate()
            pytest.fail("aplikacja demonstracyjna nie odpowiada; uruchom ją poleceniem: python app/serwer.py")
        time.sleep(0.1)
    yield PORTY_APLIKACJI
    for proces in procesy:
        proces.terminate()
        proces.wait(timeout=5)


@pytest.fixture
def model() -> ModelZastepczy:
    return ModelZastepczy()
