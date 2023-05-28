import requests
from bs4 import BeautifulSoup


website = "https://nl.wikipedia.org/wiki/Kat_(dier)"
request = requests.get(website)
soup = BeautifulSoup(request.text, "html.parser")

html_content = ''

for data in soup.find_all(['p', 'h2']):
    html_content += data.get_text()

# print(html_content)

url = "https://bionic-reading1.p.rapidapi.com/convert"

payload = f"content={html_content}&response_type=html&request_type=html&fixation=1&saccade=10"
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"X-RapidAPI-Key": "",
	"X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
}

response = requests.request("POST", url, data=payload, headers=headers)
# print(response.text)

html_content = f'''<html> <body style='font-family:Arial;'> <p> {response.text} </p> </body> </html>'''

with open('bionictext.html', 'w') as html_file:
    html_file.write(html_content)