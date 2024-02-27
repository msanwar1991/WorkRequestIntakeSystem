from models import WorkRequest, Session
from text_pattern_analyzer import TextPatternAnalyzer


def analyze_request_detail_for_spare_parts(request_detail):
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
    analyzer = TextPatternAnalyzer(training_dataset, min_frequency=3)
    patterns = analyzer.analyze_text([request_detail])
    return any(patterns)


def add_work_request(request_detail, equipment_name, station_name, date_condition_observed, spare_part_required=False):
    session = Session()
    
    # Determine if spare part is required by analyzing the request detail
    spare_part_required = analyze_request_detail_for_spare_parts(request_detail)
    
    # Create a new work request object
    new_request = WorkRequest(
        request_detail=request_detail,
        equipment_name=equipment_name,
        station_name=station_name,
        date_condition_observed=date_condition_observed,
        spare_part_required=spare_part_required
    )
    session.add(new_request)
    session.commit()
    session.close()


def get_all_work_requests():
    session = Session()
    work_requests = session.query(WorkRequest).all()
    session.close()
    return work_requests



def update_work_request(request_id, **kwargs):
    session = Session()
    work_request = session.query(WorkRequest).filter_by(id=request_id).first()
    if work_request:
        # If request_detail is in kwargs, analyze it to update spare_part_required
        # this will ensure that the spare_part_required is updated if the request_detail is updated
        if 'request_detail' in kwargs:
            kwargs['spare_part_required'] = analyze_request_detail_for_spare_parts(kwargs['request_detail'])
        
        for key, value in kwargs.items():
            setattr(work_request, key, value)
        session.commit()
    session.close()

def remove_work_request(request_id):
    session = Session()
    work_request = session.query(WorkRequest).filter_by(id=request_id).first()
    if work_request:
        work_request.remove(session)
    session.close()
