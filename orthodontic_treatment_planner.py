import streamlit as st
import requests
import json
from datetime import date

# Set up the Streamlit app
st.title('Advanced Orthodontic Treatment Planner')

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

# Section V: Diagnosis
st.header('V. Diagnosis')
skeletal_class = st.selectbox("Skeletal Class", ['Class I', 'Class II', 'Class III'])
dental_class = st.selectbox("Dental Class", ['Class I', 'Class II', 'Class III'])
overbite_severity = st.selectbox("Overbite Severity", ['Mild', 'Moderate', 'Severe'])
overjet_status = st.selectbox("Overjet", ['Increased', 'Decreased', 'Normal'])
other_conditions = st.text_area("Other Conditions (e.g., crossbite, impacted teeth)")

# Section VI: Treatment Objectives
st.header('VI. Treatment Objectives')
treatment_objectives = st.text_area("Treatment Objectives (e.g., correct malocclusion, improve aesthetics)")

# Section VII: Treatment Plan
st.header('VII. Treatment Plan')
# Appliance Therapy
appliance_therapy = st.text_area("Appliance Therapy (e.g., braces type, aligners)")
# Archwire Sequence
archwire_sequence = st.text_area("Archwire Sequence (e.g., NiTi for alignment)")
# Adjunctive Therapy
adjunctive_therapy = st.text_area("Adjunctive Therapy (e.g., elastics, extractions, TADs)")

# Section VIII: Retention Phase
st.header('VIII. Retention Phase')
retention_plan = st.text_area("Retention Plan (e.g., removable retainers, fixed retainers)")
retention_period = st.number_input("Retention Period (months)", min_value=6, max_value=36)

# Section IX: Estimated Treatment Duration
st.header('IX. Estimated Treatment Duration')
treatment_duration = st.number_input("Estimated Treatment Duration (months)", min_value=6, max_value=36)
appointments_frequency = st.selectbox("Appointment Frequency (weeks)", [4, 5, 6, 7, 8])

# Section X: Potential Risks and Complications
st.header('X. Potential Risks and Complications')
risks_complications = st.text_area("Potential Risks and Complications (e.g., root resorption, relapse)")

# Informed Consent Section
st.header('XI. Informed Consent')
informed_consent = st.text_area("Informed Consent Details (risks, benefits, and patient consent)")

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
        "max_tokens": 1500
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# Button to Generate Treatment Plan
if st.button('Generate Comprehensive Treatment Plan'):
    if not api_key:
        st.error('Please enter your OpenAI API Key')
    else:
        # Create the prompt for the OpenAI API
        prompt = f"""
        You are an experienced orthodontist. Based on the following details, generate a comprehensive treatment plan for the patient:
        
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

        Diagnosis:
        Skeletal Class: {skeletal_class}
        Dental Class: {dental_class}
        Overbite severity: {overbite_severity}
        Overjet: {overjet_status}
        Other conditions: {other_conditions}

        Treatment Objectives:
        {treatment_objectives}

        Treatment Plan:
        - Appliance Therapy: {appliance_therapy}
        - Archwire Sequence: {archwire_sequence}
        - Adjunctive Therapy: {adjunctive_therapy}

        Retention Phase:
        Retention plan: {retention_plan}
        Retention period: {retention_period} months

        Estimated Treatment Duration: {treatment_duration} months
        Appointments every {appointments_frequency} weeks

        Potential Risks and Complications:
        {risks_complications}

        Informed Consent:
        {informed_consent}
        """

        try:
            # Call OpenAI API using requests
            response = generate_treatment_plan(prompt, api_key)
            treatment_plan = response['choices'][0]['text'].strip()

            # Display the treatment plan
            st.subheader('Generated Treatment Plan')
            st.write(treatment_plan)

        except Exception as e:
            st.error(f"Error generating treatment plan: {e}")

# Footer
st.markdown("---")
st.markdown("Developed using [OpenAI](https://openai.com) and [Streamlit](https://streamlit.io).")
