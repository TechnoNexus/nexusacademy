import os
import pymupdf

def create_pwa_icons():
    os.makedirs('icons', exist_ok=True)
    
    # Nexus Academy Standard Icon (512x512)
    svg_standard = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="nexusBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020b1c"/>
      <stop offset="45%" stop-color="#001a41"/>
      <stop offset="100%" stop-color="#00357a"/>
    </linearGradient>
    <linearGradient id="nexusCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#00a3e0"/>
    </linearGradient>
    <linearGradient id="nexusEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="nexusGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Background with rounded corners -->
  <rect width="512" height="512" rx="116" fill="url(#nexusBg)"/>
  <rect width="504" height="504" x="4" y="4" rx="112" fill="none" stroke="#00a3e0" stroke-width="5" stroke-opacity="0.3"/>

  <!-- Geometric Interconnected Nexus Nodes (Academy Network) -->
  <g stroke-linecap="round" stroke-linejoin="round">
    <!-- Nexus N Backbone -->
    <!-- Left Pillar -->
    <line x1="140" y1="390" x2="140" y2="120" stroke="#005bb7" stroke-width="28"/>
    <!-- Diagonal Bridge -->
    <line x1="140" y1="120" x2="372" y2="390" stroke="url(#nexusCyan)" stroke-width="32" filter="url(#glow)"/>
    <!-- Right Pillar -->
    <line x1="372" y1="390" x2="372" y2="120" stroke="url(#nexusEmerald)" stroke-width="28"/>

    <!-- Interconnecting Academy Orbit Lines -->
    <polygon points="256,76 110,165 256,254 402,165" fill="none" stroke="#00a3e0" stroke-width="12" stroke-opacity="0.5"/>
    <polyline points="110,240 256,328 402,240" fill="none" stroke="#38bdf8" stroke-width="10" stroke-opacity="0.4"/>
    
    <!-- Nexus Core Nodes -->
    <circle cx="140" cy="120" r="22" fill="#005bb7" stroke="#ffffff" stroke-width="5"/>
    <circle cx="372" cy="120" r="22" fill="#10b981" stroke="#ffffff" stroke-width="5"/>
    <circle cx="140" cy="390" r="22" fill="#0284c7" stroke="#ffffff" stroke-width="5"/>
    <circle cx="372" cy="390" r="22" fill="#059669" stroke="#ffffff" stroke-width="5"/>
    <!-- Central Nexus Hub -->
    <circle cx="256" cy="255" r="20" fill="url(#nexusGold)" stroke="#ffffff" stroke-width="5"/>
  </g>

  <!-- Nexus Academy Text Pill at Bottom -->
  <rect x="110" y="430" width="292" height="42" rx="21" fill="rgba(0, 26, 65, 0.85)" stroke="rgba(56, 189, 248, 0.4)" stroke-width="2"/>
  <text x="256" y="457" fill="#ffffff" font-family="'Inter', sans-serif" font-size="20" font-weight="800" letter-spacing="3" text-anchor="middle">NEXUS ACADEMY</text>
</svg>"""

    # Nexus Academy Maskable Icon (Safe Area 80% circle)
    svg_maskable = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="nexusBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#020b1c"/>
      <stop offset="45%" stop-color="#001a41"/>
      <stop offset="100%" stop-color="#00357a"/>
    </linearGradient>
    <linearGradient id="nexusCyan" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8"/>
      <stop offset="100%" stop-color="#00a3e0"/>
    </linearGradient>
    <linearGradient id="nexusEmerald" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#34d399"/>
      <stop offset="100%" stop-color="#059669"/>
    </linearGradient>
    <linearGradient id="nexusGold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#fbbf24"/>
      <stop offset="100%" stop-color="#f59e0b"/>
    </linearGradient>
  </defs>

  <rect width="512" height="512" fill="url(#nexusBg)"/>

  <!-- Nexus Symbol scaled within 75% safe area -->
  <g stroke-linecap="round" stroke-linejoin="round">
    <line x1="160" y1="360" x2="160" y2="152" stroke="#005bb7" stroke-width="26"/>
    <line x1="160" y1="152" x2="352" y2="360" stroke="url(#nexusCyan)" stroke-width="28"/>
    <line x1="352" y1="360" x2="352" y2="152" stroke="url(#nexusEmerald)" stroke-width="26"/>

    <circle cx="160" cy="152" r="18" fill="#005bb7" stroke="#ffffff" stroke-width="4"/>
    <circle cx="352" cy="152" r="18" fill="#10b981" stroke="#ffffff" stroke-width="4"/>
    <circle cx="160" cy="360" r="18" fill="#0284c7" stroke="#ffffff" stroke-width="4"/>
    <circle cx="352" cy="360" r="18" fill="#059669" stroke="#ffffff" stroke-width="4"/>
    <circle cx="256" cy="256" r="16" fill="url(#nexusGold)" stroke="#ffffff" stroke-width="4"/>
  </g>
</svg>"""

    # Save SVGs
    with open('icons/icon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_standard)
    with open('icons/icon-maskable.svg', 'w', encoding='utf-8') as f:
        f.write(svg_maskable)

    def render_png(svg_str, out_path, size):
        doc = pymupdf.open(stream=svg_str.encode('utf-8'), filetype='svg')
        page = doc[0]
        rect = page.rect
        scale = size / rect.width
        mat = pymupdf.Matrix(scale, scale)
        pix = page.get_pixmap(matrix=mat)
        pix.save(out_path)
        print(f"Generated {out_path} ({pix.width}x{pix.height})")

    render_png(svg_standard, 'icons/icon-192.png', 192)
    render_png(svg_standard, 'icons/icon-512.png', 512)
    render_png(svg_standard, 'icons/apple-touch-icon.png', 180)
    render_png(svg_standard, 'icons/favicon.png', 64)
    render_png(svg_maskable, 'icons/icon-maskable-192.png', 192)
    render_png(svg_maskable, 'icons/icon-maskable-512.png', 512)

if __name__ == '__main__':
    create_pwa_icons()
