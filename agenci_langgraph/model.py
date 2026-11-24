"""Model dla agentów: dostawca i nazwa pochodzą ze zmiennych środowiskowych.

Klucza do modelu nie ma w repozytorium. Pakiet integracji dostawcy czyta go
ze swojej zmiennej środowiskowej, na przykład OPENAI_API_KEY.
"""

from __future__ import annotations

import os

from .wspolne import BladAgenta

ZMIENNA_DOSTAWCY = "QA_DEMO_MODEL_DOSTAWCA"
ZMIENNA_NAZWY = "QA_DEMO_MODEL_NAZWA"


def ustawienia_modelu() -> tuple:
    dostawca = os.environ.get(ZMIENNA_DOSTAWCY, "").strip()
    nazwa = os.environ.get(ZMIENNA_NAZWY, "").strip()
    if not dostawca or not nazwa:
        raise BladAgenta(
            f"ustaw zmienne środowiskowe {ZMIENNA_DOSTAWCY} i {ZMIENNA_NAZWY}, na przykład w PowerShell:\n"
            f'  $env:{ZMIENNA_DOSTAWCY} = "openai"\n'
            f'  $env:{ZMIENNA_NAZWY} = "<nazwa modelu>"\n'
            "Opis: docs/agenci-langgraph-model.md"
        )
    return dostawca, nazwa


def opis_modelu() -> str:
    dostawca, nazwa = ustawienia_modelu()
    return f"{dostawca}/{nazwa}"


def model_ze_srodowiska():
    dostawca, nazwa = ustawienia_modelu()
    from langchain.chat_models import init_chat_model

    try:
        return init_chat_model(nazwa, model_provider=dostawca)
    except ImportError as blad:
        raise BladAgenta(f"brakuje pakietu integracji dla dostawcy „{dostawca}”: {blad}") from blad
    except Exception as blad:
        raise BladAgenta(f"nie udało się przygotować modelu {dostawca}/{nazwa}: {blad}") from blad
