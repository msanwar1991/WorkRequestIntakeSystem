# Import necessary classes from the models module
from models import WorkRequest, Session
# Import the TextPatternAnalyzer class for text pattern analysis
from text_pattern_analyzer import TextPatternAnalyzer

def analyze_request_detail_for_spare_parts(request_detail):
    # Define a training dataset to help the analyzer detect patterns related to spare parts
    training_dataset = [
            ["need", "replace", "<PART>"],
            ["check", "<CAT_ID>", "available"],
            ["detected", "malfunction", "requires", "<PART>"],
            ["stuck", "suspect", "<CAT_ID>", "replacement"],
            ["leak", "potentially", "needs", "<PART>"],
            ["not responding", "consider", "ordering", "<CAT_ID>"],
            ["wearing out", "might need", "<PART>"],
            ["degrading", "suggest checking", "<CAT_ID>"],
            ["issue detected", "likely needs", "<PART>"],
            ["glitching", "might require", "<CAT_ID>"]
        ]
    # Initialize the TextPatternAnalyzer with the training dataset and a minimum frequency for pattern detection
    analyzer = TextPatternAnalyzer(training_dataset, min_frequency=3)
    # Analyze the provided request_detail to check for patterns that indicate the need for a spare part
    patterns = analyzer.analyze_text([request_detail])
    # Return True if any patterns are found, indicating a spare part is required
    return any(patterns)

def add_work_request(request_detail, equipment_name, station_name, date_condition_observed, spare_part_required=False):
    # Start a new session with the database
    session = Session()
    
    try:
        # Determine if a spare part is required by analyzing the request detail text
        spare_part_required = analyze_request_detail_for_spare_parts(request_detail)
    
        # Create a new WorkRequest object with the provided details and the result of the spare part analysis
        new_request = WorkRequest(
            request_detail=request_detail,
            equipment_name=equipment_name,
            station_name=station_name,
            date_condition_observed=date_condition_observed,
            spare_part_required=spare_part_required
        )
        # Add the new work request to the database session and commit the changes to save it
        session.add(new_request)
        session.commit()
    except Exception as e:
        # Roll back the session in case of an error to prevent partial changes
        session.rollback()
        raise e
    finally:
        # Close the session to release the connection to the database
        session.close()

def get_all_work_requests():
    # Start a new session with the database
    session = Session()
    # Retrieve all WorkRequest entries from the database
    work_requests = session.query(WorkRequest).all()
    # Close the session to release the connection to the database
    session.close()
    # Return the list of work requests
    return work_requests

def update_work_request(request_id, **kwargs):
    # Start a new session with the database
    session = Session()
    # Fetch the work request by its ID
    work_request = session.query(WorkRequest).filter_by(id=request_id).first()
    if work_request:
        # Check if request_detail was provided in the keyword arguments to update the spare part requirement
        if 'request_detail' in kwargs:
            kwargs['spare_part_required'] = analyze_request_detail_for_spare_parts(kwargs['request_detail'])
        
        # Update the work request with the provided keyword arguments
        for key, value in kwargs.items():
            setattr(work_request, key, value)
        # Commit the changes to the database
        session.commit()
    # Close the session to release the connection to the database
    session.close()

def remove_work_request(request_id):
    # Start a new session with the database
    session = Session()
    # Fetch the work request by its ID
    work_request = session.query(WorkRequest).filter_by(id=request_id).first()
    if work_request:
        # Remove the work request from the session and commit the change
        work_request.remove(session)
    # Close the session to release the connection to the database
    session.close()