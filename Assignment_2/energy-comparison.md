### How does adding energy constraints affect population dynamics compared to the baseline model?
_note 1: there are graphs for each metric saved in Assignment_2/results/energy_

_note 2: the duration was set to 1500 time steps but the simulations all ended early due to extinction_

#### H<sub>0</sub>: Introducing energy constraints into the baseline model does not significantly affect the population dynamics compared to the baseline model.
#### H<sub>1</sub>: Introducing energy constraints significantly changes population dynamics compared to the baseline model.

##### Metrics for Comparison

    steps_survived: how long the population persisted 
    final_rabbits, final_foxes: population sizes at termination
    max_rabbits, max_foxes: peak population
    min_rabbits, min_foxes: minimum recorded value (excl. 0 possibly)


##### Parameters
Baseline model

    movement_speed=2.0, 
    radius=50,
    fox_death_prob=0.01, 
    fox_hunt_radius=40,
    rabbit_reproduction_prob=0.005,
    duration=15000,
    fox_start_energy=0,
    fox_energy_gain_on_eat=0

Energy model

    movement_speed=2.0,
    radius=50,
    fox_death_prob=0.01,
    fox_hunt_radius=40,
    rabbit_reproduction_prob=0.005,
    duration=15000,
    fox_start_energy=0,
    fox_energy_gain_on_eat=0,
    rabbit_start_energy=0,
    rabbit_energy_gain_on_eat=0,
    rabbit_feed_radius=10


#### Results 
##### Statistical analysis
**steps_survived** 

    BASELINE: mean = 248.70, SD = 124.07, 95% con inter = [199.62, 297.78]
    ENERGY: mean = 273.40, SD = 151.02, 95% con inter = [211.06, 335.74]
    T-test p-value = 0.5244
    Mann-Whitney p-value = 0.5215

**final_rabbits**

    BASELINE: mean = 12.59, SD = 23.83, 95% con inter = [3.17, 22.02]
    ENERGY: mean = 24.12, SD = 32.25, 95% con inter = [10.81, 37.43]
    T-test p-value = 0.1524
    Mann-Whitney p-value = 0.1703

**final_foxes**

    BASELINE: mean = 13.07, SD = 27.29, 95% con inter = [2.28, 23.87]
    ENERGY: mean = 9.32, SD = 18.95, 95% con inter = [1.50, 17.14]
    T-test p-value = 0.5650
    Mann-Whitney p-value = 0.6557

**max_rabbits**

    BASELINE: mean = 87.33, SD = 33.45, 95% con inter = [74.10, 100.57]
    ENERGY: mean = 92.44, SD = 35.42, 95% con inter = [77.82, 107.06]
    T-test p-value = 0.5961
    Mann-Whitney p-value = 0.6404

**max_foxes** 

    BASELINE: mean = 110.67, SD = 69.69, 95% con inter = [83.10, 138.23]
    ENERGY: mean = 115.60, SD = 81.84, 95% con inter = [81.82, 149.38]
    T-test p-value = 0.8167
    Mann-Whitney p-value = 1.0000

**min_rabbits**

    BASELINE: mean = 2.93, SD = 4.38, 95% con inter = [1.19, 4.66]
    ENERGY: mean = 3.36, SD = 3.52, 95% con inter = [1.91, 4.81]
    T-test p-value = 0.6946
    Mann-Whitney p-value = 0.3761

**min_foxes**

    BASELINE: mean = 2.41, SD = 3.47, 95% con inter = [1.04, 3.78]
    ENERGY: mean = 1.20, SD = 2.38, 95% con inter = [0.22, 2.18]
    T-test p-value = 0.1475
    Mann-Whitney p-value = 0.3081

##### about the stats
Overall, the analysis shows that there are no significant differences between the baseline and energy models for any of the measured metrics.

_steps_survived_: \
The avg number of steps the simulation survived was slightly higher in the energy model (273.4) compared to the baseline (248.7). \
But, the large standard deviations and high p-values (t test: 0.5244, mann whitney: 0.5215) suggest this difference is not statistically significant.   
The variation between runs is large enough that this increase could be random.

_final_rabbit and final_fox_: \
Both models ended with highly variable rabbit and fox populations. e.g. in the baseline, final rabbit counts ranged from 0 to 115, and in the energy model, from 0 to 123. 
Despite the higher mean in the energy model, the overlapping confidence intervals and non-significant p-values suggest that this is not a statistically significant difference.

_min_{agent} and _max_{agent}: \
The min and max agent counts fluctuated similarly to the final populations. T
These are sensitive to short-term spikes or crashes. \
The fact that these metrics didn't differ significantly suggests that the overall population dynamics were not substantially changed by the introduction of energy parameters.

confidence intervals: \
All the confidence intervals for in both models overlap significantly. \
This means that even if one model has a slightly higher mean, that doesn't necessarilty mean it will hold across repeated simulations. \
This is another reason to not reject the null hypothesis.

non-parametric test (mann whitney): \
This test does not assume normality and was included to confirm the robustness of the t-test results. \
It also found no significant differences, which again is a reason to not reject the null hypothesis.


**final:** adding energy constraints did not have a statistically significant effect on how long populations survived, or on the population sizes at any point in time. \
This suggests that the energy constraints that were implemented here did not alter the dynamics of the predator-prey interaction in a significant way.

