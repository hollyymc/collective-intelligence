# Stage 1: basic aggregation structure

import random
from vi import Agent, Config, Simulation
from vi.util import count

def make_base_config():
    cfg = Config()
    cfg.Tjoin  = 20
    cfg.Tleave = 20
    cfg.D      = 5
    cfg.Pjoin  = staticmethod(lambda n: min(1.0, 0.3 + 0.05 * n))
    cfg.Pleave = staticmethod(lambda n: max(0.0, 0.5 - 0.05 * n))
    return cfg


class Cockroach(Agent):
    """PFSM agent with wandering, joining, still, leaving states."""

    def on_spawn(self) -> None:
        self.state = "wandering"
        self.timer = 0

    def update(self) -> None:
        if self.state == "wandering":
            if self.on_site():
                n = count(self.in_proximity_accuracy())
                if random.random() < self.config.Pjoin(n):
                    self.state = "joining"
                    self.timer = 0

        elif self.state == "joining":
            self.timer += 1
            if self.timer >= self.config.Tjoin:
                self.state = "still"
                self.freeze_movement()

        elif self.state == "still":
            self.timer += 1
            if self.timer % self.config.D == 0:
                n = count(self.in_proximity_accuracy())
                if random.random() < self.config.Pleave(n):
                    self.state = "leaving"
                    self.timer = 0
                    self.continue_movement()

        elif self.state == "leaving":
            self.timer += 1
            if self.timer >= self.config.Tleave:
                self.state = "wandering"
        


if __name__ == "__main__":
    cfg = make_base_config()
    sim = Simulation(cfg)

    w, h        = cfg.window.as_tuple()
    cx, cy      = w // 2, h // 2

    sim.spawn_obstacle("images/frame.png", cx, cy)
    sim.spawn_site("images/site.png", cx - 100, cy)
    sim.spawn_site("images/site.png", cx + 100, cy)

    sim.batch_spawn_agents(50, Cockroach, images=["images/cockroach.png"])
    sim.run()

