# app.py
import streamlit as st
import sys
import os

st.set_page_config(page_title="Internship Recommender", layout="centered")
st.title("Internship Recommender System")
st.markdown("Personalized internship suggestions based on your skills!")

# --- DEBUGGING LINES START ---
# Ye lines terminal mein print hongi, Streamlit UI mein nahi.
# Inse aapko path related issues debug karne mein help milegi.
print(f"Current working directory: {os.getcwd()}")
print(f"Path where app.py is located: {os.path.dirname(__file__)}")

script_dir = os.path.join(os.path.dirname(__file__), 'scripts')
print(f"Attempting to add to path: {script_dir}")

if script_dir not in sys.path:
    sys.path.append(script_dir)
    print(f"Added {script_dir} to sys.path.")
else:
    print(f"{script_dir} already in sys.path.")

print("Current sys.path:")
for p in sys.path:
    print(f"  {p}")
# --- DEBUGGING LINES END ---


# Now try to import InternshipRecommender
try:
    # Assuming 'internship_recommender.py' is directly in the 'scripts' folder
    # and 'scripts' folder has been added to sys.path.
    from internship_recommender import InternshipRecommender

    print("Successfully imported InternshipRecommender!")
except ModuleNotFoundError as e:
    st.error(f"Error: Module 'internship_recommender' not found.")
    st.error("Please ensure:")
    st.markdown("- `internship_recommender.py` file exists inside the `scripts` folder.")
    st.markdown("- There is an empty `__init__.py` file inside the `scripts` folder.")
    st.markdown("- You are running `streamlit run app.py` from the `Project` directory.")
    st.error(f"Detailed error: {e}")
    print(f"FATAL ERROR: ModuleNotFoundError - {e}")
    print("This means Python still can't find 'internship_recommender'.")
    print("Double-check the file name (must be .py) and its location within the 'scripts' folder.")
    sys.exit(1)  # Exit the app if the core module cannot be imported

# Initialize recommender only if import was successful
recommender = None  # Initialize to None
try:
    # Make sure the path to internship.csv is correct relative to where app.py is run
    # If 'Data' folder is a sibling to 'app.py' (i.e., inside 'Project' folder),
    # then "Data/internship.csv" is the correct relative path.
    recommender = InternshipRecommender("Data/internship.csv")
    print("InternshipRecommender initialized successfully.")

    # Check for warning messages from the recommender
    if recommender.warning_message:
        st.warning(recommender.warning_message)

except FileNotFoundError:
    st.error("Error: 'internship.csv' not found in the 'Data' folder.")
    st.error("Please ensure `Data/internship.csv` exists relative to `app.py`.")
    print("FATAL ERROR: internship.csv not found.")
    sys.exit(1)
except Exception as e:
    st.error(f"An unexpected error occurred during recommender initialization: {e}")
    print(f"FATAL ERROR during recommender initialization: {e}")
    sys.exit(1)

# Input box for user skills
user_input = st.text_input("Enter your skills (comma-separated):", placeholder="e.g., Python, Marketing, C")

# Display recommendations if user provides input and recommender is ready
if user_input and recommender:
    skills = [skill.strip() for skill in user_input.split(',') if skill.strip()]  # Clean and filter empty strings

    if skills:  # Only proceed if there are valid skills
        st.write("### Your Recommendations:")
        try:
            recommendations = recommender.recommend(skills)
            if not recommendations.empty:
                # Display only relevant columns for the user
                st.dataframe(recommendations[['internship_title', 'company_name', 'skills']])
            else:
                st.info("No recommendations found for the given skills. Try different skills!")
        except Exception as e:
            st.error(f"An error occurred while generating recommendations: {e}")
            print(f"Error during recommendation generation: {e}")
    else:
        st.info("Please enter some skills to get recommendations.")