import os
import sys

# Add backend directory to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from services.svg_generator import generate_stats_svg

# Mock stats data
mock_stats = {
    'username': 'testuser',
    'name': 'Test User',
    'total_stars': 100,
    'total_commits': 500,
    'public_repos': 10,
    'followers': 50
}

def verify_theme(theme_name, expected_color):
    print(f"Testing theme: {theme_name}...")
    try:
        svg_content = generate_stats_svg(mock_stats, theme=theme_name)
        if expected_color in svg_content:
            print(f"SUCCESS: {theme_name} generated with expected color {expected_color}.")
        else:
            print(f"FAILURE: {theme_name} NOT generated with expected color {expected_color}.")
    except Exception as e:
        print(f"ERROR generating {theme_name}: {e}")

# Test a few new themes
verify_theme('dracula', '#282a36') # BG color
verify_theme('monokai', '#272822') # BG color
verify_theme('nord', '#88c0d0')    # Accent color
