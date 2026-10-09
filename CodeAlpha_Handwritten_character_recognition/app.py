from flask import Flask, render_template, request
import tensorflow as tf
from PIL import Image
import numpy as np
import base64
import io


app = Flask(__name__)

# ==========================================================
# LOAD CNN MODEL
# ==========================================================

MODEL_PATH = "handwritten_digit_cnn.keras"

model = tf.keras.models.load_model(MODEL_PATH)

print("CNN model loaded successfully!")


# ==========================================================
# IMAGE PREPROCESSING
# ==========================================================

def preprocess_image(image):

    # Convert to grayscale
    image = image.convert("L")

    # Convert to numpy
    img_array = np.array(image)

    # If background is white, invert it
    if np.mean(img_array) > 127:
        img_array = 255 - img_array

    # Detect digit pixels
    coords = np.column_stack(
        np.where(img_array > 30)
    )

    # Crop digit
    if coords.size > 0:

        y_min, x_min = coords.min(axis=0)
        y_max, x_max = coords.max(axis=0)

        img_array = img_array[
            y_min:y_max + 1,
            x_min:x_max + 1
        ]

    # Convert back to PIL
    digit_image = Image.fromarray(img_array)

    # Keep aspect ratio
    digit_image.thumbnail((20, 20))

    # Create 28x28 MNIST canvas
    canvas = Image.new(
        "L",
        (28, 28),
        0
    )

    # Center digit
    x = (28 - digit_image.width) // 2
    y = (28 - digit_image.height) // 2

    canvas.paste(
        digit_image,
        (x, y)
    )

    # Normalize
    final_array = np.array(
        canvas
    ).astype("float32") / 255.0

    # Add batch dimension
    final_array = np.expand_dims(
        final_array,
        axis=0
    )

    # Add channel dimension
    final_array = np.expand_dims(
        final_array,
        axis=-1
    )

    return final_array


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# PREDICT UPLOADED IMAGE
# ==========================================================

@app.route("/predict", methods=["POST"])
def predict():

    if "image" not in request.files:

        return render_template(
            "index.html",
            error="Please upload an image."
        )

    file = request.files["image"]

    if file.filename == "":

        return render_template(
            "index.html",
            error="Please select an image."
        )

    try:

        image = Image.open(file)

        processed_image = preprocess_image(
            image
        )

        prediction = model.predict(
            processed_image,
            verbose=0
        )

        predicted_digit = int(
            np.argmax(prediction[0])
        )

        confidence = float(
            np.max(prediction[0]) * 100
        )

        return render_template(
            "index.html",
            prediction=predicted_digit,
            confidence=f"{confidence:.2f}",
            method="Uploaded Image"
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=f"Error processing image: {str(e)}"
        )


# ==========================================================
# PREDICT DRAWING
# ==========================================================

@app.route("/predict-drawing", methods=["POST"])
def predict_drawing():

    try:

        # Get drawing data from browser
        drawing_data = request.form.get(
            "drawing"
        )

        if not drawing_data:

            return render_template(
                "index.html",
                error="Please draw a digit first."
            )

        # Remove base64 header
        drawing_data = drawing_data.split(
            ","
        )[1]

        # Decode image
        image_bytes = base64.b64decode(
            drawing_data
        )

        image = Image.open(
            io.BytesIO(image_bytes)
        )

        # Preprocess
        processed_image = preprocess_image(
            image
        )

        # Predict
        prediction = model.predict(
            processed_image,
            verbose=0
        )

        predicted_digit = int(
            np.argmax(prediction[0])
        )

        confidence = float(
            np.max(prediction[0]) * 100
        )

        return render_template(
            "index.html",
            prediction=predicted_digit,
            confidence=f"{confidence:.2f}",
            method="Drawing Canvas"
        )

    except Exception as e:

        return render_template(
            "index.html",
            error=f"Error processing drawing: {str(e)}"
        )


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )