from typing import Dict


def create_success_response(data: Dict[str, any]) -> tuple[dict, any]:
    return {
        'status': 'success',
        'data': data
    }, 200


def create_error_response(message: str, status_code: int) -> tuple[dict, any]:
    return {
        'status': 'error',
        'message': message,
        'status_code': status_code
    }, status_code
