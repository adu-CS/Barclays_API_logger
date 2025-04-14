import time
import random
from log_utils import setup_logger

# Set up logger with custom source name
logger = setup_logger('aws_api', 'aws')

def simulate_api_call():
    try:
        # Simulate response time and status
        response_time = random.randint(100, 900)  # in ms
        status_code = random.choices([200, 200, 200, 500, 502], weights=[80, 10, 5, 3, 2])[0]

        # Log successful call or error based on status
        if status_code >= 500:
            raise Exception(f"Simulated error with status code {status_code}")
        
        logger.info("API call success", extra={
            "response_time": response_time,
            "status_code": status_code,
            "api_environment": "aws"
        })

    except Exception as e:
        logger.error("API call failed", extra={
            "error": str(e),
            "response_time": None,
            "status_code": 500,
            "api_environment": "aws"
        })

# 👇 Loop for continuous logging
if __name__ == "__main__":
    print("[AWS API SIMULATOR] Generating logs every 5 sec...")
    while True:
        simulate_api_call()
        time.sleep(3)
