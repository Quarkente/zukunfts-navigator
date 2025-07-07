import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Seitenkonfiguration
st.set_page_config(
    page_title="🎯 Zukunfts-Navigator", 
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS für besseres Design
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    .quiz-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
    }
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .step-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialisierung der Session State
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'player_data' not in st.session_state:
    st.session_state.player_data = {}
if 'quiz_completed' not in st.session_state:
    st.session_state.quiz_completed = False

def show_progress():
    """Zeigt Fortschrittsbalken"""
    steps = ["Start", "Persönliche Daten", "Kompetenzen", "Motivation", "Umgebung", "Zukunftswerte", "Persönlichkeit", "Ergebnisse"]
    progress = st.session_state.current_step / (len(steps) - 1)
    
    st.progress(progress)
    st.write(f"**Schritt {st.session_state.current_step} von {len(steps)-1}:** {steps[st.session_state.current_step]}")
    st.markdown("---")

def step_0_welcome():
    """Willkommensseite"""
    st.markdown("""
    <div class="step-header">
        <h1>🚀 Zukunfts-Navigator</h1>
        <h3>Entdecke deinen Weg nach der Sekundarschule!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="quiz-card">
        <h2 style="text-align: center;">🎯 Willkommen!</h2>
        
        Du stehst vor einer wichtigen Entscheidung:
        
        🔧 **Berufsausbildung (Lehre)** - Praktisch lernen und arbeiten
        
        📚 **Weiterführende Schule (FMS/Gymi)** - Theoretisches Wissen vertiefen
        
        Dieser interaktive Navigator hilft dir herauszufinden, welcher Weg am besten zu dir passt!
        
        ⏱️ **Dauer:** ca. 10 Minuten  
        🎁 **Ergebnis:** Personalisierte Empfehlung mit konkreten nächsten Schritten
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🌟 So funktioniert's:")
        st.write("1. Beantworte ehrlich alle Fragen")
        st.write("2. Erhalte deine personalisierte Auswertung")
        st.write("3. Bekomme konkrete nächste Schritte")
        
        if st.button("🚀 Los geht's!", type="primary", use_container_width=True):
            st.session_state.current_step = 1
            st.experimental_rerun()

def step_1_personal_data():
    """Persönliche Daten erfassen"""
    st.markdown('<div class="step-header"><h2>👤 Wer bist du?</h2></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("🙋 Dein Name:", placeholder="z.B. Anna")
        klasse = st.text_input("🎓 Deine Klasse:", placeholder="z.B. 3. Sek A")
    
    with col2:
        alter = st.number_input("🎂 Dein Alter:", min_value=13, max_value=18, value=15)
        schule = st.text_input("🏫 Deine Schule:", placeholder="z.B. Sekundarschule Muster")
    
    st.markdown("### 🎯 Deine aktuelle Situation:")
    situation = st.selectbox(
        "Wie fühlst du dich bezüglich deiner Zukunft?",
        ["😰 Sehr unsicher", "😟 Etwas unsicher", "😐 Neutral", "😊 Zuversichtlich", "🤩 Sehr optimistisch"]
    )
    
    if st.button("Weiter ➡️", type="primary"):
        if name:  # Mindestens Name erforderlich
            st.session_state.player_data.update({
                'name': name or 'Anonym',
                'klasse': klasse,
                'alter': alter,
                'schule': schule,
                'situation': situation
            })
            st.session_state.current_step = 2
            st.experimental_rerun()
        else:
            st.error("Bitte gib mindestens deinen Namen an!")

def step_2_competencies():
    """Kompetenzen bewerten"""
    st.markdown('<div class="step-header"><h2>⚡ Deine Superkräfte entdecken!</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 📊 Bewerte deine Fähigkeiten ehrlich von 1-5:")
    st.info("1 = Schwach, 2 = Ausbaufähig, 3 = Okay, 4 = Gut, 5 = Stark")
    
    competencies = {
        "🗣️ Deutsch sprechen & verstehen": "Diskutieren, präsentieren, Texte verstehen",
        "✍️ Texte schreiben": "Aufsätze, E-Mails, kreativ schreiben", 
        "🧮 Mathematik & Logik": "Rechnen, Probleme lösen, logisch denken",
        "🔧 Praktisches Arbeiten": "Mit den Händen arbeiten, basteln, reparieren",
        "💻 Technik verstehen": "Computer, Apps, technische Geräte",
        "🤝 Teamwork & Kommunikation": "Mit anderen arbeiten, Konflikte lösen",
        "🎨 Kreativität": "Gestalten, eigene Ideen entwickeln",
        "🎯 Selbstständigkeit": "Ohne Anleitung arbeiten, Verantwortung übernehmen"
    }
    
    ratings = {}
    
    for comp, desc in competencies.items():
        with st.container():
            st.markdown(f"**{comp}**")
            st.caption(desc)
            ratings[comp] = st.slider(
                f"Bewertung für {comp}",
                1, 5, 3,
                key=f"comp_{comp}",
                label_visibility="collapsed"
            )
            st.markdown("---")
    
    # Visualisierung der aktuellen Bewertungen
    if any(ratings.values()):
        st.markdown("### 📈 Dein aktuelles Profil:")
        
        # Radar Chart
        categories = list(ratings.keys())
        values = list(ratings.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Deine Kompetenzen',
            line_color='rgb(102, 126, 234)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 5]
                )),
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Weiter ➡️", type="primary"):
        st.session_state.player_data['kompetenzen'] = ratings
        st.session_state.current_step = 3
        st.experimental_rerun()

def step_3_motivation():
    """Motivation erfassen"""
    st.markdown('<div class="step-header"><h2>💪 Was motiviert dich?</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Wähle alle Aussagen aus, die auf dich zutreffen:")
    
    motivations = {
        "🔨 Ich arbeite gerne mit meinen Händen": "praktisch",
        "🧠 Ich mag komplexe Probleme und Theorien": "theoretisch", 
        "🤝 Ich helfe gerne anderen Menschen": "sozial",
        "🎨 Ich bin kreativ und gestalte gerne": "kreativ",
        "🔬 Ich entdecke gerne Neues": "forschend",
        "👑 Ich übernehme gerne Verantwortung": "führend",
        "📋 Ich brauche klare Strukturen": "strukturiert",
        "🌟 Ich liebe Abwechslung": "abwechslungsreich"
    }
    
    selected_motivations = []
    
    for motivation, key in motivations.items():
        if st.checkbox(motivation, key=f"mot_{key}"):
            selected_motivations.append(key)
    
    st.markdown("### 🎮 Mini-Challenge:")
    st.markdown("**Stell dir vor, du hast einen freien Samstag. Was machst du?**")
    
    weekend_choice = st.radio(
        "Wähle eine Option:",
        [
            "📚 Lesen oder online lernen",
            "🔨 Etwas reparieren oder basteln", 
            "🎨 Kreativ werden (zeichnen, musik, etc.)",
            "📱 Freunde anrufen oder treffen"
        ]
    )
    
    if st.button("Weiter ➡️", type="primary"):
        st.session_state.player_data['motivationen'] = selected_motivations
        st.session_state.player_data['weekend_choice'] = weekend_choice
        st.session_state.current_step = 4
        st.experimental_rerun()

def step_4_environment():
    """Arbeitsumgebung wählen"""
    st.markdown('<div class="step-header"><h2>🏢 Deine ideale Arbeitsumgebung</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 In welcher Umgebung fühlst du dich am wohlsten?")
    
    environments = {
        "🔧 Werkstatt/Labor": {
            "desc": "Praktisch arbeiten, experimentieren, bauen",
            "key": "werkstatt"
        },
        "💼 Büro/Schule": {
            "desc": "Planen, analysieren, lernen, schreiben", 
            "key": "buero"
        },
        "👥 Mit Menschen": {
            "desc": "Beraten, unterrichten, verkaufen, helfen",
            "key": "menschen"
        },
        "🌱 Draussen/Natur": {
            "desc": "Im Freien arbeiten, mit Tieren/Pflanzen",
            "key": "natur"
        }
    }
    
    # Visuelle Auswahl mit Karten
    cols = st.columns(2)
    selected_env = None
    
    for i, (env, data) in enumerate(environments.items()):
        with cols[i % 2]:
            if st.button(
                f"{env}\n\n{data['desc']}", 
                key=f"env_{data['key']}",
                use_container_width=True
            ):
                selected_env = data['key']
    
    # Fallback: Radio Buttons
    if not selected_env:
        st.markdown("**Oder wähle hier:**")
        env_choice = st.radio(
            "Arbeitsumgebung:",
            list(environments.keys()),
            key="env_radio"
        )
        if env_choice:
            selected_env = environments[env_choice]['key']
    
    if st.button("Weiter ➡️", type="primary"):
        if selected_env or 'env_radio' in st.session_state:
            final_env = selected_env or environments[st.session_state.env_radio]['key']
            st.session_state.player_data['arbeitsumgebung'] = final_env
            st.session_state.current_step = 5
            st.experimental_rerun()
        else:
            st.error("Bitte wähle eine Arbeitsumgebung!")

def step_5_future_values():
    """Zukunftswerte bewerten"""
    st.markdown('<div class="step-header"><h2>🌟 Was ist dir wichtig?</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 💼 Wie wichtig sind dir diese Aspekte im späteren Beruf?")
    st.info("1 = Unwichtig, 2 = Wenig wichtig, 3 = Neutral, 4 = Wichtig, 5 = Sehr wichtig")
    
    values = {
        "💰 Gutes Einkommen": "Finanziell abgesichert sein",
        "⚖️ Work-Life-Balance": "Zeit für Familie und Hobbys", 
        "❤️ Sinnvolle Arbeit": "Etwas Wichtiges für die Gesellschaft tun",
        "📈 Karrierechancen": "Aufstiegsmöglichkeiten haben",
        "🔒 Jobsicherheit": "Sicherer Arbeitsplatz",
        "🎓 Weiterbildung": "Immer weiter lernen können"
    }
    
    value_ratings = {}
    
    for value, desc in values.items():
        with st.container():
            st.markdown(f"**{value}**")
            st.caption(desc)
            value_ratings[value] = st.slider(
                f"Wichtigkeit: {value}",
                1, 5, 3,
                key=f"val_{value}",
                label_visibility="collapsed"
            )
            st.markdown("---")
    
    # Balkendiagramm der Werte
    if any(value_ratings.values()):
        st.markdown("### 📊 Deine Prioritäten:")
        
        df = pd.DataFrame({
            'Aspekt': list(value_ratings.keys()),
            'Wichtigkeit': list(value_ratings.values())
        })
        
        fig = px.bar(
            df, 
            x='Wichtigkeit', 
            y='Aspekt',
            orientation='h',
            color='Wichtigkeit',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    if st.button("Weiter ➡️", type="primary"):
        st.session_state.player_data['zukunftswerte'] = value_ratings
        st.session_state.current_step = 6
        st.experimental_rerun()

def step_6_personality():
    """Persönlichkeits-Assessment"""
    st.markdown('<div class="step-header"><h2>🎮 Persönlichkeits-Challenge!</h2></div>', unsafe_allow_html=True)
    
    st.markdown("### 🎯 Zwei schnelle Situationen:")
    
    # Situation 1
    st.markdown("**🎯 Du sollst eine Präsentation halten. Wie gehst du vor?**")
    presentation_style = st.radio(
        "Dein Ansatz:",
        [
            "📋 Detailliert planen und vorbereiten",
            "💡 Spontan und frei sprechen", 
            "🤝 Mit anderen zusammen vorbereiten",
            "🎨 Kreativ und visuell gestalten"
        ]
    )
    
    st.markdown("---")
    
    # Situation 2
    st.markdown("**🔍 Du stösst auf ein Problem. Was ist dein erster Impuls?**")
    problem_solving = st.radio(
        "Deine Reaktion:",
        [
            "🔧 Sofort praktisch ausprobieren",
            "📚 Erst recherchieren und verstehen",
            "👥 Andere um Hilfe fragen", 
            "💡 Kreative Lösung erfinden"
        ]
    )
    
    st.markdown("---")
    
    # Reflexion
    st.markdown("### 💭 Kurze Reflexion:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        strength = st.text_area(
            "🌟 Was ist deine grösste Stärke?", 
            placeholder="z.B. Ich bin sehr hilfsbereit..."
        )
    
    with col2:
        development = st.text_area(
            "🎯 Woran möchtest du arbeiten?",
            placeholder="z.B. Ich möchte selbstbewusster werden..."
        )
    
    if st.button("🎯 Auswertung erstellen!", type="primary"):
        if strength and development:
            st.session_state.player_data.update({
                'presentation_style': presentation_style,
                'problem_solving': problem_solving,
                'strength': strength,
                'development': development
            })
            st.session_state.quiz_completed = True
            st.session_state.current_step = 7
            st.experimental_rerun()
        else:
            st.error("Bitte fülle beide Reflexionsfelder aus!")

def calculate_recommendation():
    """Berechnet die Empfehlung"""
    data = st.session_state.player_data
    kompetenzen = data.get('kompetenzen', {})
    
    # Berechne Scores
    practical_keys = ['🔧 Praktisches Arbeiten', '💻 Technik verstehen', '🎨 Kreativität']
    theoretical_keys = ['🗣️ Deutsch sprechen & verstehen', '✍️ Texte schreiben', '🧮 Mathematik & Logik']
    
    practical_score = sum(kompetenzen.get(key, 0) for key in practical_keys) / len(practical_keys)
    theoretical_score = sum(kompetenzen.get(key, 0) for key in theoretical_keys) / len(theoretical_keys)
    
    # Motivationsanalyse
    motivations = data.get('motivationen', [])
    practical_motivation = any(mot in motivations for mot in ['praktisch', 'kreativ'])
    theoretical_motivation = any(mot in motivations for mot in ['theoretisch', 'forschend'])
    
    # Umgebungsanalyse
    environment = data.get('arbeitsumgebung', '')
    practical_environment = environment in ['werkstatt', 'natur']
    
    # Entscheidungslogik
    if (practical_score > theoretical_score + 0.5) or (practical_motivation and practical_environment):
        return 'berufsausbildung'
    elif (theoretical_score > practical_score + 0.5) or (theoretical_motivation and not practical_environment):
        return 'weiterführende_schule'
    else:
        return 'beide_wege'

def step_7_results():
    """Ergebnisse anzeigen"""
    data = st.session_state.player_data
    name = data.get('name', 'Zukunftsheld')
    
    st.markdown(f'<div class="step-header"><h1>🎉 Deine Auswertung, {name}!</h1></div>', unsafe_allow_html=True)
    
    # Berechne Empfehlung
    recommendation = calculate_recommendation()
    
    # Stärken-Schwächen-Analyse
    kompetenzen = data.get('kompetenzen', {})
    strengths = [k for k, v in kompetenzen.items() if v >= 4]
    improvements = [k for k, v in kompetenzen.items() if v <= 2]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="result-card">
        <h3>💪 Deine Stärken</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if strengths:
            for strength in strengths:
                st.success(f"🌟 {strength}")
        else:
            st.info("🌟 Ausgewogene Kompetenzen in allen Bereichen!")
    
    with col2:
        st.markdown("""
        <div class="result-card">
        <h3>🎯 Entwicklungsfelder</h3>
        </div>
        """, unsafe_allow_html=True)
        
        if improvements:
            for improvement in improvements:
                st.warning(f"📈 {improvement}")
        else:
            st.info("📈 Keine grösseren Schwächen erkannt!")
    
    # Hauptempfehlung
    st.markdown("## 🚀 Deine persönliche Wegempfehlung")
    
    if recommendation == 'berufsausbildung':
        st.markdown("""
        <div class="result-card">
        <h2>🔧 BERUFSAUSBILDUNG (EFZ/EBA)</h2>
        <h4>✨ Du bist ein praktischer Typ!</h4>
        <p>Deine Stärken liegen im hands-on Arbeiten. Eine Lehre könnte perfekt zu dir passen!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Deine nächsten Schritte:")
        steps = [
            "Informiere dich über verschiedene Lehrberufe",
            "Organisiere 2-3 Schnupperlehren",
            "Verbessere deine schulischen Kompetenzen gezielt",
            "Sprich mit Berufsberater:innen und Praktiker:innen"
        ]
        
    elif recommendation == 'weiterführende_schule':
        st.markdown("""
        <div class="result-card">
        <h2>📚 WEITERFÜHRENDE SCHULE (FMS/GYMNASIUM)</h2>
        <h4>✨ Du bist ein theoretischer Denker!</h4>
        <p>Du liebst komplexe Probleme und Wissen. FMS oder Gymnasium könnten ideal sein!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Deine nächsten Schritte:")
        steps = [
            "Informiere dich über Aufnahmeprüfungen",
            "Erstelle einen strukturierten Lernplan",
            "Besuche Informationsveranstaltungen",
            "Überlege dir mögliche Studienrichtungen"
        ]
        
    else:
        st.markdown("""
        <div class="result-card">
        <h2>⚖️ BEIDE WEGE STEHEN DIR OFFEN</h2>
        <h4>✨ Du bist vielseitig begabt!</h4>
        <p>Sowohl Lehre als auch Schule passen zu dir. Lass dich von deinen Interessen leiten!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📋 Deine nächsten Schritte:")
        steps = [
            "Mache sowohl Schnupperlehren als auch Schulbesuche",
            "Führe Gespräche mit Berufsberater:innen",
            "Reflektiere deine langfristigen Ziele",
            "Entscheide nach deinem Bauchgefühl"
        ]
    
    for i, step in enumerate(steps, 1):
        st.write(f"{i}️⃣ {step}")
    
    # Persönliche Notizen
    st.markdown("### 💬 Deine persönlichen Notizen:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"🌟 **Deine Stärke:** {data.get('strength', 'Nicht angegeben')}")
    
    with col2:
        st.info(f"🎯 **Entwicklungsfeld:** {data.get('development', 'Nicht angegeben')}")
    
    # Export-Funktionen
    st.markdown("---")
    st.markdown("### 📤 Ergebnisse teilen")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📄 PDF erstellen", type="secondary"):
            st.info("PDF-Export: Speichere diese Seite als PDF über deinen Browser (Strg+P)")
    
    with col2:
        # JSON Download
        result_data = {
            **data,
            'empfehlung': recommendation,
            'datum': datetime.now().isoformat(),
            'staerken': strengths,
            'entwicklungsfelder': improvements
        }
        
        st.download_button(
            "💾 Daten herunterladen",
            data=json.dumps(result_data, ensure_ascii=False, indent=2),
            file_name=f"zukunftsnavigator_{name}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
    
    with col3:
        if st.button("🔄 Neuer Test", type="primary"):
            # Reset alles
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()
    
    # Feedback
    st.markdown("---")
    st.markdown("### 💬 Feedback")
    feedback = st.text_area("Wie war der Test für dich? (Optional)")
    if st.button("Feedback senden") and feedback:
        st.success("Danke für dein Feedback! 🙏")

# Hauptanwendung
def main():
    # Sidebar für Navigation
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.write(f"Aktueller Schritt: {st.session_state.current_step}")
        
        if st.session_state.current_step > 0:
            if st.button("⬅️ Zurück"):
                if st.session_state.current_step > 0:
                    st.session_state.current_step -= 1
                    st.experimental_rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ Info")
        st.write("**Dauer:** ca. 10 Minuten")
        st.write("**Ziel:** Wegempfehlung finden")
        st.write("**Ergebnis:** Personalisierte Analyse")
        
        if st.session_state.current_step > 1:
            st.markdown("### 📊 Deine Daten")
            data = st.session_state.player_data
            if 'name' in data:
                st.write(f"👤 {data['name']}")
            if 'klasse' in data:
                st.write(f"🎓 {data['klasse']}")
    
    # Fortschritt anzeigen (außer bei Start und Ergebnis)
    if 0 < st.session_state.current_step < 7:
        show_progress()
    
    # Schritt-Router
    steps = [
        step_0_welcome,
        step_1_personal_data,
        step_2_competencies, 
        step_3_motivation,
        step_4_environment,
        step_5_future_values,
        step_6_personality,
        step_7_results
    ]
    
    if st.session_state.current_step < len(steps):
        steps[st.session_state.current_step]()

if __name__ == "__main__":
    main()
    