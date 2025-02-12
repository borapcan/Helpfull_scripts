import numpy as np
from scipy import stats


# Function to perform inverse rank transformation
def inverse_rank_transform(rank, desired_mean=0, desired_std=1):
    Z = stats.norm.ppf((rank - 0.5) / len(rank))
    return desired_mean + desired_std * Z


rank = np.arange(1, 201)  # Generating ranks from 1 to 200
transformed_values = inverse_rank_transform(rank)

print(transformed_values)
