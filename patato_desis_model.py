import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import cv2

# Load the saved model
# MODEL_PATH = "saved_model/potato_disease_model"
# model = tf.keras.models.load_model(MODEL_PATH)

# Define class names (replace with your actual dataset class names)
class_names = ["Healthy", "Early Blight", "Late Blight"]  # Example classes

def preprocess_image(image_path):
    """
    Preprocess the input image for prediction.
    Resizes, normalizes, and adds batch dimension.
    """
    IMAGE_SIZE = 256  # Same as the model input size
    image = cv2.imread(image_path)  # Read the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert to RGB
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE))  # Resize to 256x256
    image = image / 255.0  # Normalize pixel values to [0, 1]
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

def predict_disease(image_path):
    """
    Predict the disease class of the leaf using the saved model.
    """
    image = preprocess_image(image_path)  # Preprocess the image
    predictions = model.predict(image)  # Get predictions
    predicted_class = class_names[np.argmax(predictions)]  # Get the class name
    confidence = np.max(predictions)  # Get the confidence score
    return predicted_class, confidence

def upload_image():
    """
    Open a file dialog to select an image, and display the prediction result.
    """
    global uploaded_image, img_label, result_label
    
    # Open file dialog to select an image
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if not file_path:
        return  # Do nothing if no file is selected
    
    # Display the selected image in the GUI
    image = Image.open(file_path)
    image = image.resize((300, 300))  # Resize for display
    uploaded_image = ImageTk.PhotoImage(image)
    img_label.configure(image=uploaded_image)
    img_label.image = uploaded_image
    
    # Get prediction
    predicted_class, confidence = predict_disease(file_path)
    
    # Display the result
    result_label.configure(
        text=f"Predicted Disease: {predicted_class}\nConfidence: {confidence*100:.2f}%"
    )

# Create the GUI application
app = tk.Tk()
app.title("Leaf Disease Prediction")
app.geometry("600x600")
app.resizable(False, False)

# Heading label
heading = Label(app, text="Leaf Disease Prediction System", font=("Arial", 20, "bold"))
heading.pack(pady=10)

# Image display label
img_label = Label(app)
img_label.pack(pady=10)

# Button to upload image
upload_btn = Button(app, text="Upload Leaf Image", command=upload_image, font=("Arial", 14), bg="green", fg="white")
upload_btn.pack(pady=20)

# Label to display prediction results
result_label = Label(app, text="", font=("Arial", 16), fg="blue")
result_label.pack(pady=10)

# Run the application
app.mainloop()
