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
    """Fetch the latest GitHub contributions SVG."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    response = requests.get(SVG_URL)
    
    if response.status_code == 200 and "<svg" in response.text:
        with open(CONTRIBUTIONS_SVG, "w", encoding="utf-8") as f:
            f.write(response.text)
        print("✅ Contributions SVG updated!")
    else:
        print("❌ Failed to fetch valid contributions SVG")
        print(response.text[:500])


def extract_commits():
    """Extract commit positions and their intensity from contributions.svg."""
    if not os.path.exists(CONTRIBUTIONS_SVG):
        print("❌ contributions.svg not found!")
        return []

    with open(CONTRIBUTIONS_SVG, "r", encoding="utf-8") as f:
        contributions_svg = f.read().strip()

    if not contributions_svg or "<svg" not in contributions_svg:
        print("❌ contributions.svg is empty or invalid.")
        return []

    try:
        root = ET.fromstring(contributions_svg)
        print("✅ contributions.svg parsed successfully!")
    except ET.ParseError as e:
        print(f"❌ XML Parse Error: {e}")
        return []

    namespaces = {"svg": "http://www.w3.org/2000/svg"}
    commit_positions = []

    for rect in root.findall(".//svg:rect", namespaces):
        x = rect.get("x")
        y = rect.get("y")
        color = rect.get("fill")

        # Ensure x, y, and color are valid
        if x is None or y is None or color is None:
            continue

        # Ignore empty squares (gray color)
        if color.lower() != "#ebedf0":
            try:
                commit_positions.append((float(x), float(y), color))
            except ValueError:
                continue  # Ignore if conversion fails

    if not commit_positions:
        print("❌ No contributions found!")
        return []

    return sorted(commit_positions, key=lambda pos: pos[1])  # Sort top to bottom


def generate_pacman_svg():
    """Generate an SVG with Pac-Man moving through commit graph."""
    commits = extract_commits()
    if not commits:
        return

    pacman_animation = """
    <animateTransform attributeName="transform" type="translate"
        values=""" + ";".join([f"{x},{y}" for x, y, _ in commits]) + """
        dur="5s" repeatCount="indefinite"/>
    """
    
    commit_circles = [f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>' for x, y, color in commits]
    
    pacman_svg = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <svg width="800" height="200" xmlns="http://www.w3.org/2000/svg">
        <rect width="100%" height="100%" fill="black"/>
        <g id="commits">{" ".join(commit_circles)}</g>
        <g id="pacman" transform="translate({commits[0][0]},{commits[0][1]})">
            <circle r="10" fill="yellow"/>
            <polygon points="0,0 10,-5 10,5" fill="black"/>
            {pacman_animation}
        </g>
    </svg>'''
    
    with open(PACMAN_SVG, "w", encoding="utf-8") as f:
        f.write(pacman_svg)
    
    print("✅ Pac-Man animation generated successfully!")


if __name__ == "__main__":
    download_contributions()
    generate_pacman_svg()
