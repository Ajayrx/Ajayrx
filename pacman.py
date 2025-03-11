import os
import requests
import xml.etree.ElementTree as ET

# GitHub username
GITHUB_USER = "Ajayrx"
SVG_URL = f"https://github-contributions-api.deno.dev/{GITHUB_USER}.svg"
OUTPUT_DIR = "dist"
CONTRIBUTIONS_SVG = os.path.join(OUTPUT_DIR, "contributions.svg")
PACMAN_SVG = os.path.join(OUTPUT_DIR, "pacman.svg")

def download_contributions():
    """Fetch the latest GitHub contributions SVG from Vercel API."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    response = requests.get(SVG_URL)
    
    if response.status_code == 200 and "<svg" in response.text:
        with open(CONTRIBUTIONS_SVG, "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Contributions SVG updated!")
    else:
        print("❌ Failed to fetch valid contributions SVG")
        print(response.text[:500])  # Print response for debugging

def generate_pacman_svg():
    """Create an animated Pac-Man eating contributions without overlapping."""
    if not os.path.exists(CONTRIBUTIONS_SVG):
        print("❌ contributions.svg not found! Run the script again after fetching.")
        return

    with open(CONTRIBUTIONS_SVG, "r", encoding="utf-8") as f:
        contributions_svg = f.read().strip()

    if not contributions_svg or "<svg" not in contributions_svg:
        print("❌ contributions.svg is empty or not valid.")
        return

    try:
        root = ET.fromstring(contributions_svg)
        print("✅ contributions.svg successfully parsed!")
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return

    # Extract commit positions
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    commit_circles = []
    x_positions = []

    for rect in root.findall(".//svg:rect", namespaces):
        x = rect.get("x")
        y = rect.get("y")
        color = rect.get("fill")
        if x and y and color != "#ebedf0":  # Ignore empty contribution squares
            x_positions.append(float(x))
            commit_circles.append(f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>')

    if not x_positions:
        print("❌ No contributions found!")
        return
    
    min_x, max_x = min(x_positions), max(x_positions)
    
    # Pac-Man movement animation
    pacman_animation = f'''
    <animateTransform attributeName="transform" type="translate"
        from="{min_x},50" to="{max_x+10},50"
        dur="5s" repeatCount="indefinite"/>
    '''

    # Create Pac-Man animation with "eating" effect
    pacman_svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="black"/>
        
        <!-- Contributions Grid -->
        <g id="commits">
            {" ".join(commit_circles)}
        </g>
        
        <!-- Pac-Man -->
        <g id="pacman" transform="translate({min_x},50)">
            <circle r="10" fill="yellow"/>
            <polygon points="0,0 10,-5 10,5" fill="black"/>
            {pacman_animation}
        </g>

        <!-- Eating Effect -->
        <g id="eating">
            <animate attributeName="opacity" values="1;0" keyTimes="0;1" dur="5s" repeatCount="indefinite"/>
        </g>
    </svg>'''

    with open(PACMAN_SVG, "w", encoding="utf-8") as f:
        f.write(pacman_svg)
    
    print("✅ Pac-Man animation generated with commit eating effect!")

if __name__ == "__main__":
    download_contributions()
    generate_pacman_svg()
