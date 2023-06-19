from typing import Dict


def create_success_response(data: Dict[str, any]) -> Dict[str, any]:
    return {
        'status': 'success',
        'data': data
    }


def create_error_response(message: str, status_code: int) -> Dict[str, any]:
    return {
        'status': 'error',
        'message': message,
        'status_code': status_code
    }
