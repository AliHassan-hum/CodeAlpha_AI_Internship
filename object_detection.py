import customtkinter as ctk
import cv2
from ultralytics import YOLO
import threading

# 1. Main Window Setup
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CodeAlpha - AI Object Detection")
app.geometry("500x350")

# Global variables detection ko control karne ke liye
is_detecting = False
cap = None

# YOLOv8 ka lightweight (nano) model load karein jo bohot fast chalta hai
# Pehli dafa run hone par yeh automatic internet se 6MB ka model download karega
model = YOLO("yolov8n.pt") 

# 2. Real-time Object Detection Logic
def detection_loop():
    global is_detecting, cap
    
    # Webcam start karne ke liye (0 matlub laptop ka default front camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        status_label.configure(text="Error: Could not open webcam.", text_color="red")
        is_detecting = False
        btn_toggle.configure(text="Start Camera & AI")
        return

    while is_detecting:
        ret, frame = cap.read()
        if not ret:
            break

        # AI Model se objects detect karna (Insaan, Chairs, Phones, etc.)
        results = model(frame, stream=True)

        # Har frame par boxes aur labels draw karna
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding box ke coordinates nikalna
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Class ka naam (Object Name) aur Confidence score nikalna
                cls = int(box.cls[0])
                label_name = model.names[cls]
                conf = round(float(box.conf[0]), 2)

                # Frame ke upar Green colored box aur naam likhna
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{label_name} {conf}", (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        # Video Output window dikhane ke liye
        cv2.imshow("CodeAlpha AI - Real-time Object Detection", frame)

        # Agar 'q' key dabayein ya OpenCV window close ho toh stop ho jaye
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Camera resource release karna aur windows band karna
    if cap:
        cap.release()
    cv2.destroyAllWindows()
    is_detecting = False
    
    # Main window ka status update karna
    app.after(0, lambda: status_label.configure(text="Camera Stopped", text_color="grey"))
    app.after(0, lambda: btn_toggle.configure(text="Start Camera & AI"))

# Button click handle karne ke liye function
def toggle_detection():
    global is_detecting
    
    if not is_detecting:
        is_detecting = True
        status_label.configure(text="AI Webcam Detection Active! (Press 'q' in video window to exit)", text_color="green")
        btn_toggle.configure(text="Stop Camera")
        
        # Threading use kar rahe hain taake hamara CustomTkinter GUI lag na kare (hang na ho)
        threading.Thread(target=detection_loop, daemon=True).start()
    else:
        is_detecting = False

# --- UI Layout ---
title_label = ctk.CTkLabel(app, text="Object Detection Tool", font=("Arial", 20, "bold"))
title_label.pack(pady=20)

desc_label = ctk.CTkLabel(
    app, 
    text="This application uses the advanced pre-trained YOLOv8 model\nto detect objects (like persons, phones, and laptops) in real-time.",
    font=("Arial", 12)
)
desc_label.pack(pady=10)

# Action Button
btn_toggle = ctk.CTkButton(app, text="Start Camera & AI", font=("Arial", 14, "bold"), fg_color="blue", command=toggle_detection)
btn_toggle.pack(pady=25)

# Status Label
status_label = ctk.CTkLabel(app, text="Camera Stopped", font=("Arial", 13, "italic"), text_color="grey")
status_label.pack(pady=10)

app.mainloop()