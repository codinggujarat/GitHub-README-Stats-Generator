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
        },
        "dracula": {
            "bg_gradient": ["#282a36", "#282a36"],
            "text": "#f8f8f2",
            "accent": "#ff79c6",
            "border": "#bd93f9",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "monokai": {
            "bg_gradient": ["#272822", "#272822"],
            "text": "#f8f8f2",
            "accent": "#a6e22e",
            "border": "#75715e",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "nord": {
            "bg_gradient": ["#2e3440", "#2e3440"],
            "text": "#d8dee9",
            "accent": "#88c0d0",
            "border": "#4c566a",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "solarized_light": {
            "bg_gradient": ["#fdf6e3", "#fdf6e3"],
            "text": "#657b83",
            "accent": "#268bd2",
            "border": "#93a1a1",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "solarized_dark": {
            "bg_gradient": ["#002b36", "#002b36"],
            "text": "#839496",
            "accent": "#b58900",
            "border": "#586e75",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "cobalt": {
            "bg_gradient": ["#002240", "#002240"],
            "text": "#ffffff",
            "accent": "#ffc600",
            "border": "#193549",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "synthwave": {
            "bg_gradient": ["#2b213a", "#241b2f"],
            "text": "#b3f7f7",
            "accent": "#ff71ce",
            "border": "#362c4c",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "neon"
        },
        "high_contrast": {
            "bg_gradient": ["#000000", "#000000"],
            "text": "#ffffff",
            "accent": "#ffffff",
            "border": "#ffffff",
            "font": "'Segoe UI', Ubuntu, Sans-Serif",
            "style": "clean"
        },
        "gruvbox": {
             "bg_gradient": ["#282828", "#282828"],
             "text": "#ebdbb2",
             "accent": "#fe8019",
             "border": "#504945",
             "font": "'Segoe UI', Ubuntu, Sans-Serif",
             "style": "clean"
        },
        "tokyonight": {
             "bg_gradient": ["#1a1b26", "#1a1b26"],
             "text": "#a9b1d6",
             "accent": "#7aa2f7",
             "border": "#414868",
             "font": "'Segoe UI', Ubuntu, Sans-Serif",
             "style": "clean"
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
        ("Commits", stats.get("total_commits", "??"), "◉"), 
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

def generate_trophies_svg(stats, theme="default"):
    # High-fidelity layout: 6 columns x 2 rows
    # Width: ~800px
    # Height: ~300px
    cols = 6
    rows = 2
    item_w = 110
    item_h = 110
    gap_x = 10
    gap_y = 10
    
    width = (cols * item_w) + ((cols - 1) * gap_x) + 40 # 40px padding
    height = (rows * item_h) + ((rows - 1) * gap_y) + 40
    
    dwg = svgwrite.Drawing(size=(f"{width}px", f"{height}px"))
    theme_cfg = get_theme_config(theme)
    
    # --- Definitions (Gradients) ---
    def add_grad(id, stops):
        grad = dwg.defs.add(dwg.linearGradient(id=id, x1="0%", y1="0%", x2="100%", y2="100%"))
        for offset, color in stops:
            grad.add_stop_color(offset, color)
        return grad

    # Rank Gradients (Vibrant / Neon - Semantic)
    add_grad("gradSSS", [(0, "#ff00cc"), (1, "#333399")])   # Pink/Purple
    add_grad("gradS",   [(0, "#FFD700"), (1, "#FFA500")])   # Gold
    add_grad("gradA",   [(0, "#E0E0E0"), (1, "#A0A0A0")])   # Silver
    add_grad("gradB",   [(0, "#CD7F32"), (1, "#8B4513")])   # Bronze/Copper
    add_grad("gradC",   [(0, "#B0C4DE"), (1, "#778899")])   # Steel Blue
    add_grad("gradUnknown", [(0, "#4a5568"), (1, "#2d3748")]) # Dark Gray

    # Text Gradients (Dynamic based on theme)
    # Primary Gradient (for Header) -> uses Accent
    add_grad("gradPrimary", [(0, theme_cfg["accent"]), (1, theme_cfg["accent"])]) 
    
    # Secondary Gradient (for Subtitle) -> uses Text color
    add_grad("gradSecondary", [(0, theme_cfg["text"]), (1, theme_cfg["text"])])

    # Background (Use the helper valid for the theme)
    dwg.add(bg_rect(dwg, "100%", "100%", theme_cfg))

    # --- Helper: Draw Vector Trophy Cup ---
    def draw_trophy(insert_x, insert_y, scale=1.0, grad_id="gradS"):
        g = dwg.g(transform=f"translate({insert_x}, {insert_y}) scale({scale})")
        
        # Paths for a classic trophy cup shape
        # 1. Base
        g.add(dwg.path(d="M 25 85 L 75 85 L 70 75 L 30 75 Z", fill=f"url(#{grad_id})"))
        # 2. Stem
        g.add(dwg.path(d="M 42 55 L 58 55 L 55 75 L 45 75 Z", fill=f"url(#{grad_id})"))
        # 3. Bowl (Bezier)
        bowl_d = "M 10 10 L 90 10 C 90 45 75 60 50 60 C 25 60 10 45 10 10 Z"
        g.add(dwg.path(d=bowl_d, fill=f"url(#{grad_id})"))
        
        # 4. Handles (Strokes)
        g.add(dwg.path(d="M 10 15 C -15 15, -15 45, 15 40", 
                       fill="none", stroke=f"url(#{grad_id})", stroke_width=5, stroke_linecap="round"))
        g.add(dwg.path(d="M 90 15 C 115 15, 115 45, 85 40", 
                       fill="none", stroke=f"url(#{grad_id})", stroke_width=5, stroke_linecap="round"))
        
        # 5. Rim highlight
        g.add(dwg.ellipse(center=(50, 10), r=(40, 4), fill="#ffffff", fill_opacity=0.3))

        return g

    # --- Logic ---
    from datetime import datetime
    
    created_at_str = stats.get('created_at', '2020-01-01T00:00:00Z')
    try:
        dt = datetime.strptime(created_at_str, "%Y-%m-%dT%H:%M:%SZ")
        created_year = dt.year
        account_age_years = datetime.now().year - created_year
    except:
        created_year = 2020
        account_age_years = 1

    def get_rank_data(value, thresholds):
        ranks = ["C", "B", "A", "S", "SS", "SSS"]
        # Special case: value might be -1 for "Unknown" or some logic
        rank_idx = 0
        for i, t in enumerate(thresholds):
            if value >= t:
                rank_idx = i + 1
            else:
                break
        if rank_idx >= len(ranks): rank_idx = len(ranks) - 1
        return ranks[rank_idx]

    def get_grad_for_rank(rank):
        mapping = {
            "SSS": "gradSSS", "SS": "gradSSS",
            "S": "gradS", "A": "gradA", "B": "gradB", "C": "gradC", "?": "gradUnknown"
        }
        return mapping.get(rank, "gradC")

    # Categories Configuration (12 Types)
    
    # 1. AchieveSSSRank
    s_rank_val = 1 if stats.get('total_stars', 0) > 1000 else 0
    # 2. MultiLanguage (Mock)
    
    # 3. LongTimeUser
    long_time_val = account_age_years
    
    # 4. NewUser
    is_new_user = 1 if created_year >= 2020 else 0
    
    # 5. AncientUser
    is_ancient = 1 if created_year < 2010 else 0
    
    categories = [
        # Row 1 (6 items)
        {"name": "AchieveSSSRank", "subtitle": "SSS Rank Hacker", "desc": "Have SSS Rank", 
         "value": s_rank_val, "thresh": [0, 0, 0, 0, 1, 1], "force_rank": "S" if s_rank_val else "C"},
         
        {"name": "MultiLanguage", "subtitle": "Rainbow Lang User", "desc": "10+ Langs", 
         "value": stats.get('public_repos', 0), "thresh": [2, 5, 10, 15, 20, 30]},
         
        {"name": "LongTimeUser", "subtitle": "Village Elder", "desc": f"{account_age_years} Years", 
         "value": account_age_years, "thresh": [1, 2, 5, 8, 10, 15]},
         
        {"name": "NewUser", "subtitle": "Everything started...", "desc": "After 2020", 
         "value": is_new_user, "thresh": [0, 0, 0, 1, 1, 1], "force_rank": "S" if is_new_user else "-"},

        {"name": "Repositories", "subtitle": "God Repo Creator", "desc": f"{stats.get('public_repos', 0)} Repos", 
         "value": stats.get('public_repos', 0), "thresh": [5, 20, 50, 100, 200, 500]},
         
        {"name": "Commits", "subtitle": "Super Committer", "desc": f"{stats.get('total_commits', 0)} Commits", 
         "value": int(stats.get('total_commits', 0) if isinstance(stats.get('total_commits'), int) or (isinstance(stats.get('total_commits'), str) and stats.get('total_commits').isdigit()) else 0), 
         "thresh": [100, 500, 2000, 5000, 10000, 20000]},

        # Row 2 (6 items)
        {"name": "Stars", "subtitle": "High Star", "desc": f"{stats.get('total_stars', 0)} Stars", 
         "value": stats.get('total_stars', 0), "thresh": [10, 50, 200, 500, 1000, 2000]},
         
        {"name": "Followers", "subtitle": "Many Friends", "desc": f"{stats.get('followers', 0)} Friends", 
         "value": stats.get('followers', 0), "thresh": [10, 50, 100, 500, 1000, 5000]},
         
        {"name": "Issues", "subtitle": "First Issue", "desc": f"{stats.get('total_issues', 0)} Issues", 
         "value": stats.get('total_issues', 0), "thresh": [10, 50, 100, 200, 500, 1000]},
         
        {"name": "PullRequest", "subtitle": "First Pull", "desc": f"{stats.get('total_prs', 0)} PRs", 
         "value": stats.get('total_prs', 0), "thresh": [10, 50, 100, 200, 500, 1000]},
         
        {"name": "AncientUser", "subtitle": "Unknown", "desc": "Before 2010", 
         "value": is_ancient, "thresh": [0, 0, 0, 1, 1, 1], "force_rank": "?" if not is_ancient else "S"},
         
        {"name": "Organizations", "subtitle": "Unknown", "desc": f"{stats.get('total_orgs', 0)} Orgs", 
         "value": stats.get('total_orgs', 0), "thresh": [1, 2, 5, 10, 20, 50], "force_rank": "?" if stats.get('total_orgs', 0) == 0 else None}
    ]
    
    pad_x = 20
    pad_y = 20

    for i, cat in enumerate(categories):
        if 'force_rank' in cat and cat['force_rank']:
             rank = cat['force_rank']
        else:
             rank = get_rank_data(cat['value'], cat['thresh'])
             
        grad_id = get_grad_for_rank(rank)
        
        row = i // cols
        col = i % cols
        x = pad_x + col * (item_w + gap_x)
        y = pad_y + row * (item_h + gap_y)
        
        cx = x + item_w / 2
        
        # 1. Card Container (Rounded with Border)
        # Border color matches rank or alternating neon
        # Let's use alternating neon pink/cyan for the border aesthetic
        border_color = theme_cfg["border"]
        
        # Dim styling for "Unknown" or not achieved ranks
        if rank in ["?", "-"]:
             border_color = theme_cfg["border"]
             grad_id = "gradUnknown"
        
        # Card Background - Optional: Use slight fill based on theme style
        bg_opacity = 0.3 if theme_cfg.get("style") == "glass" else 0
        dwg.add(dwg.rect(insert=(x, y), size=(item_w, item_h), rx=8, ry=8,
                         fill=theme_cfg["bg_gradient"][0], fill_opacity=bg_opacity, 
                         stroke=border_color, stroke_width=1.5))
        
        # 2. Header Text
        dwg.add(dwg.text(cat['name'], insert=(cx, y + 16), text_anchor="middle",
                         fill="url(#gradPrimary)", font_size="10px", font_weight="bold", font_family=theme_cfg["font"]))
        
        # 3. Trophy (Centered)
        # Shift down a bit to clear header
        t_scale = 0.38
        t_y_pos = y + 22
        dwg.add(draw_trophy(cx - (50*t_scale), t_y_pos, scale=t_scale, grad_id=grad_id))
        
        # 4. Rank Letter
        rank_y = t_y_pos + (35 * t_scale) + 8
        dwg.add(dwg.text(rank, insert=(cx, rank_y), text_anchor="middle",
                         fill=theme_cfg["bg_gradient"][0] if theme == "light" else "#FFFFFF",
                         font_size="12px", font_weight="bold", font_family="Arial",
                         style="text-shadow: 0px 0px 2px rgba(0,0,0,0.5);" if theme != "light" else ""))
        
        # 5. Subtitle
        dwg.add(dwg.text(cat['subtitle'], insert=(cx, y + 82), text_anchor="middle",
                         fill="url(#gradSecondary)", font_size="8.5px", font_weight="bold", font_family=theme_cfg["font"]))
        
        # 6. Description
        # Use theme border color for description if it is visible enough, or text
        dwg.add(dwg.text(cat['desc'], insert=(cx, y + 94), text_anchor="middle",
                         fill=theme_cfg["border"], font_size="8px", font_family=theme_cfg["font"]))

        # 7. Progress Bar
        if rank not in ["?", "-"]:
            bar_w = 60
            bar_h = 3
            bar_x = cx - bar_w/2
            bar_y = y + 102
            dwg.add(dwg.rect(insert=(bar_x, bar_y), size=(bar_w, bar_h), rx=1.5, ry=1.5, fill=theme_cfg["border"], fill_opacity=0.5))
            dwg.add(dwg.rect(insert=(bar_x, bar_y), size=(bar_w * 0.6, bar_h), rx=1.5, ry=1.5, fill=theme_cfg["accent"]))

    return dwg.tostring()
