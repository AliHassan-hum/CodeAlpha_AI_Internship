import customtkinter as ctk
from deep_translator import GoogleTranslator

# Initialize the main application window
ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CodeAlpha - Language Translation Tool")
app.geometry("600x450")

# Supported Languages Dictionary
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Urdu": "ur",
    "Arabic": "ar",
    "Chinese": "zh-CN",
    "Hindi": "hi"
}

# Function to handle translation
def translate_text():
    try:
        # Get user input and selected languages
        input_text = text_input.get("1.0", "end-1c").strip()
        source_lang = LANGUAGES[source_lang_combo.get()]
        target_lang = LANGUAGES[target_lang_combo.get()]
        
        if not input_text:
            text_output.configure(state="normal")
            text_output.delete("1.0", "end")
            text_output.insert("1.0", "Please enter some text to translate.")
            text_output.configure(state="disabled")
            return

        # Perform the translation using the API background backend
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(input_text)
        
        # Display the result in the output box
        text_output.configure(state="normal")
        text_output.delete("1.0", "end")
        text_output.insert("1.0", translated)
        text_output.configure(state="disabled")
        
    except Exception as e:
        text_output.configure(state="normal")
        text_output.delete("1.0", "end")
        text_output.insert("1.0", f"Error: Ensure you are connected to the internet.\n({str(e)})")
        text_output.configure(state="disabled")

# --- UI Layout ---

# Title
title_label = ctk.CTkLabel(app, text="AI Language Translator", font=("Arial", 20, "bold"))
title_label.pack(pady=15)

# Dropdown Frame (Language Selection)
frame_lang = ctk.CTkFrame(app)
frame_lang.pack(pady=10, fill="x", padx=20)

label_from = ctk.CTkLabel(frame_lang, text="From:")
label_from.grid(row=0, column=0, padx=5, pady=5)

source_lang_combo = ctk.CTkComboBox(frame_lang, values=list(LANGUAGES.keys()))
source_lang_combo.set("English")
source_lang_combo.grid(row=0, column=1, padx=20, pady=5)

label_to = ctk.CTkLabel(frame_lang, text="To:")
label_to.grid(row=0, column=2, padx=5, pady=5)

target_lang_combo = ctk.CTkComboBox(frame_lang, values=list(LANGUAGES.keys()))
target_lang_combo.set("Spanish")
target_lang_combo.grid(row=0, column=3, padx=20, pady=5)

# Input Text Box
text_input = ctk.CTkTextbox(app, height=100, width=540)
text_input.pack(pady=10)
text_input.insert("1.0", "Type your text here...")

# Translate Button
btn_translate = ctk.CTkButton(app, text="Translate", command=translate_text, font=("Arial", 14, "bold"))
btn_translate.pack(pady=10)

# --- Output Text Box ---
text_output = ctk.CTkTextbox(app, height=100, width=540, state="disabled")
text_output.pack(pady=10)

# --- Run the app ---
app.mainloop()