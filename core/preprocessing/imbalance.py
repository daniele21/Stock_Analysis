from imblearn.over_sampling import SMOTE
import numpy as np


def smote_oversampling(x: np.array,
                       y: np.array,
                       random_state: int,
                       k_neighbors: int = 5):

    smote = SMOTE(random_state=random_state,
                  k_neighbors=k_neighbors)
    x_smote, y_smote = smote.fit_resample(x, y)

    return x_smote, y_smote




