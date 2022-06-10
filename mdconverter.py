
from markdown import markdown
import pdfkit

input_filename = 'mdresult.md'
output_filename = 'mdresult.pdf'

with open(input_filename, 'r', encoding='utf-8') as f:
    html_text = markdown(f.read(), output_format='html5')

pdfkit.from_string(html_text, output_filename, options={'zoom': 2})