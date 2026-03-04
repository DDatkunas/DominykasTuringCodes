import pandas as pd
import numpy as np

data = pd.DataFrame({
    "temperature": [20, 22, 25, 27, 30, 32, 35, 38],
    "ice_cream_sales": [180, 200, 250, 260, 300, 320, 330, 360],
    "rainfall": [120, 100, 80, 75, 60, 55, 30, 10],
    "humidity": [80, 76, 70, 68, 60, 55, 40, 35],
    "soft_drinks_sales": [190, 210, 240, 255, 270, 290, 300, 310]
})

corr_matrix = data.corr()

# Show only lower half to avoid duplication
corr_matrix_lower = corr_matrix.where(np.tril(np.ones(corr_matrix.shape), k=-1).astype(bool))
print("\nLower correlation part:\n", corr_matrix_lower)
