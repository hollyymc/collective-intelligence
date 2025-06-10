from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2
import random

@dataclass
class FlockingConfig(Config):
    # TODO: Modify the weights and observe the change in behaviour.
    alignment_weight: float = 1
    cohesion_weight: float = 1.5
    separation_weight: float = 2 # higher to stop clustering
    obstacle_weight: float = 5

# class FlockingAgent(Agent[FlockingConfig]): this line stops me running it
class FlockingAgent(Agent):
    # By overriding `change_position`, the default behaviour is overwritten.
    # Without making changes, the agents won't move.
    def starting(self):
        """
        called when a boid is created
        selects an angle, is normalized and starts the agent moving
        """
        angle = random.uniform(0, 360)
        direction = Vector2(1, 0).rotate(angle).normalize()
        self.move = direction * self.config.movement_speed

    def change_position(self):
        v_align = Vector2()
        v_cohesion = Vector2()
        v_sep = Vector2()
        v_obstacle = Vector2()

        # get neighbours nearby
        neighbours = list(self.in_proximity_accuracy())
        num_neighbours = len(neighbours)

        # obstacle avoidance
        obstacle_intersections = list(self.obstacle_intersections())
        if obstacle_intersections:
            for intersection in obstacle_intersections:
                avoid_direction = self.pos - intersection
                if avoid_direction.length_squared() > 0:
                    v_obstacle += avoid_direction.normalize()

        # if there are no neighbours, move straight at current velocity
        if num_neighbours == 0:
            # add obstacle avoidance
            if v_obstacle.length_squared() > 0:
                v_obstacle = v_obstacle.normalize()
                self.move += v_obstacle * self.config.obstacle_weight
            
            # cap speed if it exceeds movement speed
            if self.move.length() > self.config.movement_speed:
                self.move = self.move.normalize() * self.config.movement_speed
            # update pos by current velocity
            self.pos += self.move
            return
        else:
            for n, dist in neighbours:
                # for alignment, sum the neighbouring boids velocities
                v_align += n.move
                # for cohesion sum the positions
                v_cohesion += n.pos
                # for seperation, move boids that are too close away
                if dist < 25:
                    space = self.pos - n.pos
                    if space.length_squared() > 0:
                        # inverse square repulsion is stroger when the boids are closer
                        v_sep += space.normalize() / (dist * dist + 1)

            # finish calculations & normalize
            v_align /= num_neighbours
            v_cohesion = (v_cohesion / num_neighbours) - self.pos
            if v_align.length_squared() != 0:
                v_align = v_align.normalize()
            if v_cohesion.length_squared() != 0:
                v_cohesion = v_cohesion.normalize()
            if v_sep.length_squared() != 0:
                v_sep = v_sep.normalize()
            if v_obstacle.length_squared() > 0:
                v_obstacle = v_obstacle.normalize()

            final_alignment = v_align * self.config.alignment_weight
            final_sep = v_sep * self.config.separation_weight
            final_cohesion = v_cohesion * self.config.cohesion_weight
            final_obstacle = v_obstacle * self.config.obstacle_weight

            aim = (final_alignment + final_cohesion + final_sep + final_obstacle)

            if aim.length_squared() > 0:
                self.move = self.config.movement_speed * aim.normalize()
        self.pos += self.move

def create_simulation_base():
    return Simulation(
        FlockingConfig(
            image_rotation=True,
            movement_speed=1.75,
            radius=50,
            alignment_weight=1,
            cohesion_weight=1,
            separation_weight=2,
            obstacle_weight=5)
    ).batch_spawn_agents(100, FlockingAgent, images=["images/triangle.png"])

def u_shape():
    sim = create_simulation_base()
    # Left side of U
    for y in range(150, 550, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", 200, y)
    # Bottom of U
    for x in range(250, 550, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", x, 500)
    # Right side of U
    for y in range(150, 550, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", 550, y)
    return sim

def x_shape():
    sim = create_simulation_base()
    # Diagonal from top-left to bottom-right
    for i in range(8):
        x = 200 + i * 50
        y = 150 + i * 50
        sim = sim.spawn_obstacle("images/triangle@50px.png", x, y)
    # Diagonal from top-right to bottom-left
    for i in range(8):
        x = 550 - i * 50
        y = 150 + i * 50
        sim = sim.spawn_obstacle("images/triangle@50px.png", x, y)
    return sim

def vertical_line():
    sim = create_simulation_base()
    for y in range(100, 650, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", 375, y)
    return sim

def square():
    sim = create_simulation_base()
    # Top and bottom
    for x in range(250, 500, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", x, 200)
        sim = sim.spawn_obstacle("images/triangle@50px.png", x, 450)
    # Left and right
    for y in range(250, 401, 50):
        sim = sim.spawn_obstacle("images/triangle@50px.png", 250, y)
        sim = sim.spawn_obstacle("images/triangle@50px.png", 450, y)
    return sim

# Choose which simulation to run
choice = "square"  # Change to "x", "line", or "square"

if choice == "u":
    u_shape().run()
elif choice == "x":
    x_shape().run()
elif choice == "line":
    vertical_line().run()
elif choice == "square":
    square().run()