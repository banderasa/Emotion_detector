import streamlit as st
from model import predict_emotion
from database import create_table, insert_prediction, fetch_predictions

# Initialize database
create_table()

# Page configuration
st.set_page_config(
    page_title="Image Emotion Detector",
    page_icon="😀",
    layout="centered",
)

# Custom CSS
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .main-title {
            font-size: 2.2rem;
            font-weight: bold;
            color: #222;
            text-align: center;
            margin-bottom: 0.3em;
        }
        .sub-title {
            font-size: 1rem;
            color: #666;
            text-align: center;
            margin-bottom: 1.5em;
        }
        .stButton>button {
            background-color: #3c9d63;
            color: white;
            font-size: 1rem;
            border-radius: 10px;
            height: 3em;
            width: 10em;
        }
        .stButton>button:hover {
            background-color: #358a58;
        }
        .prediction-card {
            background-color: #f7e7c4;  /* sand tint */
            border-radius: 12px;
            padding: 20px;
            margin-top: 25px;
            text-align: center;
            color: #333;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
        }
        .prediction-card h4 {
            font-size: 1.4rem;
            margin-bottom: 0.5em;
        }
        .prediction-card p {
            font-size: 1.1rem;
            margin-top: 0.2em;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">Facial Emotion Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Upload a face image to analyse emotion and confidence level.</div>', unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("📸 Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="🖼 Uploaded Image", use_container_width=True)
    st.write("🔍 Processing image...")

    try:
        prediction, confidence = predict_emotion(uploaded_file)

        # Confidence as percentage (0–100)
        confidence_percentage = confidence * 100 if confidence <= 1 else confidence

        # Prediction display card
        st.markdown(f"""
        <div class="prediction-card">
            <h4>Detected Emotion: <strong>{prediction}</strong></h4>
            <p>Confidence: <strong>{confidence_percentage:.2f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.progress(int(confidence_percentage))

        # Save to database
        filename = getattr(uploaded_file, "name", "unknown_file")
        insert_prediction(filename, prediction, confidence_percentage)

    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

# Saved predictions section
st.subheader("📊 Saved Predictions")

data = fetch_predictions()

if data:
    st.table(data)
else:
    st.info("No predictions saved yet.")
