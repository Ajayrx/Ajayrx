import os

SVG_CONTENT = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg width="800" height="200" viewBox="0 0 800 200" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="black"/>

    <!-- Pac-Man -->
    <g id="pacman" transform="translate(50,100)">
        <circle r="20" fill="yellow"/>
        <polygon points="0,0 20,-10 20,10" fill="black"/>
        <animateTransform attributeName="transform" type="translate"
                          from="50,100" to="750,100" dur="5s" repeatCount="indefinite"/>
    </g>

    <!-- Ghost -->
    <g id="ghost" transform="translate(700,100)">
        <circle r="18" fill="purple"/>
        <circle cx="-5" cy="-5" r="5" fill="white"/>
        <circle cx="5" cy="-5" r="5" fill="white"/>
        <animateTransform attributeName="transform" type="translate"
                          from="700,100" to="0,100" dur="5s" repeatCount="indefinite"/>
    </g>

    <!-- Dots (GitHub Contributions) -->
    {}
</svg>"""

def generate_pacman_svg():
    os.makedirs("dist", exist_ok=True)

    dots = ""
    for i in range(10):  # 10 "commits"
        x = 100 + i * 60
        dots += f'<circle cx="{x}" cy="100" r="5" fill="white">\n'
        dots += f'  <animate attributeName="opacity" from="1" to="0" begin="{i * 0.4}s" dur="0.2s" fill="freeze"/>\n'
        dots += '</circle>\n'

    # Save SVG file
    with open("dist/pacman.svg", "w") as f:
        f.write(SVG_CONTENT.format(dots))

    print("✅ Pac-Man contribution SVG successfully generated!")

# Run the function
generate_pacman_svg()
