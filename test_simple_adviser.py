#!/usr/bin/env python3

import requests
import json

# Test adviser registration with ONLY required fields
url = "http://localhost:5000/api/auth/register"

payload = {
    "email": "simple.adviser@usjr.edu.ph",
    "password": "TestPassword123!",
    "firstName": "Test",
    "lastName": "User",
    "role": "adviser",
    "employeeId": "EMP001",
    "school": "Engineering",
    "degreeType": "Bachelor",
    "program": "CS"
}

print(f"Testing with minimal payload:")
print(json.dumps(payload, indent=2))
print("-" * 60)

try:
    response = requests.post(url, json=payload)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response:\n{json.dumps(result, indent=2)}")
    
    if response.status_code == 201:
        print("\n✓ SUCCESS! Data saved to database")
        user_id = result.get('data', {}).get('Id')
        print(f"User ID: {user_id}")
        
        # Query database to verify
        import subprocess
        cmd = f'''psql -h localhost -U postgres -d oims_dev -c "SELECT 'Email', 'Role', 'EmployeeId' FROM \\"Users\\" WHERE \\"Email\\" = 'simple.adviser@usjr.edu.ph';"'''
        # result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        # print(f"\nDatabase verification:\n{result.stdout}")
        
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
