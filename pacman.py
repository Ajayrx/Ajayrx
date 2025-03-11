import os
import svgwrite

def generate_pacman_svg():
    # Ensure the 'dist' directory exists
    os.makedirs("dist", exist_ok=True)
    
    # Create SVG canvas
    dwg = svgwrite.Drawing("dist/pacman.svg", profile="tiny", size=(800, 200))
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="black"))
    
    # Pac-Man (yellow circle with mouth)
    pacman = dwg.add(dwg.g(id="pacman"))
    pacman.add(dwg.circle(center=(50, 100), r=20, fill="yellow"))
    pacman.add(dwg.polygon(points=[(50, 100), (70, 90), (70, 110)], fill="black"))  # Mouth
    
    # Animate Pac-Man moving forward
    pacman.add(dwg.animateTransform(
        attributeName="transform",
        attributeType="XML",
        type="translate",
        from_="0,0",
        to="200,0",
        begin="0s",
        dur="2s",
        repeatCount="indefinite"
    ))
    
    # Ghost (Purple with eyes)
    ghost = dwg.add(dwg.g(id="ghost"))
    ghost.add(dwg.circle(center=(150, 100), r=18, fill="purple"))
    ghost.add(dwg.circle(center=(145, 95), r=5, fill="white"))
    ghost.add(dwg.circle(center=(155, 95), r=5, fill="white"))
    
    # Animate Ghost chasing Pac-Man (delayed start)
    ghost.add(dwg.animateTransform(
        attributeName="transform",
        attributeType="XML",
        type="translate",
        from_="0,0",
        to="180,0",
        begin="0.5s",  # Delayed start
        dur="2s",
        repeatCount="indefinite"
    ))
    
    # Commits (dots that disappear as Pac-Man eats them)
    for i in range(5):
        dot = dwg.circle(center=(80 + i * 40, 100), r=5, fill="white")
        dot.add(dwg.animate(
            attributeName="opacity",
            from_="1",
            to_="0",
            begin=f"{i * 0.4}s",
            dur="0.2s",
            fill="freeze"
        ))
        dwg.add(dot)
    
    # Save SVG file
    dwg.save()
    print("✅ Pac-Man SVG successfully generated in dist/pacman.svg")

# Run function
generate_pacman_svg()
