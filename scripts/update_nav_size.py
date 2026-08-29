from pathlib import Path

files_to_update = [Path("index.html")] + list(Path("pages").glob("*.html"))

for file_path in files_to_update:
    content = file_path.read_text(encoding="utf-8")
    if "font-size: 0.85rem;" in content:
        # We replace specifically within .nav-link if needed, or check if 0.85rem is in .nav-link
        updated = content.replace("font-size: 0.85rem;", "font-size: 0.95rem;")
        file_path.write_text(updated, encoding="utf-8")
        print(f"Updated {file_path}")
    else:
        print(f"0.85rem not found in {file_path}")
