import os
import re
import glob
import time

# Warning: The address part will be "location,suburb,code", if you want another forms, you need to change it in line 78
# Every document prepared for processing needs to be in TXT format. To reduce the burden of regex matching, I have applied some extreme deletions, keeping only the necessary parts.


# Setting
input_folder = r"YOUR INPUT FILE PATH"    # input file path,please replace the content inside "" before use
output_file = r"YOUR OUTPUT FILE PATH  \final_result.txt"  # output file path, but do not delete"\final_result.txt"

# the matching order is "displayValue"（phone）， "name"，"addressLine"，"postCode"，"suburb"，"primaryEmail"
pattern = re.compile(
    r'"displayValue"\s*:\s*"([^"]*?)".*?'         # matching phone number
    r'"name"\s*:\s*"([^"]+)"\s*,\s*"openingHoursView".*?'   # matching the name
    r'"addressLine"\s*:\s*(?:"(.*?)"|null).*?'      # matching address
    r'"postCode"\s*:\s*(?:"(.*?)"|null).*?'         # matching postCode
    r'"suburb"\s*:\s*(?:"(.*?)"|null).*?'           # matching suburb
    r'"primaryEmail"\s*:\s*(?:"(.*?)"|null)',       # matching email
    re.DOTALL
)

# stored by (suburb, name, address, postCode, email, phone) 
records = []

# sort all txt
txt_files = glob.glob(os.path.join(input_folder, "*.txt"))
txt_files.sort()

print("Pairing …")
start_total = time.time()
for i, filepath in enumerate(txt_files, 1):
    file_start = time.time()
    filename = os.path.basename(filepath)
    print(f"[{i}/{len(txt_files)}] Processing file: {filename}")

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # only keep the content between (function () { and <body> 
    start_idx = content.find('(function () {')
    end_idx = content.find('<body>')
    if start_idx == -1 or end_idx == -1 or end_idx <= start_idx:
        print(f"  File {filename} does not contain required markers, skipping.")
        continue
    content = content[start_idx:end_idx]
    
    # matching and output
    matches = pattern.findall(content)
    if matches:
        for match in matches:
            phone, name, address, postCode, suburb, email = match
            if not address or address.lower() == "null":
                address = "N/A"
            if not postCode or postCode.lower() == "null":
                postCode = "N/A"
            if not suburb or suburb.lower() == "null":
                suburb = "N/A"
            if not email or email.lower() == "null":
                email = "N/A"
            records.append((suburb, name, address, postCode, email, phone))
    else:
        print(f"  File {filename} did not match any data.")
    
    file_end = time.time()
    print(f"  File {filename} processed in {file_end - file_start:.2f} sec.")

# sort by first letter of suburb then the first letter name. If you don't want this, you can delete line 71
records.sort(key=lambda r: (r[0].upper(), r[1].upper()))

# form the result
results = []
results.append("Name=MergedAddress=Email=Phone")
for rec in records:
    suburb, name, address, postCode, email, phone = rec
    merged_addr = ",".join([address, suburb, postCode])
    line = "=".join([name, merged_addr, email, phone])
    results.append(line)

# replace all \u002F
final_output = "\n".join(results)
final_output = final_output.replace("\\u002F", "/")
with open(output_file, "w", encoding="utf-8") as out:
    out.write(final_output)

end_total = time.time()
print(f"\nAll files processed in {end_total - start_total:.2f} sec.")
print(f"Results saved to: {output_file}")
