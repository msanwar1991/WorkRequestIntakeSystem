# Description: This is the main file for the Streamlit app. 
# It contains the code to display the form to submit work requests and to view and update previous work requests.

# Import necessary libraries
import streamlit as st
from database import add_work_request, get_all_work_requests, remove_work_request, update_work_request

# Function to load values from a file
def load_values_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]

# Load possible values from files in the 'other' folder
equipment_names = load_values_from_file('other/equipment_names.txt')
station_names = load_values_from_file('other/station_names.txt')

# Main title for the form
st.title('Work Request Submission')

# Form to submit work requests
with st.form("work_request_form", clear_on_submit=True):
    # Text input for work request detail
    request_detail = st.text_area("Work Request Detail", help="Describe your work request here.")
    
    # Selectbox for equipment_name and station_name
    equipment_name = st.selectbox("Equipment Tag", options=equipment_names)
    station_name = st.selectbox("Station Name", options=station_names)  
    
    # Date input for date_condition_observed
    date_condition_observed = st.date_input("Date Condition Observed") 
    
    # Form submit button to submit the form
    submitted = st.form_submit_button("Submit")

    if submitted and request_detail:
        add_work_request(request_detail, equipment_name, station_name, date_condition_observed, spare_part_required=False)
        st.success("Your work request has been submitted successfully!")
        st.rerun()

# Section to view previous work requests
st.header("Previous Work Requests")
work_requests = get_all_work_requests()

# Display each work request with all details and options to update and delete
for wr in work_requests:
    with st.expander(f"Request ID: {wr.id}"):
        st.write(f"Submitted on: {wr.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        st.write(f"Equipment Name: {wr.equipment_name}")
        st.write(f"Station Name: {wr.station_name}")
        st.write(f"Date Condition Observed: {wr.date_condition_observed.strftime('%Y-%m-%d') if wr.date_condition_observed else 'N/A'}")

        spare_part_string = "Yes (Prediction)" if wr.spare_part_required else "No (Prediction)"
        st.write(f"Spare Part Required: {spare_part_string}")

        # Form to update work request
        with st.form(f"update_form_{wr.id}", clear_on_submit=True):
            new_detail = st.text_area("Update Request Detail", value=wr.request_detail)
            new_equipment_name = st.selectbox(f"Update Equipment Tag for ID: {wr.id}", options=equipment_names, index=equipment_names.index(wr.equipment_name) if wr.equipment_name in equipment_names else 0)
            new_station_name = st.selectbox(f"Update Station Name for ID: {wr.id}", options=station_names, index=station_names.index(wr.station_name) if wr.station_name in station_names else 0)
            new_date_observed = st.date_input("Update Date Condition Observed", value=wr.date_condition_observed if wr.date_condition_observed else st.date_input("Date"))
            update_submitted = st.form_submit_button("Update")

            if update_submitted:
                update_work_request(wr.id, request_detail=new_detail, equipment_name=new_equipment_name, station_name=new_station_name, date_condition_observed=new_date_observed, spare_part_required=False)
                st.success(f"Work Request ID: {wr.id} updated successfully!")
                st.rerun()

        # Button to delete the work request
        if st.button(f"Delete ID: {wr.id}"):
            remove_work_request(wr.id)
            st.success(f"Work Request ID: {wr.id} deleted successfully!")
            st.rerun()