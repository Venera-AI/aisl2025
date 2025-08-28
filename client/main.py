import requests


def create_session(app_name, user_id, session_id=None, state=None, events=None):
    """
    Create a new session for the given app and user.
    """
    url = f"http://localhost:8000/apps/{app_name}/users/{user_id}/sessions"
    payload = {}
    if state is not None:
        payload["state"] = state
    if events is not None:
        payload["events"] = events
    if session_id:
        # Use the endpoint to create a session with a specific ID
        url = f"http://localhost:8000/apps/{app_name}/users/{user_id}/sessions/{session_id}"
        response = requests.post(url, json=payload)
    else:
        response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()


def run_agent_loop_and_collect_data(user_id: str):
    app_name = "server"
    # Create a new session
    session = create_session(app_name, user_id)
    session_id = (
        session["id"]
        if isinstance(session, dict) and "id" in session
        else session.get("session_id")
    )
    # Prepare payload for /run endpoint
    payload = {
        "appName": app_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "parts": [
                {
                    "text": """{"gender": "Nữ", "date_of_birth": "1958/01/01 00:00", "ethnicity": null, "blood_type": null, "weight": 0.0, "reason_for_admission": null, "admission_diagnosis": null, "discharge_diagnosis": null, "treatment_method": null, "treatment_outcome": "Khỏi", "clinical_progress": [], "inpatient_admission_reason_code": null, "inpatient_admission_reason": null, "main_diagnosis_code": "E11", "main_diagnosis": "Bệnh đái tháo đường không phụ thuộc insuline", "comorbidities": ["Bệnh lý tăng huyết áp", "Bệnh tim thiếu máu cục bộ mạn", "Đau bụng và vùng chậu"], "traditional_medicine_diagnosis": [], "treating_departments": ["Khám bệnh"], "discharge_type": null, "follow_up_date": null, "services": [{"service_name": "Tổng phân tích nước tiểu (Bằng máy tự động)", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 07:55", "results": [{"parameter_name": "SG", "value": ">=1.030", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "PH", "value": "6.5", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "LEU", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "BLD", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "NIT", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "PRO", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "GLU", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "KET", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "BIL", "value": "Negative", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}, {"parameter_name": "UBG", "value": "3.2 umol/L", "unit_of_measure": null, "result_date": "2023/04/25 07:55", "description": null, "conclusion": null}]}, {"service_name": "Định lượng Cholesterol toàn phần (máu)", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 08:19", "results": [{"parameter_name": "Định lượng Cholesterol toàn phần (máu)", "value": "5.08", "unit_of_measure": null, "result_date": "2023/04/25 08:19", "description": null, "conclusion": null}]}, {"service_name": "Định lượng Triglycerid (máu) [Máu]", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 08:19", "results": [{"parameter_name": "Định lượng Triglycerid (máu) [Máu]", "value": "3.77", "unit_of_measure": null, "result_date": "2023/04/25 08:19", "description": null, "conclusion": null}]}, {"service_name": "Định lượng Creatinin (máu)", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 08:19", "results": [{"parameter_name": "Định lượng Creatinin (máu)", "value": "75", "unit_of_measure": null, "result_date": "2023/04/25 08:19", "description": null, "conclusion": null}]}, {"service_name": "Định lượng Glucose [Máu]", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 08:19", "results": [{"parameter_name": "Định lượng Glucose [Máu]", "value": "6.1", "unit_of_measure": null, "result_date": "2023/04/25 08:19", "description": null, "conclusion": null}]}, {"service_name": "Đo hoạt độ AST (GOT) [Máu]", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 08:19", "results": [{"parameter_name": "Đo hoạt độ AST (GOT) [Máu]", "value": "24", "unit_of_measure": null, "result_date": "2023/04/25 08:19", "description": null, "conclusion": null}]}, {"service_name": "Điện tim thường", "order_date": "2023/04/25 06:43", "result_date": "2023/04/25 06:57", "results": [{"parameter_name": "Điện tim thường", "value": null, "unit_of_measure": null, "result_date": "2023/04/25 06:57", "description": "_NHỊP TIM      :   92   L/P\n_PQ    :         192  mS\n_QRS :       98    mS\n_QT    :      364     mS/   414    mS\n_RV5 +   SV1  :   2.795    mV", "conclusion": "NHỊP XOANG ĐỀU   92  L/P "}]}, {"service_name": "Khám Nội", "order_date": "2023/04/25 06:38", "result_date": "2023/04/25 08:48", "results": []}], "prescriptions": [{"medication_name": "Beatil 4mg/5mg (Xuất Xưởng: Gedeon Richter Plc.; Đ/C: Gyomroi Út 19-21, Budapest, 1103, Hungary) (Perindopril + amlodipin) - (4mg+5mg) (Ba Lan)", "quantity": 30, "unit": "Viên", "dosage_strength": "4mg+5mg", "dosage_instruction": "1 Viên/lần * 1 lần/ngày", "order_date": "2023/04/25 08:48", "notes": null}, {"medication_name": "Trimetazidin (Trimpol MR) -35mg (Poland)", "quantity": 30, "unit": "Viên", "dosage_strength": "35mg", "dosage_instruction": "1 Viên/lần * 1 lần/ngày", "order_date": "2023/04/25 08:48", "notes": null}, {"medication_name": "Metformin hydroclorid (Metformin Stella 1000 mg) 1000mg (Stellapharm) ", "quantity": 30, "unit": "Viên", "dosage_strength": "1000mg", "dosage_instruction": "1 Viên/lần * 1 lần/ngày", "order_date": "2023/04/25 08:48", "notes": null}]}"""
                }
            ]
        },
    }
    url = "http://localhost:8000/run"
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print("Run agent response:", response.json())


if __name__ == "__main__":
    # Example user_id, replace as needed
    run_agent_loop_and_collect_data("3242")
