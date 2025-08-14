import streamlit as st
from streamlit.components.v1 import html
from models.predict import model  # Reuse your existing model
from schema.user_input import UserInput  # Reuse your Pydantic model

# ======== HTML/CSS Customization ========
st.set_page_config(layout="wide")

# Custom CSS injection
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Form elements */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        border: 2px solid #4a90e2 !important;
        border-radius: 8px !important;
    }
    
    /* Button */
    .stButton>button {
        background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%) !important;
        color: white !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# HTML Title
html("""
<div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2c3e50; font-size: 2.5em;">Insurance Premium Predictor</h1>
    <p style="color: #7f8c8d; font-size: 1.2em;">AI-powered risk assessment with your existing model</p>
</div>
""")

# ======== Interactive Form ========
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        weight = st.number_input("Weight (kg)", min_value=30.0, value=70.0)
        height = st.number_input("Height (m)", min_value=1.0, max_value=2.5, value=1.75, step=0.01)
    
    with col2:
        income = st.number_input("Income (LPA)", min_value=1.0, value=10.0)
        smoker = st.checkbox("Smoker")
        city = st.text_input("City", "Mumbai")
        occupation = st.selectbox("Occupation", [
            "private_job", "business_owner", "student", "retired"
        ])
    
    submitted = st.form_submit_button("Predict Premium")

# ======== Prediction Logic ========
if submitted:
    try:
        # Reuse your existing Pydantic model for validation
        user_data = UserInput(
            age=age,
            weight=weight,
            height=height,
            income_lpa=income,
            smoker=smoker,
            city=city,
            occupation=occupation
        )
        
        # Reuse your existing predict function
        prediction = model.predict([[user_data.bmi, user_data.age_group, 
                                   user_data.lifestyle_risk, user_data.city_tier,
                                   user_data.income_lpa, user_data.occupation]])
        
        # Display results with HTML
        html(f"""
        <div style="
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        ">
            <h3 style="color: #2c3e50;">Result</h3>
            <p style="font-size: 1.2em;">
                Predicted Premium Category: <strong style="color: #4facfe;">{prediction[0]}</strong>
            </p>
            <p>BMI: {user_data.bmi:.1f} | Lifestyle Risk: {user_data.lifestyle_risk}</p>
        </div>
        """)
    
    except Exception as e:
        st.error(f"Error: {str(e)}")