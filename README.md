# 🪶 The Poetry Muse
*A Local AI Collaborative Poetry Generator*

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Ollama](https://img.shields.io/badge/AI-Ollama_Local-orange)
![Streamlit](https://img.shields.io/badge/Interface-Streamlit-red)

## 📖 Project Overview
The **Poetry Muse** is an AI-powered creative writing assistant that runs 100% locally on your machine. It demonstrates advanced "Lightweight Fine-Tuning" via cue engineering to adopt distinct poetic personas, from Shakespearean Bards to Cyberpunk AIs.

## ✨ Key Features (Learning Outcomes)

### 🧠 LO1: Lightweight Fine-Tuning & Cue Engineering
Instead of generic responses, the bot utilizes **System Prompts** to enforce strict stylistic constraints:
* **Shakespearean:** Archaic English, iambic pentameter.
* **Cyberpunk:** Gritty, neon-soaked free verse.
* **Haiku Master:** Strict 5-7-5 syllable structure.

### 🎨 LO2: Multimodal Content Generation
The application goes beyond text by analyzing the **emotional composition** of every poem (Joy, Melancholy, Chaos, Serenity) and generating a dynamic **Matplotlib visualization** (Donut Chart) in real-time.

### 🔊 LO3: Text-to-Speech Integration
Includes a native offline text-to-speech engine to perform the poems aloud, allowing users to experience the rhythm and cadence of the generated verses.

## 🛠️ Tech Stack
* **Interface:** Streamlit (Web UI)
* **AI Engine:** Ollama (running `mistral:latest` or `llama3`)
* **Visualization:** Matplotlib
* **Audio:** Native System Voice (Mac `say` command) / pyttsx3

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure you have [Ollama](https://ollama.com/) installed and running.
```bash
ollama serve
ollama pull mistral  # or llama3
```
### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```
### 3. Run the Application
```bash
streamlit run app.py
```
### 4. Project Structure
```
poetry_muse_project/
├── app.py              # Main User Interface (Streamlit)
├── poetry_bot.py       # Logic: AI connection, Audio, & Analysis
├── chatbot_base.py     # Base Class (Inheritance requirement)
├── requirements.txt    # Project dependencies
└── poems/              # Saved poem exports
```
### 5.Usage Guide
Select a Persona: Choose a style from the sidebar (e.g., "Cyberpunk").

## 🔮 Future Improvements
* **More Styles:** Plan to add Limerick and Sonnet formats.
* **PDF Export:** Will allow users to download poems as designed PDFs.
* **Temperature Control:** Adding a slider to adjust the "creativity" of the AI.

Enter a Topic: Type a subject (e.g., "The rain in neon city").

Compose: Click "Compose Poem" to generate text and visuals.

Listen: Click "Read Aloud" to hear the poem.

Save: Download the poem as a text file for your portfolio.
