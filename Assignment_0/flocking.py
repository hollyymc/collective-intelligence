from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2

@dataclass
class FlockingConfig(Config):
    # TODO: Modify the weights and observe the change in behaviour.
    alignment_weight: float = 1
    cohesion_weight: float = 1
    separation_weight: float = 1


# class FlockingAgent(Agent[FlockingConfig]): this line stops me running it
class FlockingAgent(Agent):
    # By overriding `change_position`, the default behaviour is overwritten.
    # Without making changes, the agents won't move.
    def change_position(self):
        self.there_is_no_escape()

        # TODO: Modify self.move and self.pos accordingly.

        pairs = self.in_proximity_accuracy()
        neighbours = [agent for agent, dist in pairs]

        # if there are no neighbours, move straight at current velocity
        if not neighbours:
            # cap speed if it exceeds movement speed
            if self.move.length() > self.config.movement_speed:
                self.move = self.move.normalize() * self.config.movement_speed
            # update pos by current velocity
            self.pos += self.move
            return

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
                separation_force += displacement.normalize() / dist

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



(
    Simulation(
        # TODO: Modify `movement_speed` and `radius` and observe the change in behaviour.
        FlockingConfig(image_rotation=True, movement_speed=1, radius=50)
    )
    .batch_spawn_agents(100, FlockingAgent, images=["images/triangle.png"])
    .run()
)
