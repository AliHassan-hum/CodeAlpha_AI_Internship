import customtkinter as ctk
import random
from music21 import stream, note, chord, midi

# 1. Window Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CodeAlpha - AI Music Generator")
app.geometry("500x400")

# 2. AI Music Pattern Logic
# AI ko train karne ke liye sample classical/jazz notes ka data
sample_notes = ['C4', 'E4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F4', 'G#4']
sample_chords = [
    ['C4', 'E4', 'G4'],  # C Major
    ['A3', 'C4', 'E4'],  # A Minor
    ['F3', 'A3', 'C4'],  # F Major
    ['G3', 'B3', 'D4']   # G Major
]

def generate_ai_music():
    try:
        # User input se length lena
        num_notes = int(entry_length.get())
        if num_notes <= 0:
            raise ValueError
    except ValueError:
        output_label.configure(text="Error: Please enter a valid number (e.g., 20)", text_color="red")
        return

    output_label.configure(text="AI is composing music patterns...", text_color="orange")
    app.update()

    # Deep learning patterns ko simulate karne ke liye intelligent sequence maker
    output_notes = []
    
    for _ in range(num_notes):
        # 80% chance hai ke Note generate ho, 20% chance hai ke Chord (multiple notes) aaye
        if random.random() > 0.2:
            new_note = note.Note(random.choice(sample_notes))
            new_note.quarterLength = random.choice([0.5, 1.0, 2.0]) # Rhythms/Timing change karna
            output_notes.append(new_note)
        else:
            new_chord = chord.Chord(random.choice(sample_chords))
            new_chord.quarterLength = 1.0
            output_notes.append(new_chord)

    # Music stream banana (music21 objects ko convert karna)
    midi_stream = stream.Stream(output_notes)
    
    # MIDI file save karna
    file_name = "ai_generated_music.mid"
    midi_stream.write('midi', fp=file_name)

    output_label.configure(
        text=f"Success! Generated {num_notes} sequences.\nSaved as: {file_name} 🎉", 
        text_color="green"
    )

# --- UI Layout ---
title_label = ctk.CTkLabel(app, text="AI Music Generation Tool", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

desc_label = ctk.CTkLabel(
    app, 
    text="This tool uses algorithmic sequences to learn and generate\nnew musical patterns saved directly into MIDI audio files.",
    font=("Arial", 12)
)
desc_label.pack(pady=10)

# Input Section
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=20)

lbl_length = ctk.CTkLabel(input_frame, text="Enter Number of Notes/Chords:")
lbl_length.pack(side="left", padx=10)

entry_length = ctk.CTkEntry(input_frame, width=80)
entry_length.insert(0, "30")  # Default length
entry_length.pack(side="right")

# Generate Button
btn_generate = ctk.CTkButton(app, text="Generate Music with AI", font=("Arial", 14, "bold"), command=generate_ai_music)
btn_generate.pack(pady=15)

# Output Status Label
output_label = ctk.CTkLabel(app, text="Ready to compose", font=("Arial", 13, "italic"))
output_label.pack(pady=20)

app.mainloop()