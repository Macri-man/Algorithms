import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.neural_network import MLPRegressor

# 1. Load and prepare the dataset
digits = load_digits()
X = digits.data  # Features (images flattened into vectors)

# 2. Define and train the autoencoder
autoencoder = MLPRegressor(hidden_layer_sizes=(64,), activation='relu', max_iter=2000)
autoencoder.fit(X, X)

# 3. Obtain the encoded representations (i.e., the output from the hidden layer)
# Here we assume the encoder is the first layer of the MLP model
encoded_data = autoencoder.predict(X)

# 4. Reduce dimensions using PCA for 2D visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(encoded_data)

# 5. Plot the results
plt.figure(figsize=(8, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=digits.target, cmap='viridis', s=50, alpha=0.7)
plt.colorbar()
plt.title("2D PCA of Encoded Data from Autoencoder")
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.show()
