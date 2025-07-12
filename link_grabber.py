import requests
import re
import base64

def extract_download_links(url):
    # Fetch the HTML content
    response = requests.get(url)
    html = response.text

    # Regex to find all window.open(...) statements
    window_open_calls = re.findall(r'window\.open\((.*?)\)', html)

    links = []

    for call in window_open_calls:
        # Clean up and parse the argument
        call = call.strip()

        # Case: window.open("https://...") — direct link
        if call.startswith('"') or call.startswith("'"):
            link = call.strip('"\'')

        # Case: window.open(atob("..."))
        elif call.startswith('atob('):
            encoded = re.findall(r'atob\(["\'](.*?)["\']\)', call)
            if encoded:
                try:
                    link = base64.b64decode(encoded[0]).decode('utf-8')
                except Exception as e:
                    print(f"❌ Error decoding base64: {e}")
                    continue
            else:
                continue
        else:
            continue

        links.append(link)

    return links

# === Example Usage ===
if __name__ == "__main__":
    input_file = "Desktop/links.txt" 

    try:
        with open(input_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ File not found: {input_file}")
        exit()

    all_links = []

    for test_url in urls:
        print(f"\n🌐 Processing: {test_url}")
        download_links = extract_download_links(test_url)

        if download_links:
            print("✅ Extracted link(s):")
            for link in download_links:
                print(link)
                all_links.append(link)
        else:
            print("⚠️ No links found.")

    # Optional: Save to a file
    with open("extracted_links.txt", "w") as out:
        for link in all_links:
            out.write(link + "\n")

    print(f"\n📝 Saved {len(all_links)} total links to extracted_links.txt")
