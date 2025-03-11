import svgwrite

def generate_pacman_svg():
    width, height = 500, 200
    dwg = svgwrite.Drawing("dist/pacman.svg", size=(width, height))

    # Define colors
    pacman_color = "yellow"
    ghost_colors = ["red", "blue", "pink", "orange"]

    # Create Pac-Man (Open Mouth)
    dwg.add(dwg.circle(center=(50, 100), r=20, fill=pacman_color))
    dwg.add(dwg.polygon([(50, 100), (70, 90), (70, 110)], fill="black"))  # Mouth

    # Create Ghosts
    ghost_x = 100  # Initial x position for the first ghost
    for color in ghost_colors:
        dwg.add(dwg.rect(insert=(ghost_x, 80), size=(30, 40), fill=color, rx=10, ry=10))  # Body
        dwg.add(dwg.circle(center=(ghost_x + 8, 90), r=5, fill="white"))  # Left eye
        dwg.add(dwg.circle(center=(ghost_x + 22, 90), r=5, fill="white"))  # Right eye
        ghost_x += 50  # Move next ghost to the right

    # Save the SVG
    dwg.save()

if __name__ == "__main__":
    generate_pacman_svg()
