import unittest
from pathfinding import get_next_step

class TestAStar(unittest.TestCase):

    def test_straight_line(self):
        """Test if robot moves towards target in empty space"""
        start = (0, 0)
        target = (0, 3)
        obstacles = []
        # Expected: Should move to (0, 1) to get closer to (0, 3)
        next_step = get_next_step(start, target, obstacles)
        self.assertEqual(next_step, (0, 1))

    def test_avoid_obstacle(self):
        """Test if robot goes AROUND a wall"""
        start = (0, 0)
        target = (0, 2)
        # Wall directly in the way at (0, 1)
        obstacles = [(0, 1)] 
        
        next_step = get_next_step(start, target, obstacles)
        
        # It should NOT step into the wall
        self.assertNotEqual(next_step, (0, 1))
        # It SHOULD step to the side, e.g., (1, 0)
        self.assertEqual(next_step, (1, 0))

    def test_stuck_robot(self):
        """Test if robot stays put when completely trapped"""
        start = (0, 0)
        target = (0, 5)
        # Surrounded by walls
        obstacles = [(0, 1), (1, 0)] 
        
        next_step = get_next_step(start, target, obstacles)
        self.assertEqual(next_step, (0, 0)) # Should not move

if __name__ == '__main__':
    unittest.main()