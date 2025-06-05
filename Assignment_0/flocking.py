from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2
import random

@dataclass
class FlockingConfig(Config):
    # TODO: Modify the weights and observe the change in behaviour.
    alignment_weight: float = 1
    cohesion_weight: float = 1
    separation_weight: float = 2 # higher to stop clustering

    # vi base config also wants:
    mass = 15


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
        self.there_is_no_escape()
        v_align = Vector2()
        v_cohesion = Vector2()
        v_sep = Vector2()

        # get neighbours nearby
        neighbours = list(self.in_proximity_accuracy())
        num_neighbours = len(neighbours)

        # if there are no neighbours, move straight at current velocity
        if num_neighbours == 0:
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
                        v_sep += space.normalize() / (space * space)

            # finish calculations & normalize
            v_align /= num_neighbours
            v_cohesion = (v_cohesion / num_neighbours) - self.pos
            if v_align.length_squared() != 0:
                v_align = v_align.normalize()
            if v_cohesion.length_squared() != 0:
                v_cohesion = v_cohesion.normalize()
            if v_sep.length_squared() != 0:
                v_sep = v_sep.normalize()

            final_alignment = v_align * self.config.alignment_weight
            final_sep = v_sep * self.config.separation_weight
            final_cohesion = v_cohesion * self.config.cohesion_weight

            aim = (final_alignment + final_cohesion + final_sep)

            if aim.length_squared() > 0:
                self.move = self.config.movement_speed * aim.normalize()
        self.pos += self.move

'''
        # alignment (steer toward the average velocity of neighbors) ####
        avg_velocity = Vector2(0, 0)
        for nbr in neighbours:
            avg_velocity += nbr.move
        avg_velocity /= len(neighbours)
        alignment_force = avg_velocity - self.move # steering component

        # separation (steer away from neighbors that are too close)
        # force is stronger the closer neighbours are (base weight on distance)
        separation_force = Vector2(0, 0)
        for nbr in neighbours:
            displacement = self.pos - nbr.pos
            dist = displacement.length()
            if dist > 0:
                separation_force += displacement.normalize() / (dist**2)
        separation_force *= 10

        # Cohesion (steer toward the center of mass of neighbors)
        # Compute average position XN of neighbors
        center_of_mass = Vector2(0, 0)
        for nbr in neighbours:
            center_of_mass += nbr.pos
        center_of_mass /= len(neighbours)
        # Cohesion force
        cohesion_force = (center_of_mass - self.pos) - self.move

        # Combine the three forces (no mass term since we assume Mboid = 1)
        total_force = (
            (self.config.alignment_weight * alignment_force)
            + (self.config.cohesion_weight * cohesion_force)
            + (self.config.separation_weight * separation_force)
        )

        # Update velocity
        self.move += total_force

        # Enforce speed limit (movement_speed) and normalize direction
        speed_limit = self.config.movement_speed
        if self.move.length() > speed_limit:
            self.move = self.move.normalize() * speed_limit

        # update position by new velocity 
        self.pos += self.move  # Xboid = Xboid + Vboid · Δt  (Δt = 1)  :contentReference[oaicite:4]{index=4}

'''
(
    Simulation(
        # TODO: Modify `movement_speed` and `radius` and observe the change in behaviour.
        FlockingConfig(
            image_rotation=True,
            movement_speed=1,
            radius=50,
            alignment_weight=1,
            cohesion_weight=1,
            separation_weight=2)
    )
    .batch_spawn_agents(100, FlockingAgent, images=["images/triangle.png"])
    .run()
)
