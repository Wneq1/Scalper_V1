
with open("vinted.html", "r", encoding="utf-8") as f:
    content = f.read()

search_term = "Czarna męska bluza"
index = content.find(search_term)

if index != -1:
    print(f"Found '{search_term}' at index {index}")
    start = max(0, index - 500)
    end = min(len(content), index + 500)
    print("Context around match:")
    print(content[start:end])
else:
    print(f"'{search_term}' not found.")
