#!/usr/bin/env python3

import requests
import json

# Test adviser registration
url = "http://localhost:5000/api/auth/register"

payload = {
    "email": "adviser.test@usjr.edu.ph",
    "password": "TestPassword123!",
    "firstName": "Juan",
    "lastName": "Dela Cruz",
    "role": "adviser",
    "university": "usjr",
    "employeeId": "ADV00123",
    "school": "College of Engineering",
    "degreeType": "Bachelor",
    "program": "Computer Science"
}

headers = {
    "Content-Type": "application/json"
}

print(f"Testing adviser registration at {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")
print("-" * 60)

try:
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"Error: {e}")
