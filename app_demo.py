import os
import json
from typing import Literal
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
import streamlit as st

# Caricamento variabili d'ambiente
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Inizializzazione client AI con chiave API e timeout
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=15000)
)

# Schema Output Strutturato
class AnalisiMeeting(BaseModel):
    titolo: str
    score_utilita: int = Field(description="Punteggio da 1 a 100")
    azione: Literal["ACCETTA", "DELEGA", "DECLINA"]
    delegato_suggerito: str = Field(description="Nome collega se azione è DELEGA, altrimenti 'Nessuno'")
    motivazione: str = Field(description="Spiegazione sintetica basata sui driver decisionali")
    bozza_email: str = Field(description="Email di risposta garbata pronta all'invio")

# 3. Dati simulati (domani li espandete in un file data.json)
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

# Funzione di analisi con AI
def analizza_con_ai(meeting: dict, livello_autonomia: str) -> AnalisiMeeting:
    prompt = f"""
    Sei un Smart Meeting Assistant aziendale. Livello autonomia impostato dall'utente: {livello_autonomia}.
    Analizza questo invito a riunione considerando:
    - Fattore gerarchico (CEO/stakeholder critici = alta priorità)
    - Ridondanza del team (se c'è già il Tech Lead o troppe persone dello stesso team, valuta delega o declino)
    - Opportunità di crescita per profili Junior su riunioni operative a basso rischio.
    
    Dati riunione: {json.dumps(meeting, ensure_ascii=False)}
    """
    # Fallback automatico sui modelli funzionanti
    for modello in ["gemini-3.1-flash-lite", "gemma-4-31b-it", "gemini-3.8-flash"]:
        try:
            response = client.models.generate_content(
                model=modello,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=AnalisiMeeting,
                    temperature=0.2
                )
            )
            return AnalisiMeeting.model_validate_json(response.text)
        except Exception:
            continue
    raise RuntimeError("Nessun modello AI disponibile al momento.")

# Interfaccia Utente (Streamlit)
st.set_page_config(page_title="AI Prototype Demo", layout="wide")
st.title("Smart Meeting Assistant — MVP")

# Sidebar per parametri di governance/autonomia
with st.sidebar:
    st.header("Parametri Agente")
    autonomia = st.select_slider(
        "Livello di autonomia",
        options=["Solo Suggerimento", "Bozza Automatica", "Azione Autonoma"]
    )
    st.info("Architettura modulare: UI (Streamlit) -> Orchestrator -> LLM Provider")

if st.button("Analizza Inviti in Calendario", type="primary"):
    for m in MEETING_SIMULATI:
        with st.spinner(f"Analisi di '{m['titolo']}'..."):
            res = analizza_con_ai(m, autonomia)
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.subheader(res.titolo)
            st.metric("Score Utilità", f"{res.score_utilita}/100")
            st.write(f"**Azione:** `{res.azione}`")
            if res.delegato_suggerito != "Nessuno":
                st.write(f"**Delega a:** {res.delegato_suggerito}")
        with col2:
            st.write(f"**Motivazione AI:** {res.motivazione}")
            st.text_area("Bozza Email Generata", value=res.bozza_email, height=100, key=res.titolo)
        st.divider()
