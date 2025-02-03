from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import math
import logging
from functools import lru_cache
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Constants
NUMBERS_API_BASE_URL = "http://numbersapi.com"
HTTP_OK = 200
HTTP_BAD_REQUEST = 400


@lru_cache(maxsize=1000)
def is_armstrong(num):
    """
    Check if a number is an Armstrong number.
    An Armstrong number is one where the sum of its digits raised to the power 
    of the total number of digits equals the number itself.
    """
    str_num = str(num)
    power = len(str_num)
    total = 0
    for digit in num:
        total += int(digit) ** power
    return num == total


@lru_cache(maxsize=1000)
def is_prime(num):
    """
    Check if a number is prime.
    A prime number is only divisible by 1 and itself.
    """
    if num < 2:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(num)) + 1, 2):
        if num % i == 0:
            return False
    return True


@lru_cache(maxsize=1000)
def is_perfect(num):
    """
    Check if a number is perfect.
    A perfect number equals the sum of its proper divisors.
    """
    if num < 1:
        return False
    sum_of_divisor = 0
    for i in range(1, num):
        if num % i == 0:
            sum_of_divisor += i
    return num == sum_of_divisor


@lru_cache(maxsize=1000)
def get_digit_sum(num):
    """Calculate the sum of digits in the number."""
    digit_sum = 0
    for digit in str(num):
        digit_sum += int(digit)
    return digit_sum


def get_number_properties(num):
    """Gets all the properties of a number."""
    properties = []

    if is_armstrong(num):
        properties.append("armstrong")

    properties.append("even" if num % 2 == 0 else "odd")

    return properties


def get_fun_fact(num):
    """Get a fun fact about the number from the Numbers API."""
    try:
        # Fetch fun fact from the Numbers API
        response = requests.get(f"{NUMBERS_API_BASE_URL}/{num}/math", timeout=2)
        response.raise_for_status()
        fun_fact = response.text

        # Add custom fun fact for Armstrong numbers
        if is_armstrong(num):
            digit_expressions = []
            power = len(str(num))  # Number of digits
            for digit in str(num):
                digit_expressions.append(f"{digit}^{power}")
            armstrong_fact = f"{num} is an Armstrong number because " + " + ".join(digit_expressions) + f" = {num}"

            # Combine the API fun fact with the Armstrong fact
            if armstrong_fact not in fun_fact:
                fun_fact = f"{fun_fact}. Also, {armstrong_fact}"

        return fun_fact

    except requests.RequestException as e:
        # Log the error and return a fallback message
        logger.error(f"Error fetching fun fact: {e}")
        return f"{num} is still a fascinating number!"


def validate_number(num):
    """
    Validate the input number.
    Returns tuple of (is_valid, error_message)
    """
    if not num:
        return False, "Number parameter is required"

    if not num.lstrip('-').isdigit():
        return False, "Input must be a valid integer"

    # If the number is negative, we don't want to process it as an Armstrong number
    if int(num) < 0:
        return False, f"{num} is a boring number"

    return True, None


@app.route('/api/classify-number', methods=['GET'])
def classify_number():
    """Handle GET requests to classify numbers."""
    start_time = time.time()

    try:
        # Get and validate the number
        number = request.args.get('number')
        is_valid, error_message = validate_number(number)

        if not is_valid:
            return jsonify({
                "number": number,
                "error": True,
                "message": error_message
            }), HTTP_BAD_REQUEST

        # Convert to integer
        num = int(number)

        # Prepare response
        response = {
            "number": num,
            "is_prime": is_prime(num),
            "is_perfect": is_perfect(num),
            "properties": get_number_properties(num),
            "digit_sum": get_digit_sum(num),
            "fun_fact": get_fun_fact(num)
        }

        # Log response time
        processing_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        logger.info(f"Request processed in {processing_time:.2f}ms")

        return jsonify(response), HTTP_OK

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({
            "error": True,
            "message": "An unexpected error occurred"
        }), HTTP_BAD_REQUEST


# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify API is running."""
    return jsonify({"status": "healthy"}), HTTP_OK


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
