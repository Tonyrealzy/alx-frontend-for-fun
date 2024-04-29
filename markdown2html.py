#!/usr/bin/python3

import sys
import markdown
import re
import hashlib

def convert_markdown_to_html(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            markdown_text = f.read()
            html = markdown.markdown(markdown_text)
        with open(output_file, 'w') as f:
            f.write(html)
    except FileNotFoundError:
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)
        
def parse_headings(html):
    html = html.replace('<h1>', '<h1>').replace('</h1>', '</h1>')
    html = html.replace('<h2>', '<h2>').replace('</h2>', '</h2>')
    html = html.replace('<h3>', '<h3>').replace('</h3>', '</h3>')
    html = html.replace('<h4>', '<h4>').replace('</h4>', '</h4>')
    html = html.replace('<h5>', '<h5>').replace('</h5>', '</h5>')
    html = html.replace('<h6>', '<h6>').replace('</h6>', '</h6>')
    return html

def parse_lists(html):
    html = html.replace('<ul>', '<ul>').replace('</ul>', '</ul>')
    html = html.replace('<ol>', '<ol>').replace('</ol>', '</ol>')
    html = html.replace('<li>', '<li>').replace('</li>', '</li>')
    return html

def parse_unordered_lists(html):
    html = html.replace('<ul>', '<ul>').replace('</ul>', '</ul>')
    html = html.replace('<li>', '<li>').replace('</li>', '</li>')
    return html

def parse_paragraphs(html):
    # Wrap each paragraph with <p> tags
    paragraphs = html.split('\n\n')
    html = ''
    for paragraph in paragraphs:
        html += f'<p>\n{paragraph}\n</p>\n'
    # Add <br> tag for line breaks within paragraphs
    html = html.replace('<p>\n', '<p>\n    ').replace('\n</p>', '\n</p>\n')
    return html

def parse_bold(html):
    # Parsing for '**text**' bold syntax
    html = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', html)
    # Parsing for '__text__' bold syntax
    html = re.sub(r'__(.*?)__', r'<em>\1</em>', html)
    return html

def parse_custom_syntax(html):
    # Parsing for [[text]] bold syntax and convert to MD5 (lowercase)
    html = re.sub(r'\[\[(.*?)\]\]', lambda match: hashlib.md5(match.group(1).encode()).hexdigest(), html)
    # Parsing for ((text)) bold syntax and remove all 'c' (case insensitive) from the content
    html = re.sub(r'\(\((.*?)\)\)', lambda match: match.group(1).replace('c', '').replace('C', ''), html)
    return html

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_markdown_to_html(input_file, output_file)
    sys.exit(0)
