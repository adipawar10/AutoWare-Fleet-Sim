from pathfinding import find_path
from aws_logger import log_telemetry

# Zones
PICKUP_ZONE = (0, 0)
DROPOFF_ZONE = (9, 9)
CHARGING_ZONE = (4, 5)

class Robot:
    def __init__(self, robot_id, start_pos):
        self.id = robot_id
        self.pos = start_pos
        self.battery = 100
        self.state = "IDLE"
        self.target = None
        self.current_path = [] # <--- New: Store the planned path

    def assign_mission(self):
        # Priority 1: Battery
        if self.battery < 20 and self.state != "CHARGING":
            self.state = "CHARGING"
            self.target = CHARGING_ZONE
            return

        # Priority 2: Charge
        if self.state == "CHARGING":
            if self.pos == CHARGING_ZONE:
                self.battery += 10
                if self.battery >= 100:
                    self.battery = 100
                    self.state = "IDLE"
            return

        # Priority 3: Work Loop
        if self.state == "IDLE":
            self.state = "FETCHING"
            self.target = PICKUP_ZONE
            
        elif self.state == "FETCHING" and self.pos == PICKUP_ZONE:
            self.state = "DELIVERING"
            self.target = DROPOFF_ZONE
            
        elif self.state == "DELIVERING" and self.pos == DROPOFF_ZONE:
            self.state = "IDLE"
            self.target = None

    def move(self, obstacles):
        self.assign_mission()

        if self.state == "CHARGING" and self.pos == CHARGING_ZONE:
            self.current_path = []
            return

        if self.target:
            # Calculate the FULL path to the target
            full_path = find_path(self.pos, self.target, obstacles)
            self.current_path = full_path # Store for visualization
            
            # If path exists, take the first step
            if len(full_path) > 0:
                self.pos = full_path[0]
                self.battery -= 1
            else:
                self.current_path = [] # Blocked

class WarehouseSimulation:
    def __init__(self):
        self.grid_size = 10
        self.robots = [
            Robot(1, (9, 0)),
            Robot(2, (0, 9)),
            Robot(3, (5, 5))
        ]
        self.obstacles = [(3, 3), (3, 4), (3, 5), (7, 7), (7, 8)]

    def toggle_obstacle(self, r, c):
        if (r,c) in [PICKUP_ZONE, DROPOFF_ZONE, CHARGING_ZONE]:
            return
        if (r, c) in self.obstacles:
            self.obstacles.remove((r, c))
        else:
            self.obstacles.append((r, c))

    def get_state(self):
        return {
            "grid_size": self.grid_size,
            "robots": [
                {
                    "id": r.id, 
                    "pos": r.pos, 
                    "battery": r.battery, 
                    "state": r.state,
                    "path": r.current_path # <--- Send path to frontend
                } 
                for r in self.robots
            ],
            "obstacles": self.obstacles,
            "zones": {
                "pickup": PICKUP_ZONE, 
                "dropoff": DROPOFF_ZONE,
                "charging": CHARGING_ZONE
            }
        }

    def update(self):
        current_robot_positions = [r.pos for r in self.robots]

        for robot in self.robots:
            dynamic_obstacles = list(self.obstacles)
            for pos in current_robot_positions:
                if pos != robot.pos:
                    dynamic_obstacles.append(pos)
            
            robot.move(dynamic_obstacles)
            
        log_telemetry(self.robots)