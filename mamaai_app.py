# mamaai_app.py
import streamlit as st
import pandas as pd
import numpy as np
from gtts import gTTS
import pygame
import io
import warnings
warnings.filterwarnings('ignore')

# Pregnancy Risk Prediction Model
class PregnancyRiskPredictor:
    def __init__(self):
        self.high_risk_symptoms = [
            'vaginal bleeding', 'severe abdominal pain', 'high fever',
            'no fetal movement', 'blurred vision', 'severe headache',
            'convulsions', 'water breaking early'
        ]
        
        self.medium_risk_symptoms = [
            'mild headache', 'swelling', 'dizziness', 'nausea',
            'back pain', 'fatigue', 'frequent urination'
        ]
    
    def predict_risk(self, age, gestational_weeks, symptoms, previous_complications=False):
        risk_score = 0
        
        # Age factor
        if age < 18:
            risk_score += 2
        elif age > 35:
            risk_score += 2
        
        # Gestational weeks factor
        if gestational_weeks < 12:
            risk_score += 1
        elif gestational_weeks > 40:
            risk_score += 2
        
        # Symptoms assessment
        high_risk_count = sum(1 for symptom in symptoms if symptom in self.high_risk_symptoms)
        medium_risk_count = sum(1 for symptom in symptoms if symptom in self.medium_risk_symptoms)
        
        risk_score += high_risk_count * 3
        risk_score += medium_risk_count * 1
        
        # Previous complications
        if previous_complications:
            risk_score += 2
        
        # Determine risk level
        if risk_score >= 5:
            return "HIGH RISK", self.get_high_risk_advice(symptoms)
        elif risk_score >= 3:
            return "MEDIUM RISK", self.get_medium_risk_advice(symptoms)
        else:
            return "LOW RISK", self.get_low_risk_advice()
    
    def get_high_risk_advice(self, symptoms):
        advice = "🚨 EMERGENCY - SEEK IMMEDIATE MEDICAL ATTENTION!\n\n"
        advice += "Based on your symptoms, this could be serious.\n"
        advice += "Please go to the nearest hospital or call emergency services.\n"
        
        if 'vaginal bleeding' in symptoms:
            advice += "\n• Vaginal bleeding can indicate serious complications"
        if 'no fetal movement' in symptoms:
            advice += "\n• Reduced fetal movement needs immediate evaluation"
        if 'severe abdominal pain' in symptoms:
            advice += "\n• Severe abdominal pain could indicate emergencies"
        
        advice += "\n\nDon't wait - your health and baby's health are important!"
        return advice
    
    def get_medium_risk_advice(self, symptoms):
        advice = "⚠️ Consult Your Doctor Soon\n\n"
        advice += "You should see a healthcare provider within 24-48 hours.\n"
        
        if 'swelling' in symptoms:
            advice += "\n• Monitor swelling and blood pressure"
        if 'headache' in symptoms:
            advice += "\n• Headaches should be evaluated if persistent"
        if 'dizziness' in symptoms:
            advice += "\n• Stay hydrated and avoid sudden movements"
        
        advice += "\n\nKeep monitoring your symptoms and contact your doctor."
        return advice
    
    def get_low_risk_advice(self):
        advice = "✅ Low Risk - Continue Routine Care\n\n"
        advice += "Your symptoms appear to be within normal range.\n"
        advice += "Continue with your regular prenatal care and:\n"
        advice += "\n• Attend all scheduled appointments"
        advice += "\n• Maintain healthy diet and hydration"
        advice += "\n• Get adequate rest"
        advice += "\n• Monitor any new symptoms"
        
        advice += "\n\nAlways contact your healthcare provider with concerns."
        return advice

# Text-to-Speech Function
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        audio_file = io.BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
            
        return True
    except Exception as e:
        st.error(f"Voice output error: {e}")
        return False

# Main Streamlit App
def main():
    st.set_page_config(
        page_title="MamaAI - Pregnancy Risk Assessment",
        page_icon="🤰",
        layout="wide"
    )
    
    # Initialize predictor
    predictor = PregnancyRiskPredictor()
    
    # App header
    st.title("🤰 MamaAI - Pregnancy Risk Assessment")
    st.markdown("""
    Welcome to MamaAI! I'll help assess your pregnancy symptoms and provide risk guidance.
    **Always consult healthcare professionals for medical advice.**
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About MamaAI")
        st.markdown("""
        This AI assistant helps identify potential pregnancy risks.
        
        **Remember:** This is not a substitute for professional medical care.
        """)
        
        st.header("🚨 Emergency Symptoms")
        st.markdown("""
        Go to hospital immediately if you have:
        - Heavy vaginal bleeding
        - Severe abdominal pain
        - No fetal movement
        - High fever with pain
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Enter Your Information")
        
        with st.form("pregnancy_assessment"):
            age = st.slider("Your Age", 15, 45, 25)
            gestational_weeks = st.slider("Weeks Pregnant", 1, 42, 20)
            
            st.subheader("Select Your Symptoms")
            
            # High risk symptoms
            st.write("**Concerning Symptoms:**")
            high_risk_col1, high_risk_col2 = st.columns(2)
            
            with high_risk_col1:
                bleeding = st.checkbox("Vaginal bleeding")
                severe_pain = st.checkbox("Severe abdominal pain")
                high_fever = st.checkbox("High fever")
                no_movement = st.checkbox("No fetal movement")
            
            with high_risk_col2:
                blurred_vision = st.checkbox("Blurred vision")
                severe_headache = st.checkbox("Severe headache")
                convulsions = st.checkbox("Convulsions")
                water_break = st.checkbox("Water breaking early")
            
            # Medium risk symptoms
            st.write("**Common Symptoms:**")
            medium_risk_col1, medium_risk_col2 = st.columns(2)
            
            with medium_risk_col1:
                mild_headache = st.checkbox("Mild headache")
                swelling = st.checkbox("Swelling")
                dizziness = st.checkbox("Dizziness")
                nausea = st.checkbox("Nausea")
            
            with medium_risk_col2:
                back_pain = st.checkbox("Back pain")
                fatigue = st.checkbox("Fatigue")
                frequent_urination = st.checkbox("Frequent urination")
            
            previous_complications = st.checkbox("Previous pregnancy complications")
            
            submitted = st.form_submit_button("🔍 Assess My Risk")
    
    with col2:
        st.header("🎯 Risk Assessment")
        
        if submitted:
            # Collect symptoms
            symptoms = []
            
            # High risk symptoms
            if bleeding: symptoms.append("vaginal bleeding")
            if severe_pain: symptoms.append("severe abdominal pain")
            if high_fever: symptoms.append("high fever")
            if no_movement: symptoms.append("no fetal movement")
            if blurred_vision: symptoms.append("blurred vision")
            if severe_headache: symptoms.append("severe headache")
            if convulsions: symptoms.append("convulsions")
            if water_break: symptoms.append("water breaking early")
            
            # Medium risk symptoms
            if mild_headache: symptoms.append("mild headache")
            if swelling: symptoms.append("swelling")
            if dizziness: symptoms.append("dizziness")
            if nausea: symptoms.append("nausea")
            if back_pain: symptoms.append("back pain")
            if fatigue: symptoms.append("fatigue")
            if frequent_urination: symptoms.append("frequent urination")
            
            # Perform risk assessment
            if symptoms or previous_complications:
                risk_level, advice = predictor.predict_risk(
                    age, gestational_weeks, symptoms, previous_complications
                )
                
                # Display results
                if risk_level == "HIGH RISK":
                    st.error(f"## {risk_level}")
                    st.error(advice)
                    
                    st.warning("""
                    **Emergency Contacts in Nigeria:**
                    - Emergency: 112 or 199
                    - Contact your nearest hospital immediately!
                    """)
                    
                elif risk_level == "MEDIUM RISK":
                    st.warning(f"## {risk_level}")
                    st.warning(advice)
                    
                else:
                    st.success(f"## {risk_level}")
                    st.success(advice)
                
                # Voice output
                st.subheader("🔊 Voice Output")
                if st.button("🗣️ Hear This Advice"):
                    full_message = f"Risk Level: {risk_level}. {advice}"
                    if speak_text(full_message):
                        st.success("✅ Voice output completed!")
                
                # Summary table
                st.subheader("📊 Assessment Summary")
                summary_data = {
                    'Parameter': ['Age', 'Weeks Pregnant', 'Symptoms Count', 'Previous Complications', 'Risk Level'],
                    'Value': [age, gestational_weeks, len(symptoms), 'Yes' if previous_complications else 'No', risk_level]
                }
                st.table(pd.DataFrame(summary_data))
                
            else:
                st.info("Please select at least one symptom or indicate previous complications.")
        
        else:
            st.info("👈 Fill out the form and click 'Assess My Risk' to get started")

# Run the app
if __name__ == "__main__":
    main()