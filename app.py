import os
import streamlit as st
import google.generativeai as genai

# Step 1: Configure the API with your Gemini API Key
API_KEY = "AIzaSyDGmyrPOLnIqNpHw0ndxkB3fe9LDEhWTP0"  # Replace with your actual API Key
genai.configure(api_key=API_KEY)

# Streamlit App
st.title("ADRShield AI")
st.write("Upload images of medications, prescription images, or enter text to assess potential interactions.")

# Step 2: Add a selection option for the user
option = st.radio("Choose an option:", ("Upload images of medicines", "Upload prescription images", "Enter prescription text"))

# Step 3: Option 1: Upload multiple images of medications
if option == "Upload images of medicines":
    uploaded_files = st.file_uploader("Upload medication images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    if uploaded_files:
        # Display the uploaded images
        for i, uploaded_file in enumerate(uploaded_files):
            st.image(uploaded_file, caption=f"Medication Image {i+1}", use_column_width=True)

        # Submit button to trigger the response
        if st.button("Submit"):
            # Save and upload each medication image to the Gemini API
            uploaded_files_paths = []
            for i, uploaded_file in enumerate(uploaded_files):
                file_path = f"med_image_{i+1}.jpg"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.read())
                uploaded_files_paths.append(file_path)

            # Upload all images to the Gemini API and store the file references
            uploaded_files_refs = [genai.upload_file(file_path) for file_path in uploaded_files_paths]

            # Step 4: Create a structured prompt to ensure the response follows the required format
            prompt_template = """
            You are asked to assess potential Adverse Drug Reactions between the following medications. 
            Please follow this format exactly in your response:

            Adverse Drug Reactions Warnings and Recommendations:

            I understand you're asking about potential interactions between the medications.

            It's crucial to understand that I am an AI and cannot provide medical advice. The information I provide should not be considered a substitute for professional medical guidance.

            Here's what I can tell you about potential interactions based on general information:

            Medications: (Describe the purpose and use of each medication).

            Potential Interactions:

            - Describe any known or potential interactions.

            Recommendations and Warnings:

            - Advise the user to consult their healthcare provider.
            - Monitor for symptoms or unusual side effects.
            - Provide recommendations for discussing these medications with their doctor.

            Make sure to remind the user to consult their doctor or pharmacist for professional advice.
            Cite the references from where the drug interactions were fetched from.
            """

            # Create the prompt (no specific medication names since we are uploading images)
            prompt = prompt_template

            # Step 5: Use the Gemini model to generate a response based on the images and the prompt
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            # Pass the images and the prompt to the model
            response = model.generate_content([prompt] + uploaded_files_refs)

            # Step 6: Output the model’s recommendations in the structured format
            #st.subheader("Adverse Drug Reactions Warnings and Recommendations:")
            st.write(response.text)

# Step 4: Option 2: Upload multiple prescription images
elif option == "Upload prescription images":
    uploaded_prescriptions = st.file_uploader("Upload your prescription images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

    if uploaded_prescriptions:
        # Display the uploaded prescription images
        for i, uploaded_prescription in enumerate(uploaded_prescriptions):
            st.image(uploaded_prescription, caption=f"Prescription Image {i+1}", use_column_width=True)

        # Submit button to trigger the response
        if st.button("Submit"):
            # Save and upload each prescription image to the Gemini API
            uploaded_prescriptions_paths = []
            for i, uploaded_prescription in enumerate(uploaded_prescriptions):
                file_path = f"prescription_image_{i+1}.jpg"
                with open(file_path, "wb") as f:
                    f.write(uploaded_prescription.read())
                uploaded_prescriptions_paths.append(file_path)

            # Upload all prescription images to the Gemini API and store the file references
            uploaded_prescriptions_refs = [genai.upload_file(file_path) for file_path in uploaded_prescriptions_paths]

            # Step 4: Create a structured prompt for the prescription images
            prompt_template = """
            You are asked to assess potential Adverse Drug Reactions based on the following prescription images:

            Please follow this format exactly in your response:

            Adverse Drug Reactions Warnings and Recommendations:

            I understand you're asking about potential interactions between the medications listed in the prescription images.

            It's crucial to understand that I am an AI and cannot provide medical advice. The information I provide should not be considered a substitute for professional medical guidance.

            Here's what I can tell you about potential interactions based on general information:

            List of medications from the prescription: (Describe the purpose and use of each medication).

            Potential Interactions:

            - Describe any known or potential interactions between the listed medications.

            Recommendations and Warnings:

            - Advise the user to consult their healthcare provider.
            - Monitor for symptoms or unusual side effects.
            - Provide recommendations for discussing these medications with their doctor.

            Make sure to remind the user to consult their doctor or pharmacist for professional advice.
            Cite the references from where the drug interactions were fetched from.
            """

            # Use the uploaded prescription images to generate a response
            prompt = prompt_template

            # Step 5: Use the Gemini model to generate a response based on the prescription images and the prompt
            model = genai.GenerativeModel(model_name="gemini-1.5-flash")

            # Pass the prescription images and the prompt to the model
            response = model.generate_content([prompt] + uploaded_prescriptions_refs)

            # Step 6: Output the model’s recommendations in the structured format
            #st.subheader("Adverse Drug Reactions Warnings and Recommendations:")
            st.write(response.text)

# Step 5: Option 3: Enter text for prescription
elif option == "Enter prescription text":
    # Text area for the user to input the prescription
    prescription_text = st.text_area("Enter your prescription details (e.g., 'Aspirin 100mg, Warfarin 5mg daily').")

    # Submit button to trigger the response
    if st.button("Submit") and prescription_text:
        # Step 4: Create a structured prompt for the entered prescription text
        prompt_template = """
        You are asked to assess potential Adverse Drug Reactions based on the following prescription text:

        Prescription: {prescription_text}

        Please follow this format exactly in your response:

       Adverse Drug Reactions Warnings and Recommendations:

        I understand you're asking about potential interactions between the medications listed in the prescription.

        It's crucial to understand that I am an AI and cannot provide medical advice. The information I provide should not be considered a substitute for professional medical guidance.

        Here's what I can tell you about potential interactions based on general information:

        List of medications from the prescription: (Describe the purpose and use of each medication).

        Potential Interactions:

        - Describe any known or potential interactions between the listed medications.

        Recommendations and Warnings:

        - Advise the user to consult their healthcare provider.
        - Monitor for symptoms or unusual side effects.
        - Provide recommendations for discussing these medications with their doctor.

        Make sure to remind the user to consult their doctor or pharmacist for professional advice.
        Cite the references from where the drug interactions were fetched from.
        """

        # Format the prompt with the entered prescription text
        prompt = prompt_template.format(prescription_text=prescription_text)

        # Step 5: Use the Gemini model to generate a response based on the entered text and the prompt
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        # Pass the prompt to the model
        response = model.generate_content([prompt])

        # Step 6: Output the model’s recommendations in the structured format
        #st.subheader("Adverse Drug Reaction Warnings and Recommendations:")
        st.write(response.text)
