import os
import pymupdf

def create_pwa_icons():
    os.makedirs('icons', exist_ok=True)
    
    # Standard icon (with rounded corners for favicon/standard)
    svg_standard = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00122e"/>
      <stop offset="50%" stop-color="#001a41"/>
      <stop offset="100%" stop-color="#002d6b"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00a3e0"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <!-- Background -->
  <rect width="512" height="512" rx="112" fill="url(#bgGrad)"/>
  
  <!-- Outer subtle border -->
  <rect width="504" height="504" x="4" y="4" rx="108" fill="none" stroke="#00a3e0" stroke-width="6" stroke-opacity="0.35"/>
  
  <!-- Top Layer / Prism Peak -->
  <polygon points="256,76 80,180 256,276 432,180" fill="#001a41" fill-opacity="0.6" stroke="url(#accentGrad)" stroke-width="26" stroke-linejoin="round" stroke-linecap="round"/>
  
  <!-- Middle Layer -->
  <polyline points="80,260 256,356 432,260" fill="none" stroke="#005bb7" stroke-width="26" stroke-linejoin="round" stroke-linecap="round"/>
  
  <!-- Bottom Foundation Layer (Pega Emerald Mastery) -->
  <polyline points="80,340 256,436 432,340" fill="none" stroke="#10b981" stroke-width="26" stroke-linejoin="round" stroke-linecap="round"/>
  
  <!-- Small Center Star / Accent -->
  <circle cx="256" cy="180" r="14" fill="#38bdf8"/>
</svg>"""

    # Maskable icon (safe area 80% circle, edge-to-edge background)
    svg_maskable = """<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#00122e"/>
      <stop offset="50%" stop-color="#001a41"/>
      <stop offset="100%" stop-color="#002d6b"/>
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#00a3e0"/>
      <stop offset="100%" stop-color="#38bdf8"/>
    </linearGradient>
  </defs>
  <!-- Full bleed Background for maskable -->
  <rect width="512" height="512" fill="url(#bgGrad)"/>
  
  <!-- Top Layer scaled within safe zone -->
  <polygon points="256,110 116,194 256,270 396,194" fill="#001a41" fill-opacity="0.6" stroke="url(#accentGrad)" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>
  
  <!-- Middle Layer -->
  <polyline points="116,258 256,334 396,258" fill="none" stroke="#005bb7" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>
  
  <!-- Bottom Foundation Layer -->
  <polyline points="116,322 256,398 396,322" fill="none" stroke="#10b981" stroke-width="22" stroke-linejoin="round" stroke-linecap="round"/>
  
  <circle cx="256" cy="194" r="12" fill="#38bdf8"/>
</svg>"""

    # Save SVGs
    with open('icons/icon.svg', 'w', encoding='utf-8') as f:
        f.write(svg_standard)
    with open('icons/icon-maskable.svg', 'w', encoding='utf-8') as f:
        f.write(svg_maskable)

    # Render PNGs
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
