import customtkinter as ctk
import difflib  # Built-in library, iske liye kuch install nahi karna padega

# 1. CustomTkinter Window Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

app = ctk.CTk()
app.title("CodeAlpha - FAQ Chatbot")
app.geometry("600x500")

# 2. FAQs Dataset [cite: 27, 28]
faq_data = {
    "what is codealpha?": "CodeAlpha is a software development company dedicated to driving innovation and excellence across emerging technologies.",
    "how many tasks do i need to complete?": "To be eligible for the certificate, you must complete a minimum of two or three tasks.",
    "where do i submit my tasks?": "A submission form will be shared in your WhatsApp group. You are required to submit completed tasks only through that form.",
    "what is the github repository naming convention?": "You should upload your complete source code to GitHub in a repository named: CodeAlpha_ProjectName.",
    "when will i get my certificate?": "Certificates are issued after successfully submitting your tasks and completing the instructions like sharing your status on LinkedIn."
}

faq_questions = list(faq_data.keys())

# 3. Intelligent Matching Logic [cite: 30]
def get_bot_response():
    user_query = user_input.get().strip().lower()
    
    if not user_query:
        return

    # User ka text chat area mein show karein
    chat_box.configure(state="normal")
    chat_box.insert("end", f"You: {user_input.get()}\n")
    
    # NLP String Matching: Yeh user ke sawal ko hamare FAQs se match karta hai (thodi spelling mistake bhi sambhal leta hai)
    matches = difflib.get_close_matches(user_query, faq_questions, n=1, cutoff=0.4)
    
    if matches:
        matched_question = matches[0]
        bot_reply = faq_data[matched_question]
    else:
        bot_reply = "I'm sorry, I couldn't find an exact match for your question. Please try asking differently (e.g., 'what is codealpha?' or 'where do i submit my tasks?')."

    # Bot ka reply chat area mein show karein [cite: 31]
    chat_box.insert("end", f"Bot: {bot_reply}\n\n")
    chat_box.configure(state="disabled")
    
    # Auto scroll to bottom
    chat_box.yview("end")
    user_input.delete(0, "end")

# --- UI Layout --- [cite: 32]
title_label = ctk.CTkLabel(app, text="AI FAQ Chatbot", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

chat_box = ctk.CTkTextbox(app, height=350, width=540, state="disabled", wrap="word")
chat_box.pack(pady=10)

# Welcome Message
chat_box.configure(state="normal")
chat_box.insert("end", "Bot: Hello! Ask me anything about your CodeAlpha Internship.\n\n")
chat_box.configure(state="disabled")

# Input Section
input_frame = ctk.CTkFrame(app, fg_color="transparent")
input_frame.pack(pady=10, fill="x", padx=30)

user_input = ctk.CTkEntry(input_frame, placeholder_text="Ask a question...", width=400)
user_input.pack(side="left", padx=(0, 10))
user_input.bind("<Return>", lambda event: get_bot_response())

btn_send = ctk.CTkButton(input_frame, text="Send", width=80, command=get_bot_response)
btn_send.pack(side="right")

app.mainloop()