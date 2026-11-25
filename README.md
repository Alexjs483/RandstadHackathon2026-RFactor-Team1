# HACKATHON - R-FACTOR

Hackathon organized by Randstad Digital & ITS TTF - Team #1

*Thursday November 26th 2026 # Randstad BOX Milano (Italy)*

## Set-Up

### Create the Python Virtual Environment (only once)

Make sure you have python installed:
```bash
$ sudo apt update && sudo apt install -y python3-venv
```

Create Python Virtual Environment inside your repo:
```bash
$ sudo apt update && sudo apt install -y python3-venv
$ python3 -m venv .venv
```

From inside the Virtual Environment:
```bash
$ source .venv/bin/activate
(.env) $ pip install openai
(.env) $ pip install google-genai
(.env) $ pip install python-dotenv
```
Install Streamlit and Pydantic
```bash
(.env) $ pip install streamlit pydantic
```

Create a file `.env` containing your API:
`GEMINI_API_KEY="your-api-key"`




## Usage
### Source the Python Virtual Environment (everytime)
```bash
$ source .venv/bin/activate
```

Run the app using the CLI command:
```bash
(.env) $ streamlit run app_demo.py
```
The app will be available at http://localhost:8501

### 1) Smart Meeting Assistant
Use the data in the json: `data/meeting_assistant_data.json` --> already in `MEETING_SIMULATI`

```py
# 3. Dati simulati (da espandere in un file data.json)
MEETING_SIMULATI = [
    {
        "titolo": "Allineamento Strategico Q4",
        "organizzatore": "Marco Rossi (CEO)",
        "partecipanti_tuo_team": ["Tu (Senior Dev)", "Luca (Junior Dev)"],
        "agenda": "Definizione priorità tecnologiche e budget 2027"
    },
    {
        "titolo": "Sync settimanale fornitore logging",
        "organizzatore": "Account Manager Esterno",
        "partecipanti_tuo_team": ["Tu (Senior Dev)", "Sara (Tech Lead)", "Luca (Junior Dev)"],
        "agenda": "Aggiornamento ticket minori e stato avanzamento"
    }
]
```


### 2) Smart Office Planner
Use the data in the json: `data/office_planner_data.json`
```py
class SuggerimentoGiorno(BaseModel):
    giorno: str
    modalita: Literal["UFFICIO", "REMOTO"]
    scrivania_consigliata: str
    colleghi_chiave_presenti: list[str]
    motivazione: str
```

### 3) AI Personal Assistant
Use the data in the json: `data/personal_assistant_data.json`
```py
class AnalisiEmail(BaseModel):
    id_email: str
    categoria: Literal["CRITICA_VIP", "RICHIESTA_MEETING", "SCADENZA_SOLLECITO", "TASK_OPERATIVO", "NEWSLETTER"]
    priorita: Literal["ALTA", "MEDIA", "BASSA"]
    azione_suggerita: str
    task_estratti: list[str]
    bozza_risposta_o_invito: str
    ```
