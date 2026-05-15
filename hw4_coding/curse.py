'''CODING HOMEWORK #4'''
'''Rachel Papirmeister'''
'''UNI: rmp2205'''

import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(8, 4))
ax.set(xlabel='dimensions (m)', ylabel='log(dmax/dmin)', title='dmax/dmin vs. dimensionality')
line_styles = {0: 'ro-', 1: 'b^-', 2: 'gs-', 3: 'cv-'}

# sample sizes taken from article "A Few Useful Things to Know About Machine Learning"
sample_sizes = [10, 100, 1000, 10000]

for idx, num_samples in enumerate(sample_sizes):
    feature_range = range(1, 101)  # d = 1 to 100
    ratios = []

    for num_features in feature_range:
        # generates synthetic data from standard Gaussian distribution
        X = np.random.randn(num_samples, num_features)

        # picks random query point from X
        query_idx = np.random.randint(0, num_samples)
        query_point = X[query_idx]

        # removes query point from X so it's not used in distance calculations
        X = np.delete(X, query_idx, axis=0)

        # calculates Euclidean distances from query point to all other points
        distances = np.linalg.norm(X - query_point, axis=1)

        ratio = np.max(distances) / np.min(distances)
        ratios.append(ratio)

    ax.plot(feature_range, np.log(ratios), line_styles[idx], label=f'N={num_samples:,}', markersize=3)

plt.legend()
plt.tight_layout()
plt.grid(True)
plt.savefig('curse_of_dimensionality.png', dpi=150, bbox_inches='tight')
plt.show()