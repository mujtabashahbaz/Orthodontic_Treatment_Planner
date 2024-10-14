import streamlit as st
import requests
import json
from datetime import date

# Set up the Streamlit app
st.title('AI-powered Orthodontic Diagnosis and Treatment Planner')

# Ask for OpenAI API key
api_key = st.text_input('Enter your OpenAI API Key', type='password')

# Section I: Basic Information
st.header('I. Basic Information')
patient_name = st.text_input("Patient's Name")
dob = st.date_input("Date of Birth")
date_of_consultation = st.date_input("Date of Consultation", value=date.today())
orthodontist_name = st.text_input("Orthodontist Name")
patient_id = st.text_input("Patient ID")

# Section II: Chief Complaint
st.header('II. Chief Complaint')
chief_complaint = st.text_area("Chief Complaint (e.g., crowding, overbite, spacing)")
aesthetic_concerns = st.text_area("Aesthetic Concerns (e.g., front teeth alignment)")
functional_concerns = st.text_area("Functional Concerns (e.g., chewing difficulties)")

# Section III: Clinical Examination
st.header('III. Clinical Examination')
# Extraoral Examination
st.subheader('Extraoral Examination')
facial_symmetry = st.selectbox("Facial Symmetry", ['Symmetric', 'Asymmetric'])
lip_competency = st.selectbox("Lip Competency", ['Competent', 'Incompetent'])
smile_line = st.selectbox("Smile Line", ['High', 'Low', 'Normal'])
chin_position = st.selectbox("Chin Position", ['Protrusive', 'Retrusive', 'Normal'])

# Intraoral Examination
st.subheader('Intraoral Examination')
arch_form = st.selectbox("Arch Form", ['U-shaped', 'V-shaped'])
crowding = st.selectbox("Crowding", ['Mild', 'Moderate', 'Severe', 'None'])
spacing = st.selectbox("Spacing", ['Present', 'Absent'])
crossbite = st.selectbox("Crossbite", ['Anterior', 'Posterior', 'Absent'])
overbite = st.selectbox("Overbite", ['Normal', 'Deep', 'Open'])
overjet = st.selectbox("Overjet", ['Normal', 'Increased', 'Decreased'])
occlusion_class = st.selectbox("Occlusion Class", ['Class I', 'Class II', 'Class III'])

# Section IV: Radiographic Analysis
st.header('IV. Radiographic Analysis')
# Cephalometric Analysis
st.subheader('Cephalometric Analysis')
sna = st.number_input("SNA (degree)", min_value=0.0, max_value=90.0, step=0.1)
snb = st.number_input("SNB (degree)", min_value=0.0, max_value=90.0, step=0.1)
anb = st.number_input("ANB (degree)", min_value=-10.0, max_value=10.0, step=0.1)
fma = st.number_input("FMA (degree)", min_value=0.0, max_value=60.0, step=0.1)

# Panoramic X-ray
st.subheader('Panoramic X-ray')
impacted_teeth = st.text_input("Impacted Teeth (specify if present)")
root_resorption = st.selectbox("Root Resorption", ['Present', 'Absent'])
eruption_pattern = st.selectbox("Eruption Pattern", ['Normal', 'Delayed'])

# Function to call OpenAI API
def generate_treatment_plan(prompt, api_key):
    url = "https://api.openai.com/v1/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 1500,
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Button to Generate Diagnosis and Treatment Plan
if st.button('Generate Diagnosis and Treatment Plan'):
    if not api_key:
        st.error('Please enter your OpenAI API Key')
    else:
        # Create the prompt for the OpenAI API
        prompt = f"""
        You are an experienced orthodontist. Based on the following details, generate both a comprehensive diagnosis (Dx) and a treatment plan (Rx) for the patient:
        
        - Patient's Name: {patient_name}
        - Date of Birth: {dob}
        - Date of Consultation: {date_of_consultation}
        - Orthodontist: Dr. {orthodontist_name}
        - Patient ID: {patient_id}

        Chief Complaint:
        {chief_complaint}
        Aesthetic Concerns: {aesthetic_concerns}
        Functional Concerns: {functional_concerns}

        Clinical Examination:
        - Facial symmetry: {facial_symmetry}
        - Lip competency: {lip_competency}
        - Smile line: {smile_line}
        - Chin position: {chin_position}
        - Arch form: {arch_form}
        - Crowding: {crowding}
        - Spacing: {spacing}
        - Crossbite: {crossbite}
        - Overbite: {overbite}
        - Overjet: {overjet}
        - Occlusion Class: {occlusion_class}

        Radiographic Analysis:
        - SNA: {sna} degrees
        - SNB: {snb} degrees
        - ANB: {anb} degrees
        - FMA: {fma} degrees
        - Impacted teeth: {impacted_teeth}
        - Root resorption: {root_resorption}
        - Eruption pattern: {eruption_pattern}

        Based on this data, provide a detailed diagnosis (Dx) of the patient's orthodontic condition, followed by a comprehensive treatment plan (Rx) that includes proposed appliances, sequence of therapy, adjunctive treatments if necessary, and estimated treatment duration.
        """

        try:
            # Call OpenAI API using requests
            response = generate_treatment_plan(prompt, api_key)
            
            if response:
                if 'choices' in response and len(response['choices']) > 0:
                    treatment_plan = response['choices'][0]['text'].strip()

                    # Display the diagnosis and treatment plan
                    st.subheader('Generated Diagnosis and Treatment Plan')
                    st.write(treatment_plan)
                else:
                    st.error('Unexpected response structure. Please check the API call or prompt.')
        except Exception as e:
            st.error(f"Error generating treatment plan: {e}")

# Footer
st.markdown("---")
st.markdown("Developed using [OpenAI](https://openai.com) and [Streamlit](https://streamlit.io).")
