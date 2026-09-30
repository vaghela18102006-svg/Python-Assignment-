import os
import re
import pickle
import zipfile

folder = input("Enter log folder path: ").strip()

index = {}

for filename in os.listdir(folder):
    filepath = os.path.join(folder, filename)

    if not os.path.isfile(filepath):
        continue

    if not filename.lower().endswith(".txt"):
        continue

    with open(filepath, "r", encoding="utf-8") as file:
        for line_no, line in enumerate(file, 1):
            tokens = re.findall(r'\b[a-zA-Z0-9]+\b', line.lower())

            for token in set(tokens):
                if token not in index:
                    index[token] = []

                index[token].append((filename, line_no))

index_file = os.path.join(folder, "log_index.pkl")

with open(index_file, "wb") as file:
    pickle.dump(index, file)

zip_file = os.path.join(folder, "compressed_logs.zip")

with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)

        if os.path.isfile(filepath):
            if filename.endswith(".txt") or filename == "log_index.pkl":
                zipf.write(filepath, filename)

print("Index created successfully")
print("Index file:", "log_index.pkl")
print("ZIP file:", "compressed_logs.zip")
