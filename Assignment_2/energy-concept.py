from dataclasses import dataclass
from vi import Agent, Config, Simulation
from pygame.math import Vector2
import random
import matplotlib.pyplot as plt
import pandas as pd


@dataclass
class LotkaVolterraConfig(Config):
    fox_death_prob: float = 0.01
    fox_hunt_radius: float = 10
    movement_speed: float = 2.0
    rabbit_reproduction_prob: float = 0.005
    fox_start_energy: int = 0
    fox_energy_gain_on_eat: int = 0
    rabbit_start_energy: int = 0
    rabbit_energy_gain_on_eat: int = 0
    rabbit_feed_radius: int = 10
    grass_reproduction_prob: float = 0.005
    duration: int = 15000  # Simulation duration in steps


class PopulationTracker:
    def __init__(self):
        self.data = []
        self.step = 0

    def record(self, simulation):
        """Record current population counts"""
        rabbit_count = sum(1 for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "rabbit")
        fox_count = sum(1 for agent in simulation._agents if hasattr(agent, 'species') and agent.species == "fox")

        self.data.append({
            'step': self.step,
            'rabbits': rabbit_count,
            'foxes': fox_count
        })
        self.step += 1

        # Print every 20 steps to monitor progress
        if self.step % 20 == 0:
            print(f"Step {self.step}: Rabbits={rabbit_count}, Foxes={fox_count}")

        # Check if population is extinct
        if rabbit_count == 0 and fox_count == 0:
            print("Both populations extinct!")
            return True
        elif rabbit_count == 0:
            print("All rabbits extinct!")
            return True
        elif fox_count == 0:
            print("All foxes extinct!")
            return True
        return False

    def plot(self):
        """Create simple population dynamics plot"""
        if not self.data:
            print("No data to plot!")
            return

        df = pd.DataFrame(self.data)
        print(f"Plotting {len(df)} data points...")

        # Create single plot
        plt.figure(figsize=(10, 6))
        plt.plot(df['step'], df['rabbits'], label='Rabbits', color='blue', linewidth=2)
        plt.plot(df['step'], df['foxes'], label='Foxes', color='red', linewidth=2)
        plt.xlabel('Time Steps')
        plt.ylabel('Population Count')
        plt.title('Lotka-Volterra Population Dynamics Over Time')
        plt.legend()
        plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('population_dynamics_energy.png', dpi=300, bbox_inches='tight')
        print("Plot saved as 'population_dynamics_energy.png'")
        plt.show()

        # Print basic statistics
        print(f"\n=== Population Statistics ===")
        print(f"Duration: {len(df)} time steps")
        print(f"Rabbits - Max: {df['rabbits'].max()}, Min: {df['rabbits'].min()}, Final: {df['rabbits'].iloc[-1]}")
        print(f"Foxes - Max: {df['foxes'].max()}, Min: {df['foxes'].min()}, Final: {df['foxes'].iloc[-1]}")

class Grass(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "grass"

    def starting(self):
        self.species = "grass"
        angle = random.uniform(0, 360)
        self.move = Vector2(0, 0).rotate(angle) * 0

    def change_position(self):
        # Move randomly
        pass


class Rabbit(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "rabbit"
        self.energy = self.config.rabbit_start_energy

    def starting(self):
        self.species = "rabbit"
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed

    def change_position(self):
        # Move randomly
        if random.random() < 0.1:
            self.move = self.move.rotate(random.uniform(-30, 30))

        self.pos += self.move
        self.there_is_no_escape()

        # Hunt rabbits
        neighbours = list(self.in_proximity_accuracy())
        for agent, distance in neighbours:
            if hasattr(agent, 'species') and agent.species == "grass":
                if distance <= self.config.rabbit_feed_radius:
                    agent.kill()
                    self.energy += self.config.rabbit_energy_gain_on_eat
                    # self.reproduce() could changed based on if we want rabbits to only reproduce after eating
                    break

        # Reproduction
        if random.random() < self.config.rabbit_reproduction_prob:
            self.reproduce()


class Fox(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "fox"
        self.energy = self.config.fox_start_energy

    def starting(self):
        self.species = "fox"
        self.energy = self.config.fox_start_energy
        angle = random.uniform(0, 360)
        self.move = Vector2(1, 0).rotate(angle) * self.config.movement_speed

    def change_position(self):
        # Check for random death FIRST
        if random.random() < self.config.fox_death_prob:
            self.kill()
            return

        # Hunt rabbits
        neighbours = list(self.in_proximity_accuracy())

        for agent, distance in neighbours:
            if hasattr(agent, 'species') and agent.species == "rabbit":
                if distance <= self.config.fox_hunt_radius:
                    agent.kill()
                    self.energy += self.config.fox_energy_gain_on_eat
                    self.reproduce()
                    break

        # Random movement
        if random.random() < 0.15:
            self.move = self.move.rotate(random.uniform(-45, 45))

        self.pos += self.move
        self.there_is_no_escape()

        # Energy loss and starvation
        # this is the no energy model so we dont want this to run
        if self.config.fox_start_energy > 0:
            self.energy -= 1
            if self.energy <= 0:
                self.kill()


class LotkaVolterraSimulation(Simulation):
    def __init__(self, config):
        super().__init__(config)
        self.tracker = PopulationTracker()
        self.current_step = 0
        self.simulation_ended = False

    def tick(self):
        # Record population every 5 steps
        if self.current_step % 5 == 0:
            extinct = self.tracker.record(self)
            if extinct and not self.simulation_ended:
                print("Population extinct! Generating plot...")
                self.tracker.plot()
                self.simulation_ended = True

        super().tick()
        self.current_step += 1

    def end(self):
        super().end()
        if not self.simulation_ended:
            print("\nSimulation ended normally. Generating plot...")
            self.tracker.plot()


# Run simulation with population tracking
if __name__ == "__main__":
    print("Starting Lotka-Volterra simulation with population tracking...")

    config = LotkaVolterraConfig(
        movement_speed=2.0,
        radius=50,
        fox_death_prob=0.01,
        fox_hunt_radius=40,
        rabbit_reproduction_prob=0.005,
        duration=1000,
        fox_start_energy=0,
        fox_energy_gain_on_eat=0,
        rabbit_start_energy=0,
        rabbit_energy_gain_on_eat=0,
        rabbit_feed_radius=10
    )

    simulation = LotkaVolterraSimulation(config)
    simulation.batch_spawn_agents(50, Rabbit, images=["images/rabbit.png"])
    simulation.batch_spawn_agents(10, Fox, images=["images/fox.png"])
    simulation.batch_spawn_agents(30, Grass, images=["images/grass.png"])
    simulation.run()

    # Ensure plot is generated even if end() wasn't called
    if not simulation.simulation_ended:
        print("Generating final plot...")
        simulation.tracker.plot()