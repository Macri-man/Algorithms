import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import time

# Step 1: Generate synthetic binary classification data
X, y = make_classification(
    n_samples=100,       # number of data points
    n_features=2,        # 2D data for visualization
    n_informative=2,     # both features are useful
    n_redundant=0,       # no redundant features
    n_clusters_per_class=1,
    random_state=np.random.RandomState(int(time.time()))
)

# Step 2: Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=int(time.time())
)

# Step 3: Initialize and train the Perceptron model
model = Perceptron()
model.fit(X_train, y_train)

# Step 4: Predict and evaluate
y_pred = model.predict(X_test)
print("Accuracy on test set:", accuracy_score(y_test, y_pred))

# Step 5: Visualize decision boundary
plt.figure(figsize=(8, 6))

# Plot original data
plt.scatter(X[:, 0], X[:, 1], c=y, cmap='bwr', edgecolor='k', s=50)
plt.title("Perceptron Classification")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")

# Create mesh to plot decision boundary
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(
    np.linspace(x_min, x_max, 200),
    np.linspace(y_min, y_max, 200)
)
Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Contour plot
plt.contourf(xx, yy, Z, alpha=0.2, cmap='bwr')

# Show plot
plt.grid(True)
plt.show()
