"""
Simple Flask API for route optimization using a Dijkstra-based route planner.
Run with:
    python api_server.py

Then use:
    POST http://localhost:5000/optimize
    POST http://localhost:5000/route-map
"""

from flask import Flask, request, jsonify, Response
import traceback

from route_optimizer import optimize_route
from map_builder import build_route_map

app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'route-optimization',
    })


@app.route('/optimize', methods=['POST'])
def optimize():
    try:
        data = request.get_json(force=True)
        start = data.get('start')
        end = data.get('end')
        via = data.get('via', [])
        mode = data.get('mode', 'distance')

        if not start or not end:
            return jsonify({'error': 'Missing required fields: start, end'}), 400
        if mode not in ('distance', 'time'):
            return jsonify({'error': 'mode must be either "distance" or "time"'}), 400

        result = optimize_route(start=start, end=end, via=via, mode=mode)
        return jsonify({'success': True, 'route': result})
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
        }), 500


@app.route('/route-map', methods=['POST'])
def route_map():
    try:
        data = request.get_json(force=True)
        start = data.get('start')
        end = data.get('end')
        via = data.get('via', [])
        mode = data.get('mode', 'distance')

        if not start or not end:
            return jsonify({'error': 'Missing required fields: start, end'}), 400
        if mode not in ('distance', 'time'):
            return jsonify({'error': 'mode must be either "distance" or "time"'}), 400

        result = optimize_route(start=start, end=end, via=via, mode=mode)
        map_html = build_route_map(result['best_path'])
        return Response(map_html, mimetype='text/html')
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'available_endpoints': ['/health', '/optimize', '/route-map'],
    }), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
