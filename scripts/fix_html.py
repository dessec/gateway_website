import os
import glob

files = glob.glob('**/*.html', recursive=True)
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace the powershell literal "`n"
    content = content.replace("`n", "\n")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Fixed newlines in all html files!")
