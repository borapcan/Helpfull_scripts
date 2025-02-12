import statsmodels.api as sm
import numpy as np

# Given parameters
alpha = 0.05  # Significance level
beta = 0.8  # Desired power
mu_before = 19.73676914 # Mean of the 1st point
mu_after = 24.28175883 # Mean of Menstruation cohort
sigma = 3.5 # Standard deviation

# Effect size (Cohen's d)
effect_size = (mu_before - mu_after) / sigma

# Perform power analysis
power_analysis = sm.stats.TTestIndPower()
sample_size = power_analysis.solve_power(effect_size=effect_size, alpha=alpha, power=beta, alternative='two-sided')

print(f"Required sample size: {sample_size:.2f}")
