import re

def parse_curl_command(curl_command):
    # Remove 'curl' from the beginning of the command and join lines
    curl_command = curl_command.replace('\\\n', ' ').strip()
    if curl_command.startswith('curl'):
        curl_command = curl_command[4:].strip()

    # Initialize variables
    url = ''
    method = 'GET'
    headers = {}
    data = None

    # Parse URL
    url_match = re.search(r"'(https?://[^']+)'", curl_command)
    if url_match:
        url = url_match.group(1)

    # Parse method
    if '-X' in curl_command or '--request' in curl_command:
        method_match = re.search(r'(?:-X|--request)\s+(\w+)', curl_command)
        if method_match:
            method = method_match.group(1)

    # Parse headers
    header_matches = re.finditer(r"-H '([^:]+):\s*([^']+)'", curl_command)
    for match in header_matches:
        headers[match.group(1)] = match.group(2)

    # Parse data
    data_match = re.search(r"--data '(.+?)'", curl_command)
    if data_match:
        data = data_match.group(1)

    return url, method, headers, data

def generate_python_code(url, method, headers, data):
    code = "import requests\n\n"
    code += f"url = '{url}'\n\n"
    
    if headers:
        code += "headers = {\n"
        for key, value in headers.items():
            code += f"    '{key}': '{value}',\n"
        code += "}\n\n"
    else:
        code += "headers = {}\n\n"

    code+= f'requests.{method.lower()}(url, headers=headers)'
    return code

def curl2requests(curl):
    data = parse_curl_command(curl)
    return generate_python_code(*data)