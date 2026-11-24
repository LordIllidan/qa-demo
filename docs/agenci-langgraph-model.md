# Agenty LangGraph: konfiguracja modelu

Dostawcę i nazwę modelu agenty biorą ze zmiennych środowiskowych. Klucza do modelu nie ma w repozytorium i nie podaje się go w poleceniu.

## Zmienne

| Zmienna | Znaczenie |
| --- | --- |
| `QA_DEMO_MODEL_DOSTAWCA` | dostawca modelu, na przykład `openai` albo `anthropic` |
| `QA_DEMO_MODEL_NAZWA` | nazwa modelu u tego dostawcy |

Obie są wymagane. Bez nich agent kończy się kodem 2 i wypisuje, jak je ustawić.

Klucz czyta pakiet integracji dostawcy ze swojej zmiennej:

| Dostawca | Zmienna z kluczem | Pakiet integracji |
| --- | --- | --- |
| `openai` | `OPENAI_API_KEY` | `langchain-openai`, w `requirements-langgraph.txt` |
| `anthropic` | `ANTHROPIC_API_KEY` | `langchain-anthropic`, w `requirements-langgraph.txt` |

## Ustawienie w PowerShell

Zmienne ustawione przez `$env:` obowiązują w bieżącym oknie PowerShell.

```powershell
$env:QA_DEMO_MODEL_DOSTAWCA = "openai"
$env:QA_DEMO_MODEL_NAZWA = "<nazwa modelu>"
$env:OPENAI_API_KEY = "<klucz>"
python -m agenci_langgraph zestaw
```

Dla dostawcy `anthropic`:

```powershell
$env:QA_DEMO_MODEL_DOSTAWCA = "anthropic"
$env:QA_DEMO_MODEL_NAZWA = "<nazwa modelu>"
$env:ANTHROPIC_API_KEY = "<klucz>"
```

Sprawdzenie, co jest ustawione, bez pokazywania klucza:

```powershell
$env:QA_DEMO_MODEL_DOSTAWCA
$env:QA_DEMO_MODEL_NAZWA
[bool]$env:OPENAI_API_KEY
```

## Usługa zgodna z interfejsem OpenAI

Dostawca `openai` łączy się także z usługą, która ma interfejs zgodny z OpenAI. Adres usługi podaje zmienna `OPENAI_BASE_URL`:

```powershell
$env:QA_DEMO_MODEL_DOSTAWCA = "openai"
$env:QA_DEMO_MODEL_NAZWA = "<nazwa modelu w tej usłudze>"
$env:OPENAI_BASE_URL = "<adres usługi zakończony na /v1>"
$env:OPENAI_API_KEY = "<klucz albo token tej usługi>"
```

## Inny dostawca

Model tworzy funkcja `init_chat_model` z pakietu `langchain`, więc wartość `QA_DEMO_MODEL_DOSTAWCA` to nazwa dostawcy, którą ta funkcja zna. Dostawca spoza tabeli wymaga doinstalowania swojego pakietu integracji. Jeśli pakietu brakuje, agent wypisze jego nazwę:

```text
Agent zatrzymany: brakuje pakietu integracji dla dostawcy „google_genai”: ... pip install langchain-google-genai
```

Wtedy:

```powershell
python -m pip install langchain-google-genai
```

Zmienną z kluczem dla takiego dostawcy podaje dokumentacja jego pakietu.

## Jak to działa

Kod: `agenci_langgraph/model.py`. Funkcja `model_ze_srodowiska` czyta obie zmienne i wywołuje `init_chat_model(nazwa, model_provider=dostawca)`. Dostawca i nazwa trafiają do protokołu agenta w wierszu `model:`. Klucz do protokołu nie trafia.

Model dostaje w każdym kroku dwie wiadomości: instrukcję (krótki opis pracy w grafie i treść skilla) oraz wejście (tekst oddany przez skrypty). Agenty nie ustawiają temperatury ani innych parametrów modelu.

## Bez klucza

Kroki grafu, zatrzymanie i wznowienie po decyzji można sprawdzić bez klucza, na modelu zastępczym w testach: [agenci-langgraph-testy.md](agenci-langgraph-testy.md).
