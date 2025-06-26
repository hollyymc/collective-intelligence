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
    duration: int = 15000  # Simulation duration in steps


class PopulationTracker:
    def __init__(self):
        self.data = []
        self.step = 0
        self.summary = {}

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
        filename= f'population_dynamics_run_{self.run_id or "unknown"}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"Plot saved as '{filename}'")
        plt.show()

        # Print basic statistics
        print(f"\n=== Population Statistics ===")
        print(f"Duration: {len(df)} time steps")
        print(f"Rabbits - Max: {df['rabbits'].max()}, Min: {df['rabbits'].min()}, Final: {df['rabbits'].iloc[-1]}")
        print(f"Foxes - Max: {df['foxes'].max()}, Min: {df['foxes'].min()}, Final: {df['foxes'].iloc[-1]}")

    def create_summary(self):
        df = pd.DataFrame(self.data)
        self.summary["steps_survived"] = len(df)
        self.summary["final_rabbits"] = df['rabbits'].iloc[-1]
        self.summary["final_foxes"] = df['foxes'].iloc[-1]
        self.summary["max_rabbits"] = df['rabbits'].max()
        self.summary["max_foxes"] = df['foxes'].max()
        self.summary["min_rabbits"] = df['rabbits'].min()
        self.summary["min_foxes"] = df['foxes'].min()

    def get_summary(self):
        return self.summary


class Rabbit(Agent):
    def __init__(self, images, simulation, pos=None, move=None):
        super().__init__(images, simulation, pos, move)
        self.species = "rabbit"

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
                self.tracker.create_summary()
                self.simulation_ended = True

        super().tick()
        self.current_step += 1

    def end(self):
        super().end()
        if not self.simulation_ended:
            print("\nSimulation ended normally. Generating plot...")
            self.tracker.plot()
            self.tracker.create_summary()


def run_simulation_once(seed=None):
    if seed is not None:
        random.seed(seed)

    config = LotkaVolterraConfig(
        movement_speed=2.0,
        radius=50,
        fox_death_prob=0.01,
        fox_hunt_radius=40,
        rabbit_reproduction_prob=0.005,
        duration=15000,
        fox_start_energy=0,
        fox_energy_gain_on_eat=0
    )

    simulation = LotkaVolterraSimulation(config)
    simulation.batch_spawn_agents(50, Rabbit, images=["images/rabbit.png"])
    simulation.batch_spawn_agents(10, Fox, images=["images/fox.png"])
    simulation.run()

    return simulation.tracker.get_summary()

# Run simulation with population tracking
if __name__ == "__main__":
    print("Starting Lotka-Volterra simulation with population tracking...")

    num_runs = 27
    results = []

    for i in range(num_runs):
        print(f"\n--- Simulation {i + 1} ---")
        summary = run_simulation_once(seed=i)
        summary['run'] = i + 1
        results.append(summary)

    # create df and save
    df_results = pd.DataFrame(results)
    df_results.to_csv("baseline_results.csv", index=False)
    print("\nSaved all run results to 'baseline_results.csv'.")


    #simulation.run()


