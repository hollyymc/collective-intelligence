### How does adding adding energy and lifecycle constraints effect the population dynamics compared to the baseline?

#### H<sub>0</sub>: Introducing energy and lifecycle constraints into the baseline model does not significantly effect the population dynamics compared to the baseline model.
#### H<sub>1</sub>: Introducing energy and lifecycle constraints significantly changes population dynamics compared to the the baseline model.

##### Metrics for Comparison

    steps_survived: how long the population persisted 
    final_rabbits, final_foxes: population sizes at termination
    max_rabbits, max_foxes: peak population
    min_rabbits, min_foxes: minimum recorded value 


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

Lifecycle and energy model

    movement_speed=2.0, 
    fox_death_prob=0.0005, 
    fox_hunt_radius=50, 
    rabbit_reproduction_prob=0.001, 
    fox_reproduction_prob=0.05, 
    mating_radius=40.0, 
    fox_start_energy=1000, 
    fox_energy_gain_on_eat=500, 
    rabbit_start_energy=800, 
    rabbit_energy_gain_on_eat=400, 
    rabbit_feed_radius=15, 
    grass_reproduction_prob=0.005, 
    max_age=200, enable_logging=False, 
    enable_recording=False, 
    duration=1000


#### Results 
##### Statistical analysis
**steps_survived** 

    BASELINE: mean = 248.70, SD = 124.07, 95% con inter = [199.62, 297.78]
    LIFECYCLE AND ENERGY: mean = 201.00, SD = 0.00, 95% con inter = [201.00, 201.00]
    T-test p-value = 0.0563
    Mann-Whitney p-value = 0.4723

**final_rabbits**

    BASELINE: mean = 12.59, SD = 23.83, 95% con inter = [3.17, 22.02]
    LIFECYCLE AND ENERGY: mean = 4.76, SD = 5.08, 95% con inter = [2.66, 6.86]
    T-test p-value = 0.1063
    Mann-Whitney p-value = 0.6090

**final_foxes**

    BASELINE: mean = 13.07, SD = 27.29, 95% con inter = [2.28, 23.87]
    LIFECYCLE AND ENERGY: mean = 10.40, SD = 10.48, 95% con inter = [6.07, 14.73]
    T-test p-value = 0.6393
    Mann-Whitney p-value = 0.0191

**max_rabbits**

    BASELINE: mean = 87.33, SD = 33.45, 95% con inter = [74.10, 100.57]
    LIFECYCLE AND ENERGY: mean = 100.00, SD = 0.00, 95% con inter = [100.00, 100.00]
    T-test p-value = 0.0599
    Mann-Whitney p-value = 0.0296

**max_foxes**

    BASELINE: mean = 110.67, SD = 69.69, 95% con inter = [83.10, 138.23]
    LIFECYCLE AND ENERGY: mean = 25.20, SD = 8.79, 95% con inter = [21.57, 28.83]
    T-test p-value = 0.0000
    Mann-Whitney p-value = 0.0000

**min_rabbits**

    BASELINE: mean = 2.93, SD = 4.38, 95% con inter = [1.19, 4.66]
    LIFECYCLE AND ENERGY: mean = 4.60, SD = 4.76, 95% con inter = [2.63, 6.57]
    T-test p-value = 0.1944
    Mann-Whitney p-value = 0.0664

**min_foxes**

    BASELINE: mean = 2.41, SD = 3.47, 95% con inter = [1.04, 3.78]
    LIFECYCLE AND ENERGY: mean = 7.48, SD = 5.77, 95% con inter = [5.10, 9.86]
    T-test p-value = 0.0005
    Mann-Whitney p-value = 0.0001

#### analysis

Overall, the analysis shows that adding energy and lifecycle constraints to the baseline model does affect the population dynamics for some of the metrics.

Steps survived: \
The simulations under the lifecycle-energy configuration tended to end slightly sooner (mean = 201) than the baseline (mean = 248.7). However, the difference was not statistically significant (T-test p = 0.0563; Mann-Whitney p = 0.4723). Thus, while the average duration dropped, this alone doesn’t provide strong evidence for a significant change in survival time.


Final populations (rabbits and foxes): \
Both rabbits and foxes showed somewhat lower mean final populations under the lifecycle-energy model, but only the Mann-Whitney test for foxes was significant (p = 0.0191), suggesting a potential shift in the fox population distribution, even though means were close. Rabbit final populations were lower on average but not significantly so.


Maximum populations: \
There was a clear, significant reduction in the maximum fox population under the lifecycle-energy model (T-test p = 0.0000; Mann-Whitney p = 0.0000), dropping from an average peak of 110.67 to just 25.20. This indicates energy constraints and aging greatly limit how large fox populations can grow.
Interestingly, the maximum rabbit count was higher and fixed at 100 in all lifecycle-energy runs, leading to marginal significance (Mann-Whitney p = 0.0296). This may reflect limits in the simulation rather than genuine biological differences.


Minimum populations: \
The minimum fox population increased significantly under the lifecycle-energy configuration (means rising from 2.41 to 7.48), suggesting that fox numbers do not crash as hard to low levels, pointing to greater population stability. Both the t-test (p = 0.0005) and Mann-Whitney test (p = 0.0001) confirm this effect. Minimum rabbit counts showed no significant differences, though the means trended slightly higher in the lifecycle-energy runs.

Final Statement\
Taken together, these results indicate that adding energy and lifecycle constraints does change the dynamics of the predator-prey system for some of the metrics. Fox populations peak at much lower numbers but remain more stable at their minimum levels under energy constraints and aging. Therefore, we can say that introducing lifecycle and energy constraints into this model controls the extremes in the fox populations. The constraints did not significantly impact the other metrics.


