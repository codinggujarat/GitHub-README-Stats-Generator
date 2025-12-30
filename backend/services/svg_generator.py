import svgwrite
from svgwrite import shapes, gradients

def get_theme_config(theme):
    themes = {
        "default": {
            "bg_gradient": ["#0d1117", "#161b22"],
            "text": "#c9d1d9",
            "accent": "#58a6ff",
            "border": "#30363d",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "light": {
            "bg_gradient": ["#ffffff", "#f6f8fa"],
            "text": "#24292f",
            "accent": "#0969da",
            "border": "#d0d7de",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "neon": {
            "bg_gradient": ["#000000", "#1a1a1a"],
            "text": "#fff",
            "accent": "#00ffff",
            "border": "#00ffff",
            "font": "Courier, monospace",
            "style": "neon"
        },
        "glass": {
            "bg_gradient": ["#ffffff", "#ffffff"],
            "text": "#fff",
            "accent": "#ffffff",
            "border": "rgba(255, 255, 255, 0.2)",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "glass"
        },
        "cyberpunk": { 
             "bg_gradient": ["#2b213a", "#2b213a"],
             "text": "#fcee0a",
             "accent": "#ff003c",
             "border": "#05d9e8",
             "font": "'Orbitron', sans-serif",
             "style": "tech"
        }
    }
    return themes.get(theme, themes["default"])

def bg_rect(dwg, width, height, theme_cfg):
    # Definition of Gradient
    grad = dwg.defs.add(dwg.linearGradient(id="bgGrad", x1="0%", y1="0%", x2="100%", y2="100%"))
    grad.add_stop_color(0, theme_cfg["bg_gradient"][0])
    grad.add_stop_color(1, theme_cfg["bg_gradient"][1])
    
    # Rect
    rect = dwg.rect(insert=(0, 0), size=(width, height), rx=15, ry=15, fill="url(#bgGrad)", stroke=theme_cfg["border"], stroke_width=1)
    
    if theme_cfg["style"] == "glass":
        rect['fill-opacity'] = 0.6
        
    return rect

def generate_stats_svg(stats, theme="default"):
    dwg = svgwrite.Drawing(size=("480px", "220px"))
    theme_cfg = get_theme_config(theme)
    
    # Background
    dwg.add(bg_rect(dwg, "100%", "100%", theme_cfg))
    
    # Neon Glow Effect
    if theme_cfg["style"] == "neon":
        glow = dwg.defs.add(dwg.filter(id="glow"))
        glow.feGaussianBlur(in_="SourceGraphic", stdDeviation=2)
    
    # Title
    title = dwg.text(f"{stats['name'] or stats['username']}", insert=(25, 40), fill=theme_cfg["text"], font_size="22px", font_weight="bold", font_family=theme_cfg["font"])
    if theme_cfg["style"] == "neon":
        title['filter'] = "url(#glow)"
        title['fill'] = theme_cfg["accent"]
        
    dwg.add(title)
    dwg.add(dwg.text("GitHub Stats", insert=(25, 65), fill=theme_cfg["text"], font_size="12px", opacity=0.7, font_family=theme_cfg["font"]))

    # Stats Grid
    items = [
        ("Stars", stats.get("total_stars", 0), "★"),
        ("Commits", "??", "◉"), # Placeholder as full commits need expensive fetch
        ("Repos", stats.get("public_repos", 0), "📘"),
        ("Followers", stats.get("followers", 0), "👥")
    ]
    
    x_start = 25
    y_start = 100
    
    for i, (label, value, icon) in enumerate(items):
        x = x_start + (i % 2) * 220
        y = y_start + (i // 2) * 55
        
        # Stat Box
        box = dwg.rect(insert=(x, y), size=("200px", "45px"), rx=8, ry=8, fill=theme_cfg["accent"], fill_opacity=0.1)
        dwg.add(box)
        
        # Icon
        dwg.add(dwg.text(icon, insert=(x+15, y+30), fill=theme_cfg["accent"], font_size="18px"))
        
        # Label & Value
        dwg.add(dwg.text(label, insert=(x+45, y+20), fill=theme_cfg["text"], font_size="11px", font_family=theme_cfg["font"]))
        val_text = dwg.text(str(value), insert=(x+45, y+38), fill=theme_cfg["text"], font_size="16px", font_weight="bold", font_family=theme_cfg["font"])
        
        if theme_cfg["style"] == "neon":
             val_text['fill'] = theme_cfg["accent"]
             
        dwg.add(val_text)

    return dwg.tostring()

def generate_language_svg(languages, theme="default"):
    dwg = svgwrite.Drawing(size=("480px", "300px"))
    theme_cfg = get_theme_config(theme)
    
    # Background
    dwg.add(bg_rect(dwg, "100%", "100%", theme_cfg))
    
    # Title
    dwg.add(dwg.text("Top Languages", insert=(25, 40), fill=theme_cfg["text"], font_size="18px", font_weight="bold", font_family=theme_cfg["font"]))
    
    y = 75
    total_usage = sum(languages.values())
    
    for i, (lang, count) in enumerate(list(languages.items())[:6]):
        percentage = (count / total_usage) * 100
        
        # Text
        dwg.add(dwg.text(lang, insert=(25, y), fill=theme_cfg["text"], font_size="13px", font_family=theme_cfg["font"]))
        dwg.add(dwg.text(f"{percentage:.1f}%", insert=(430, y), fill=theme_cfg["text"], text_anchor="end", font_size="13px", font_family=theme_cfg["font"], opacity=0.8))
        
        # Progress Bar BG
        dwg.add(dwg.rect(insert=(25, y+8), size=("420px", "6px"), rx=3, ry=3, fill=theme_cfg["text"], fill_opacity=0.1))
        
        # Progress Bar Fill
        bar_width = (percentage / 100) * 420
        # Varied colors could be added here, using accent for now
        fill_col = theme_cfg["accent"]
        dwg.add(dwg.rect(insert=(25, y+8), size=(f"{bar_width}px", "6px"), rx=3, ry=3, fill=fill_col))
        
        y += 40
        
    return dwg.tostring()

def generate_streak_svg(stats, theme="default"):
    dwg = svgwrite.Drawing(size=("495px", "195px"))
    theme_cfg = get_theme_config(theme)
    
    # Background
    dwg.add(bg_rect(dwg, "100%", "100%", theme_cfg))
    
    # Colors
    text_color = theme_cfg["text"]
    accent_color = "#ff8c00" if theme == "default" else theme_cfg["accent"] 
    muted_color = "#88898b"
    
    # Fonts
    font_family = theme_cfg["font"]
    
    # Center lines
    dwg.add(dwg.line(start=(165, 30), end=(165, 165), stroke=theme_cfg["border"], stroke_width=1))
    dwg.add(dwg.line(start=(330, 30), end=(330, 165), stroke=theme_cfg["border"], stroke_width=1))
    
    # --- Left: Total Contributions ---
    dwg.add(dwg.text(f"{stats['total_contributions']}", insert=(82.5, 70), text_anchor="middle", fill=text_color, font_size="28px", font_weight="bold", font_family=font_family))
    dwg.add(dwg.text("Total Contributions", insert=(82.5, 105), text_anchor="middle", fill=text_color, font_size="14px", font_family=font_family))
    dwg.add(dwg.text(f"{stats['start_date']} - Present", insert=(82.5, 130), text_anchor="middle", fill=muted_color, font_size="12px", font_family=font_family))
    
    # --- Center: Current Streak ---
    cx, cy = 247.5, 80
    r = 35
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=theme_cfg["border"], stroke_width=4))
    dwg.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=accent_color, stroke_width=4, stroke_dasharray="220", stroke_dashoffset="0", transform=f"rotate(-90 {cx} {cy})"))
    
    dwg.add(dwg.text("🔥", insert=(cx, cy-40), text_anchor="middle", font_size="24px")) 
    
    dwg.add(dwg.text(f"{stats['current_streak']}", insert=(cx, cy+10), text_anchor="middle", fill=text_color, font_size="28px", font_weight="bold", font_family=font_family))
    
    dwg.add(dwg.text("Current Streak", insert=(cx, 130), text_anchor="middle", fill=accent_color, font_size="14px", font_weight="bold", font_family=font_family))
    dwg.add(dwg.text(f"{stats['end_date']}", insert=(cx, 155), text_anchor="middle", fill=muted_color, font_size="12px", font_family=font_family))

    # --- Right: Longest Streak ---
    dwg.add(dwg.text(f"{stats['longest_streak']}", insert=(412.5, 70), text_anchor="middle", fill=text_color, font_size="28px", font_weight="bold", font_family=font_family))
    dwg.add(dwg.text("Longest Streak", insert=(412.5, 105), text_anchor="middle", fill=text_color, font_size="14px", font_family=font_family))
    dwg.add(dwg.text(f"{stats['start_date']} - {stats['end_date']}", insert=(412.5, 130), text_anchor="middle", fill=muted_color, font_size="12px", font_family=font_family))

    return dwg.tostring()
