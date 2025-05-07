from django.conf import settings
import requests
import logging
import re

def validate_turnstile(turnstile_response, remote_ip=None):
    logger = logging.getLogger(__name__)
    data = {
        'secret': settings.TURNSTILE_SECRET,
        'response': turnstile_response,
    }
    if remote_ip:
        data['remoteip'] = remote_ip
    logger.error(data)

    try:
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        return result.get('success', False)
    except requests.exceptions.RequestException as e:
        logger.error("validate_turnstile error")
        logger.error(e)
        return False

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None