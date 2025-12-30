from flask import Blueprint, request, jsonify, Response, current_app
from services.github_service import get_user_data, get_contribution_years
from services.svg_generator import generate_stats_svg, generate_language_svg, generate_streak_svg

api_bp = Blueprint('api', __name__)

@api_bp.route('/stats/<username>', methods=['GET'])
def get_stats(username):
    """
    Returns JSON stats for debugging or custom frontend rendering.
    """
    data = get_user_data(username)
    if not data:
        return jsonify({"error": "User not found or API limits reached"}), 404
    return jsonify(data)

@api_bp.route('/stats/<username>/svg', methods=['GET'])
def get_stats_svg(username):
    """
    Returns an SVG image of the stats card.
    """
    theme = request.args.get('theme', 'default')
    data = get_user_data(username)
    
    if not data:
         # Return an error SVG or text
        return Response('<svg><text>User not found</text></svg>', mimetype='image/svg+xml'), 404
        
    svg_content = generate_stats_svg(data['stats'], theme=theme)
    
    return Response(svg_content, mimetype='image/svg+xml')

@api_bp.route('/languages/<username>/svg', methods=['GET'])
def get_languages_svg(username):
    theme = request.args.get('theme', 'default')
    data = get_user_data(username)
    if not data:
        return Response('<svg><text>User not found</text></svg>', mimetype='image/svg+xml'), 404
    
    svg_content = generate_language_svg(data['languages'], theme=theme)
    return Response(svg_content, mimetype='image/svg+xml')  
    
@api_bp.route('/contributions/<username>', methods=['GET'])
def get_contributions(username):
    # improved implementation pending for full graph, just returning basic data for now
    data = get_contribution_years(username)
    if not data:
         return jsonify({"error": "User not found"}), 404
    return jsonify(data)

@api_bp.route('/streak/<username>/svg', methods=['GET'])
def get_streak_svg(username):
    theme = request.args.get('theme', 'default')
    # Streak data comes from contributions
    data = get_contribution_years(username)
    if not data:
        return Response('<svg><text>User not found</text></svg>', mimetype='image/svg+xml'), 404
    
    svg_content = generate_streak_svg(data, theme=theme)
    return Response(svg_content, mimetype='image/svg+xml')
