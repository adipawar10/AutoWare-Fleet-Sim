from flask import Flask, jsonify, request
from flask_cors import CORS
from simulation import WarehouseSimulation

app = Flask(__name__)
CORS(app)

sim = WarehouseSimulation()

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(sim.get_state())

@app.route('/tick', methods=['POST'])
def tick():
    sim.update()
    return jsonify({"message": "Simulation updated", "state": sim.get_state()})

@app.route('/toggle_obstacle', methods=['POST'])
def toggle_obstacle():
    data = request.json
    r, c = data.get('r'), data.get('c')
    sim.toggle_obstacle(r, c)
    return jsonify({"message": "Obstacle toggled", "state": sim.get_state()})

if __name__ == '__main__':
    app.run(debug=True, port=5001)