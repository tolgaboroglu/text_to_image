import imgkit

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Sample HTML</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a sample HTML content.</p>
</body>
</html>
"""

options = {
    'format': 'png',
    'encoding': 'utf-8',
    'quiet': '',
}

# Replace '/path/to/wkhtmltoimage' with the actual path where wkhtmltoimage is installed
wkhtmltoimage_path = 'wkhtmltoimage.exe'

config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)

try:
    img = imgkit.from_string(html_content, False , options=options, config=config)
    print("Image successfully generated.") 
    print(type(img))
except Exception as e:
    print("Error:", e)