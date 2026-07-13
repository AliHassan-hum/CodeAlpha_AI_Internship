import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(page_title="AI Language Translator", page_icon="🌎", layout="centered")
st.title("🌎 AI Language Translator Tool")
st.write("Type your text, select target language, and translate instantly!")

user_text = st.text_area("Enter Text to Translate:", placeholder="Type something here...")

languages = {
    "Urdu": "ur", "English": "en", "Spanish": "es", "French": "fr",
    "Arabic": "ar", "German": "de", "Hindi": "hi"
}
selected_lang = st.selectbox("Select Target Language:", list(languages.keys()))

if st.button("Translate ✨"):
    if user_text.strip() == "":
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Translating..."):
            try:
                target_code = languages[selected_lang]
                translated = GoogleTranslator(source='auto', target=target_code).translate(user_text)
                st.success("Translation Completed!")
                st.subheader("Result:")
                st.write(translated)
            except Exception as e:
                st.error(f"Error: {e}")