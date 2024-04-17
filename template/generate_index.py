import json
from jinja2 import Environment, FileSystemLoader

"""
usage: python generate_index.py

Make sure Jinja2 is installed
"""

# Set up Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))

# Load the template
template = env.get_template('template.html')

# Load JSON data
with open('data.json', 'r') as f:
    data = json.load(f)

# Render the template with the data
output_html = template.render(data)

# Write the output to a new HTML file
with open('../index.html', 'w') as f:
    f.write(output_html)
