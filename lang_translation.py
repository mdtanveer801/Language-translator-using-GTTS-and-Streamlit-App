import streamlit as st
import pandas as pd
import os
from gtts import gTTS
import base64
from translate import Translator  # Using 'translate' package as an alternative to 'mtranslate'

# Load language dataset
df = pd.read_csv(r'C:\Users\mdtan\VS code\language.csv')
df.dropna(inplace=True)
lang = df['name'].to_list()
langlist = tuple(lang)
langcode = df['iso'].to_list()

# Create a dictionary of language names and their codes
lang_array = {lang[i]: langcode[i] for i in range(len(langcode))}

# Supported languages for gTTS
speech_langs = {
    "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali", "ca": "Catalan",
    "cs": "Czech", "da": "Danish", "de": "German", "el": "Greek", "en": "English",
    "es": "Spanish", "fi": "Finnish", "fr": "French", "hi": "Hindi", "it": "Italian",
    "ja": "Japanese", "ko": "Korean", "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali",
    "nl": "Dutch", "pl": "Polish", "pt": "Portuguese", "ro": "Romanian", "ru": "Russian",
    "si": "Sinhala", "sv": "Swedish", "ta": "Tamil", "te": "Telugu", "tr": "Turkish",
    "uk": "Ukrainian", "ur": "Urdu", "vi": "Vietnamese", "zh-CN": "Chinese"
}

# Streamlit App Title
st.title("🌐 Language Translation App")

# User input
inputtext = st.text_area("Enter text to translate:", height=100)

# Sidebar for language selection
choice = st.sidebar.radio('Select Language', langlist)

# Function to download audio
def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    bin_str = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>'
    return href

# Display columns
c1, c2 = st.columns([4, 3])

if len(inputtext) > 0:
    try:
        # Translation using 'translate' package
        translator = Translator(to_lang=lang_array[choice])
        output = translator.translate(inputtext)
        
        with c1:
            st.text_area("Translated Text", output, height=200)
        
        # Text-to-Speech
        selected_lang_code = lang_array[choice]
        if selected_lang_code in speech_langs:
            with c2:
                audio_file_path = f"temp_{selected_lang_code}.mp3"
                tts = gTTS(text=output, lang=selected_lang_code, slow=False)
                tts.save(audio_file_path)
                
                # Play audio
                audio_file = open(audio_file_path, 'rb')
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format='audio/mp3')
                
                # Download link
                st.markdown(get_binary_file_downloader_html(audio_file_path, 'Audio File'), unsafe_allow_html=True)
                
                # Clean up
                os.remove(audio_file_path)

    except Exception as e:
        st.error(f"An error occurred: {e}")
