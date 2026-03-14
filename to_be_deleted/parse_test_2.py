from bs4 import BeautifulSoup

with open("C:/Projects/Gateway_Final/rw_snippet.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

scripts = soup.find_all("script")
for s in scripts:
    if s.string and "window.payloads" in s.string:
        print("FOUND PAYLOADS:")
        print(s.string.strip()[:1000])

for s in scripts:
    if s.string and "buildItem" in s.string:
        print("FOUND BUILD ITEM:", s.string.strip()[:500])
