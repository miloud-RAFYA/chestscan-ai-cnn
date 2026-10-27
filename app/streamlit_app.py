"""
ChestScan AI — Interface Streamlit
Direction artistique : Modern Health-Tech SaaS (Clair / Lumineux)

Contrat API inchangé :
    GET  {API_URL}/health   -> {"model_available": bool, ...}
    POST {API_URL}/predict  -> champ multipart « file »
                               {"prediction", "pneumonia_probability", "threshold"}
"""

import html
import os
import uuid
from pathlib import Path

import requests
import streamlit as st


# =========================================================
# 1. Configuration de la page et de la session
# =========================================================

st.set_page_config(
    page_title="ChestScan AI | Imagerie intelligente",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.getenv("API_URL", "http://api:8000").rstrip("/")

if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4().hex[:8].upper()


# =========================================================
# 2. Design CSS — Direction « Modern Health-Tech »
# =========================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg-app: #F3F6F9; /* Gris-bleu très clair, pas de noir */
    --bg-card: #FFFFFF;
    --text-main: #101828;
    --text-muted: #475467;
    --primary: #0066FF; /* Bleu médical vif */
    --primary-hover: #0052CC;
    --primary-light: #EFF4FF;
    --border: #EAECF0;
    
    --success-bg: #ECFDF3;
    --success-text: #027A48;
    --success-border: #A6F4C5;
    
    --warn-bg: #FFFAEB;
    --warn-text: #B54708;
    --warn-border: #FEDF89;
    
    --error-bg: #FEF3F2;
    --error-text: #B42318;
    
    --font-display: 'Plus Jakarta Sans', sans-serif;
    --font-body: 'Inter', sans-serif;
    
    --shadow-sm: 0 1px 2px 0 rgba(16, 24, 40, 0.05);
    --shadow-md: 0 4px 8px -2px rgba(16, 24, 40, 0.05), 0 2px 4px -2px rgba(16, 24, 40, 0.05);
    --shadow-lg: 0 12px 24px -4px rgba(16, 24, 40, 0.04);
    
    --radius-md: 10px;
    --radius-lg: 16px;
    --radius-full: 9999px;
}

/* Global Reset */
.stApp {
    background-color: var(--bg-app);
    color: var(--text-main);
    font-family: var(--font-body);
}

header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    max-width: 1160px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Navbar moderne (Flottante) */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: var(--bg-card);
    padding: 1rem 1.5rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    margin-bottom: 2.5rem;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.nav-logo-icon {
    width: 36px;
    height: 36px;
    background: var(--primary-light);
    color: var(--primary);
    border-radius: var(--radius-md);
    display: flex;
    align-items: center;
    justify-content: center;
}

.nav-title {
    font-family: var(--font-display);
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-main);
    letter-spacing: -0.02em;
}

.nav-status {
    display: flex;
    gap: 0.75rem;
}

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.75rem;
    border-radius: var(--radius-full);
    font-size: 0.75rem;
    font-weight: 600;
    font-family: var(--font-display);
    letter-spacing: 0.02em;
}

.status-badge.ok {
    background: var(--success-bg);
    color: var(--success-text);
    border: 1px solid var(--success-border);
}
.status-badge.bad {
    background: var(--error-bg);
    color: var(--error-text);
    border: 1px solid #FECDCA;
}

.dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}
.status-badge.ok .dot { background: var(--success-text); }
.status-badge.bad .dot { background: var(--error-text); }

/* Hero Section */
.hero {
    text-align: center;
    margin-bottom: 3rem;
}

.hero h1 {
    font-family: var(--font-display);
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 800;
    color: var(--text-main);
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.1rem;
    color: var(--text-muted);
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}

.hero .blue-text {
    color: var(--primary);
}

/* Section Cards (Conteneurs principaux) */
.module-card {
    background: var(--bg-card);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
    height: 100%;
}

.module-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border);
}

.module-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: var(--primary-light);
    color: var(--primary);
    border-radius: 8px;
}

.module-title {
    font-family: var(--font-display);
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-main);
}

/* Zone d'upload Streamlit Customisée */
[data-testid="stFileUploader"] section {
    background: #F9FAFB;
    border: 2px dashed #D0D5DD;
    border-radius: var(--radius-md);
    padding: 2rem 1rem;
    transition: all 0.2s ease;
}
[data-testid="stFileUploader"] section:hover {
    border-color: var(--primary);
    background: var(--primary-light);
}
[data-testid="stFileUploader"] label p {
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-main);
}
[data-testid="stFileUploader"] small {
    color: var(--text-muted);
}
[data-testid="stFileUploader"] button {
    border-radius: 8px;
    border: 1px solid #D0D5DD;
    background: white;
    color: var(--text-main);
    font-weight: 600;
    box-shadow: var(--shadow-sm);
}

/* Aperçu Image & Meta */
[data-testid="stImage"] img {
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    box-shadow: var(--shadow-sm);
}

.file-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #F9FAFB;
    padding: 0.75rem 1rem;
    border-radius: 8px;
    margin-top: 1rem;
    border: 1px solid var(--border);
    font-size: 0.85rem;
}
.file-meta strong { color: var(--text-main); font-weight: 600; }
.file-meta span { color: var(--text-muted); }

/* Boutons principaux */
.stButton > button,
[data-testid="stBaseButton-primary"] {
    width: 100%;
    min-height: 3rem;
    border-radius: var(--radius-md);
    border: none;
    background: var(--primary);
    color: #FFFFFF;
    font-family: var(--font-display);
    font-weight: 700;
    font-size: 1rem;
    box-shadow: 0 4px 12px rgba(0, 102, 255, 0.25);
    transition: all 0.2s ease;
}
.stButton > button:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: var(--primary-hover);
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 102, 255, 0.3);
}
.stButton > button:disabled,
[data-testid="stBaseButton-primary"]:disabled {
    background: #E5E7EB;
    color: #9CA3AF;
    box-shadow: none;
    transform: none;
}

/* Design du résultat */
.result-container {
    text-align: center;
    padding: 1.5rem 0;
}

.verdict-badge {
    display: inline-block;
    padding: 0.5rem 1.25rem;
    border-radius: var(--radius-full);
    font-family: var(--font-display);
    font-weight: 800;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    border: 2px solid transparent;
}
.verdict-badge.normal {
    background: var(--success-bg);
    color: var(--success-text);
    border-color: var(--success-border);
}
.verdict-badge.pneumonia {
    background: var(--warn-bg);
    color: var(--warn-text);
    border-color: var(--warn-border);
}
.verdict-badge.unknown {
    background: #F1F5F9;
    color: #475569;
    border-color: #E2E8F0;
}

.metrics-row {
    display: flex;
    justify-content: space-around;
    background: #F9FAFB;
    padding: 1rem;
    border-radius: var(--radius-md);
    border: 1px solid var(--border);
    margin-bottom: 1.5rem;
}
.metric-box { text-align: center; }
.metric-label { font-size: 0.75rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }
.metric-value { font-family: var(--font-display); font-size: 1.25rem; font-weight: 700; color: var(--text-main); margin-top: 0.25rem; }

/* Barre de progression moderne */
.progress-wrapper {
    position: relative;
    padding-top: 10px;
    margin-bottom: 2rem;
}
.progress-track {
    height: 8px;
    background: #E5E7EB;
    border-radius: var(--radius-full);
    overflow: hidden;
    position: relative;
}
.progress-fill {
    height: 100%;
    border-radius: var(--radius-full);
    transition: width 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
.fill-normal { background: var(--success-text); }
.fill-pneumonia { background: var(--warn-text); }

.threshold-marker {
    position: absolute;
    top: 5px;
    width: 2px;
    height: 18px;
    background: var(--text-main);
    border-radius: 2px;
    transform: translateX(-1px);
    z-index: 10;
}
.threshold-label {
    position: absolute;
    top: -12px;
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--text-main);
    transform: translateX(-50%);
}

/* État vide & attente */
.empty-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 3rem 1rem;
    background: #F9FAFB;
    border-radius: var(--radius-md);
    border: 1px dashed #D0D5DD;
    color: var(--text-muted);
}
.empty-box svg { color: #9CA3AF; margin-bottom: 1rem; }
.empty-box p { margin: 0; font-size: 0.95rem; line-height: 1.5; }

/* Alertes & Notices */
.alert-box {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    border-radius: var(--radius-md);
    font-size: 0.85rem;
    line-height: 1.5;
    margin: 1rem 0;
}
.alert-box.info { background: var(--primary-light); color: #175CD3; border: 1px solid #B2DDFF; }
.alert-box.warning { background: var(--warn-bg); color: var(--warn-text); border: 1px solid var(--warn-border); }
.alert-box.error { background: var(--error-bg); color: var(--error-text); border: 1px solid #FECDCA; }
.alert-box svg { flex-shrink: 0; margin-top: 2px; }

/* Specs / Tech stack */
.tech-stack {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1rem;
    margin-top: 3rem;
    padding-top: 2rem;
    border-top: 1px solid var(--border);
}
.tech-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    background: #FFFFFF;
    border: 1px solid var(--border);
    border-radius: var(--radius-full);
    font-size: 0.8rem;
    font-weight: 600;
    color: var(--text-muted);
    box-shadow: var(--shadow-sm);
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid var(--border);
    border-radius: 8px;
    background: white;
    box-shadow: var(--shadow-sm);
}
[data-testid="stExpander"] summary {
    font-weight: 600;
    color: var(--text-main);
}

@media (max-width: 768px) {
    .block-container { padding: 1rem; }
    .hero h1 { font-size: 1.75rem; }
    .module-card { margin-bottom: 1rem; }
}
</style>
"""

# Icônes SVG inline pour le style moderne
SVG_LOGO = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>"""
SVG_UPLOAD = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>"""
SVG_CHIP = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>"""
SVG_INFO = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>"""
SVG_WARN = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>"""


# =========================================================
# 3. Helpers HTML sécurisés
# =========================================================

def esc(value) -> str:
    return html.escape(str(value), quote=True)


def render(markup: str) -> None:
    cleaned = "\n".join(line.strip() for line in markup.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def render_navbar(api_ok: bool, model_ok: bool) -> None:
    api_cls = "ok" if api_ok else "bad"
    api_txt = "API Connectée" if api_ok else "API Hors-ligne"
    
    if not api_ok:
        mod_cls, mod_txt = "bad", "Modèle Indisponible"
    elif model_ok:
        mod_cls, mod_txt = "ok", "Modèle Prêt"
    else:
        mod_cls, mod_txt = "bad", "Modèle Non Chargé"

    render(
        f"""
        <div class="navbar">
            <div class="nav-brand">
                <div class="nav-logo-icon">{SVG_LOGO}</div>
                <div class="nav-title">ChestScan AI</div>
            </div>
            <div class="nav-status">
                <span class="status-badge {api_cls}"><i class="dot"></i>{api_txt}</span>
                <span class="status-badge {mod_cls}"><i class="dot"></i>{mod_txt}</span>
            </div>
        </div>
        """
    )


def render_hero() -> None:
    render(
        """
        <div class="hero">
            <h1>Analyse radiologique assistée par <span class="blue-text">Intelligence Artificielle</span></h1>
            <p>Importez une radiographie thoracique pour obtenir une prédiction instantanée de classification saine ou pathologique (pneumonie), propulsée par un réseau de neurones convolutifs.</p>
        </div>
        """
    )


def module_open(title: str, icon_svg: str) -> None:
    render(
        f"""
        <div class="module-card">
            <div class="module-header">
                <div class="module-icon">{icon_svg}</div>
                <div class="module-title">{esc(title)}</div>
            </div>
        """
    )


def module_close() -> None:
    render("</div>")


def alert(kind: str, text: str) -> None:
    icon = SVG_WARN if kind in ["warning", "error"] else SVG_INFO
    render(f'<div class="alert-box {kind}">{icon} <div>{esc(text)}</div></div>')


def render_empty_state(is_result_side: bool = False) -> None:
    if is_result_side:
        render(
            f"""
            <div class="empty-box" style="padding: 4rem 1rem;">
                {SVG_CHIP}
                <p>En attente d'image.<br>Importez un fichier et lancez l'analyse.</p>
            </div>
            """
        )


def render_result_ui(result: dict, probability: float, threshold: float, prediction: str) -> None:
    badge_cls = "unknown"
    fill_cls = "fill-normal"
    
    if prediction == "NORMAL":
        badge_cls = "normal"
        fill_cls = "fill-normal"
    elif prediction == "PNEUMONIA":
        badge_cls = "pneumonia"
        fill_cls = "fill-pneumonia"

    fill_pct = probability * 100
    mark_pct = min(max(threshold, 0.0), 1.0) * 100

    render(
        f"""
        <div class="result-container">
            <div class="verdict-badge {badge_cls}">{esc(prediction)}</div>
            
            <div class="progress-wrapper">
                <div class="threshold-label" style="left:{mark_pct:.1f}%">Seuil ({threshold:.2f})</div>
                <div class="progress-track">
                    <div class="progress-fill {fill_cls}" style="width:{fill_pct:.1f}%"></div>
                    <div class="threshold-marker" style="left:{mark_pct:.1f}%"></div>
                </div>
            </div>
            
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-label">Probabilité PNEUMONIA</div>
                    <div class="metric-value">{probability:.1%}</div>
                </div>
                <div class="metric-box">
                    <div class="metric-label">Session ID</div>
                    <div class="metric-value" style="font-size:1rem; margin-top:0.4rem;">{esc(st.session_state['session_id'])}</div>
                </div>
            </div>
        </div>
        """
    )
    
    alert("warning", "Note : Cet outil est un prototype expérimental SaaS. Il ne remplace en aucun cas un diagnostic médical certifié.")
    
    with st.expander("Voir la réponse brute de l'API JSON"):
        st.json(result)


def render_tech_stack() -> None:
    render(
        """
        <div class="tech-stack">
            <div class="tech-pill">⚙️ FastAPI (Backend)</div>
            <div class="tech-pill">🧠 MobileNetV2 (Modèle)</div>
            <div class="tech-pill">🎨 Streamlit (Frontend)</div>
            <div class="tech-pill">🐳 Docker (Déploiement)</div>
        </div>
        """
    )


# =========================================================
# 4. Appels API
# =========================================================

def check_health() -> tuple[bool, bool]:
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        response.raise_for_status()
        health = response.json()
        return True, bool(health.get("model_available"))
    except (requests.RequestException, ValueError):
        return False, False


def run_prediction(uploaded_file) -> dict:
    key = f"{uploaded_file.name}:{uploaded_file.size}"
    try:
        response = requests.post(
            f"{API_URL}/predict",
            files={
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "image/jpeg",
                )
            },
            timeout=60,
        )
    except requests.RequestException as exc:
        return {"key": key, "error": f"Erreur réseau avec l'API : {exc}"}

    if not response.ok:
        try:
            detail = response.json().get("detail", "Erreur serveur.")
        except (ValueError, AttributeError):
            detail = response.text[:200]
        return {"key": key, "error": f"HTTP {response.status_code} : {detail}"}

    try:
        result = response.json()
    except ValueError:
        return {"key": key, "error": "Le JSON renvoyé par l'API est invalide."}

    return {
        "key": key,
        "result": result,
        "prediction": str(result.get("prediction", "UNKNOWN")).upper(),
        "probability": max(0.0, min(1.0, float(result.get("pneumonia_probability", 0)))),
        "threshold": float(result.get("threshold", 0.5)),
    }


# =========================================================
# 5. Interface Principale
# =========================================================

st.markdown(CSS, unsafe_allow_html=True)

api_available, model_available = check_health()
render_navbar(api_available, model_available)

if not api_available:
    alert("error", f"Impossible de joindre le serveur FastAPI ({API_URL}). Vérifiez que l'API est lancée.")

render_hero()

col1, col2 = st.columns([1, 1], gap="large")

# ---------- COLONNE GAUCHE : IMPORTATION ----------
with col1:
    module_open("Source Radiographique", SVG_UPLOAD)
    
    uploaded_file = st.file_uploader(
        "Déposez votre radiographie ici (JPG, PNG)",
        type=["jpg", "jpeg", "png", "bmp"],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.image(uploaded_file.getvalue(), use_container_width=True)
        ext = Path(uploaded_file.name).suffix.upper().replace(".", "")
        render(
            f"""
            <div class="file-meta">
                <div><span>Fichier :</span> <strong>{esc(uploaded_file.name)}</strong></div>
                <div><strong>{ext}</strong> • {uploaded_file.size / 1024:.0f} KB</div>
            </div>
            """
        )
    module_close()

# ---------- COLONNE DROITE : PRÉDICTION ----------
with col2:
    module_open("Analyse & Résultats", SVG_CHIP)
    
    st.button(
        "Lancer l'analyse du modèle",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_file is None or not api_available or not model_available),
        key="analyze_btn"
    )

    if st.session_state.get("analyze_btn") and uploaded_file is not None:
        with st.spinner("Inférence en cours via l'API..."):
            st.session_state["analysis"] = run_prediction(uploaded_file)

    analysis = st.session_state.get("analysis")
    current_key = f"{uploaded_file.name}:{uploaded_file.size}" if uploaded_file else None

    if uploaded_file is None or analysis is None or analysis.get("key") != current_key:
        render_empty_state(is_result_side=True)
    elif "error" in analysis:
        alert("error", analysis["error"])
    else:
        render_result_ui(
            analysis["result"],
            analysis["probability"],
            analysis["threshold"],
            analysis["prediction"],
        )
        
    module_close()

render_tech_stack()