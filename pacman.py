import os
import requests
from xml.etree import ElementTree as ET

# GitHub username
GITHUB_USER = "Ajayrx"
SVG_URL = f"https://github.com/{GITHUB_USER}.svg"
OUTPUT_DIR = "dist"
PACMAN_SVG = os.path.join(OUTPUT_DIR, "pacman.svg")
CONTRIBUTIONS_SVG = os.path.join(OUTPUT_DIR, "contributions.svg")

def download_contributions():
    """Fetch the latest GitHub contributions SVG."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    response = requests.get(SVG_URL)
    if response.status_code == 200:
        with open(CONTRIBUTIONS_SVG, "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Contributions SVG updated!")
    else:
        print("❌ Failed to fetch contributions SVG")

def generate_pacman_svg():
    """Create an animated Pac-Man eating contributions."""
    if not os.path.exists(CONTRIBUTIONS_SVG):
        print("❌ contributions.svg not found! Run the script again after fetching.")
        return

    # Read contributions SVG content
    with open(CONTRIBUTIONS_SVG, "r", encoding="utf-8") as f:
        contributions_svg = f.read()
    
    # Extract commit positions
    root = ET.fromstring(contributions_svg)
    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    dots = ""
    pacman_path = ""
    x_positions = []
    
    for rect in root.findall(".//svg:rect", namespaces):
        x = rect.get("x")
        y = rect.get("y")
        color = rect.get("fill")
        if x and y and color != "#ebedf0":  # Ignore empty contributions
            x_positions.append(float(x))
            dots += f'<circle cx="{x}" cy="{y}" r="5" fill="white"/>'
    
    if not x_positions:
        print("❌ No contributions found!")
        return
    
    min_x, max_x = min(x_positions), max(x_positions)
    pacman_path = f'<animateTransform attributeName="transform" type="translate" from="{min_x},100" to="{max_x+10},100" dur="5s" repeatCount="indefinite"/>'

    # Create final SVG
    pacman_svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="black"/>
        {contributions_svg}
        
        <!-- Pac-Man -->
        <g id="pacman" transform="translate({min_x},100)">
            <circle r="10" fill="yellow"/>
            <polygon points="0,0 10,-5 10,5" fill="black"/>
            {pacman_path}
        </g>
        {dots}
    </svg>'''
    
    with open(PACMAN_SVG, "w", encoding="utf-8") as f:
        f.write(pacman_svg)
    print("✅ Pac-Man animation generated!")

if __name__ == "__main__":
    download_contributions()
    generate_pacman_svg()
