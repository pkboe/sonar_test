import requests
from http import HTTPStatus
import sys

def handle_failure(error_message, exit_code, is_error_graceful):
    """
    Handles failure scenarios by logging and exiting the script.

    Args:
        error_message (str): Error message to log.
        exit_code (int): Exit code for the script.
        is_error_graceful (bool): Determines if error is an actual execution error or just a usecase failure.
    """
    print(f"ERROR: {error_message}")
    if not is_error_graceful:
        print(f"Failure. Exit code: {exit_code}")
    sys.exit(exit_code)

def fetch_status_and_check_conditions():
    """
    Fetches the status from httpbin and checks conditions.
    Logs the results and exits the script.
    """
    try:
        response = requests.get('https://httpbin.org/status/401')
        
        # Handle HTTP errors (4xx, 5xx)
        response.raise_for_status()

        # Map status code to its meaning using HTTPStatus
        status_meaning = HTTPStatus(response.status_code).phrase
        print(f"Request was successful! Status code: {response.status_code} ({status_meaning})")

        # Handle 200 OK response
        if response.status_code == 200:
            print("Response text:", response.text)
            print("Response headers:", response.headers)
        else:
            # Handle other 2xx responses (e.g., 204 No Content, 201 Created)
            print(f"Received a successful but unexpected response: {response.status_code} ({status_meaning})")
            print("No content or additional data to process.")

    except requests.exceptions.HTTPError as err:
        # Handle HTTP errors (4xx, 5xx)
        status_meaning = HTTPStatus(response.status_code).phrase if response.status_code in HTTPStatus else "Unknown"
        error_message = (
            f"{type(err).__name__}::{repr(err)}::RESPONSE: {repr(err.response.text) if err.response else 'No Response Text'}"
        )
        handle_failure(
            error_message=error_message,
            exit_code=1,
            is_error_graceful=False
        )

    except requests.exceptions.RequestException as err:
        # Handle other types of errors (e.g., connection errors)
        handle_failure(
            error_message=f"{type(err).__name__}::{repr(err)}::No Response",
            exit_code=1,
            is_error_graceful=True
        )

# Main execution
if __name__ == "__main__":
    fetch_status_and_check_conditions()
