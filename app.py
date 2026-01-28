"""
Poetry Muse - Main Application Entry Point
------------------------------------------
This file handles the Streamlit user interface, manages the session state,
connects the visual frontend to the PoetryBot logic, and handles
automated local data archiving.
"""

import streamlit as st
import matplotlib.pyplot as plt
import os
from datetime import datetime
from poetry_bot import PoetryBot

# Page Config
st.set_page_config(page_title="Poetry Muse", page_icon="🪶", layout="wide")

# Initialize Session State
if "history" not in st.session_state:
    st.session_state.history = []

# Initialize Bot (Default to mistral:latest if not set)
if "bot" not in st.session_state:
    st.session_state.bot = PoetryBot(model_name="mistral:latest")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/100/000000/poetry.png")
    st.header("⚙️ Muse Settings")
    
    # NEW: Model Selector (Fixes the 404 error)
    st.markdown("### 🧠 AI Model")
    model_input = st.text_input("Ollama Model Name", value="mistral:latest")
    
    if st.button("🔄 Update Model"):
        st.session_state.bot = PoetryBot(model_name=model_input)
        st.success(f"Switched to {model_input}")

    st.divider()

    # LO1: Style Selection (Simulated Fine-Tuning)
    style = st.selectbox(
        "Poetic Persona (Style)",
        ["Shakespearean", "Cyberpunk", "Haiku Master", "Surrealist"]
    )
    
    # Mode Selection
    mode = st.radio("Engine Mode", ["Ollama (Local AI)", "Mock Mode (Test)"])
    use_mock = True if "Mock" in mode else False
    
    st.info("💡 **Tip:** For local AI, ensure 'ollama serve' is running in your terminal.")

# --- MAIN INTERFACE ---
st.title("🪶 The Poetry Muse")
st.markdown(f"*Collaborative AI Poetry - Current Style: **{style}***")

# 1. Input Area
col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input("What is your inspiration today?", placeholder="e.g., A lost astronaut, the smell of rain...")

with col2:
    st.write("") # Spacer
    st.write("") 
    generate_btn = st.button("✨ Compose Poem", use_container_width=True, type="primary")

# 2. Generation Logic (Updated with Auto-Save)
if generate_btn and topic:
    with st.spinner(f"The Muse is composing a {style} piece..."):
        # A. Generate Text
        poem = st.session_state.bot.generate_poem(topic, style, use_mock)
        
        # B. Analyze Emotions
        emotions = st.session_state.bot.analyze_emotions(poem)
        
        # C. DATA MANAGEMENT: Auto-Save to 'poems/' folder
        # Create folder if it doesn't exist
        if not os.path.exists("poems"):
            os.makedirs("poems")
            
        # Create a unique filename based on time and topic
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_topic = topic.replace(" ", "_")
        filename = f"poems/{safe_topic}_{timestamp_str}.txt"
        
        # Write the file to your hard drive
        try:
            with open(filename, "w") as f:
                f.write(f"Topic: {topic}\nStyle: {style}\nDate: {datetime.now()}\n\n{poem}")
            # Show a small pop-up notification
            st.toast(f"✅ Archived to {filename}", icon="💾")
        except Exception as e:
            st.error(f"Could not save file: {e}")
        
        # D. Save to Session History (For the screen)
        timestamp = datetime.now().strftime("%H:%M")
        st.session_state.history.insert(0, {
            "topic": topic,
            "style": style,
            "text": poem,
            "emotions": emotions,
            "time": timestamp,
            "filepath": filename
        })

# 3. Display Feed
if st.session_state.history:
    for i, entry in enumerate(st.session_state.history):
        st.divider()
        c1, c2 = st.columns([2, 1])
        
        with c1:
            st.subheader(f"Untitled '{entry['topic']}'")
            st.caption(f"Style: {entry['style']} | Time: {entry['time']}")
            st.markdown(f"> *{entry['text'].replace(chr(10), '<br>') }*", unsafe_allow_html=True)
            
            # LO3: Voice Output
            if st.button("🔊 Read Aloud", key=f"speak_{i}"):
                st.session_state.bot.speak_poem(entry['text'])
                
            st.caption(f"📁 Local file: `{entry.get('filepath', 'Not saved')}`")
        
        with c2:
            # LO2: Emotion Visualization
            st.caption("Emotional Composition")
            fig, ax = plt.subplots(figsize=(3, 3))
            
            # Donut Chart
            labels = list(entry['emotions'].keys())
            sizes = list(entry['emotions'].values())
            colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99']
            
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, pctdistance=0.85)
            # Draw circle for donut
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig.gca().add_artist(centre_circle)
            ax.axis('equal')  
            
            st.pyplot(fig, use_container_width=False)
            
            # Manual Download Button
            st.download_button(
                "💾 Download Copy", 
                data=f"Topic: {entry['topic']}\nStyle: {entry['style']}\n\n{entry['text']}", 
                file_name=f"poem_{i}.txt",
                key=f"save_{i}"
            )

else:
    st.info("Enter a topic above to begin co-creating.")