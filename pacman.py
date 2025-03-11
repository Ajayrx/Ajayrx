import svgwrite

def generate_pacman_svg():
    dwg = svgwrite.Drawing("dist/pacman.svg", profile="tiny", size=(800, 200))

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))

    # Pac-Man (yellow circle with mouth)
    pacman = dwg.add(dwg.g(id="pacman"))
    pacman.add(dwg.circle(center=(50, 100), r=20, fill="yellow"))
    pacman.add(dwg.polygon(points=[(50, 100), (70, 90), (70, 110)], fill="black"))  # Mouth

    # Ghost (Purple with eyes)
    ghost = dwg.add(dwg.g(id="ghost"))
    ghost.add(dwg.circle(center=(150, 100), r=18, fill="purple"))
    ghost.add(dwg.circle(center=(145, 95), r=5, fill="white"))
    ghost.add(dwg.circle(center=(155, 95), r=5, fill="white"))

    # Commits (dots that disappear)
    for i in range(5):
        dwg.add(dwg.circle(center=(80 + i * 20, 100), r=5, fill="white"))

    dwg.save()

generate_pacman_svg()
