import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

def gaussian_pdf(x, mean, cov):
    """Calculate the probability density function of a Gaussian distribution."""
    d = len(mean)
    norm_const = 1 / np.sqrt((2 * np.pi) ** d * np.linalg.det(cov))
    x_centered = x - mean
    exponent = -0.5 * np.dot(np.dot(x_centered, np.linalg.inv(cov)), x_centered.T)
    return norm_const * np.exp(exponent)

def e_step(X, means, covariances, weights):
    """E-step: calculate responsibilities."""
    n_samples, n_components = X.shape[0], means.shape[0]
    responsibilities = np.zeros((n_samples, n_components))

    for k in range(n_components):
        responsibilities[:, k] = weights[k] * gaussian_pdf(X, means[k], covariances[k])

    # Normalize responsibilities
    responsibilities_sum = responsibilities.sum(axis=1)[:, np.newaxis]
    responsibilities /= responsibilities_sum

    return responsibilities

def m_step(X, responsibilities):
    """M-step: update parameters."""
    n_samples, n_components = responsibilities.shape
    n_features = X.shape[1]

    weights = responsibilities.sum(axis=0) / n_samples
    means = np.dot(responsibilities.T, X) / responsibilities.sum(axis=0)[:, np.newaxis]

    covariances = np.zeros((n_components, n_features, n_features))
    for k in range(n_components):
        x_centered = X - means[k]
        covariances[k] = np.dot(responsibilities[:, k] * x_centered.T, x_centered) / responsibilities[:, k].sum()

    return means, covariances, weights

def em_algorithm(X, n_components, max_iter=100, tol=1e-4):
    """EM algorithm for Gaussian Mixture Model."""
    n_samples, n_features = X.shape

    # Initialize parameters
    weights = np.ones(n_components) / n_components
    means = X[np.random.choice(n_samples, n_components, replace=False)]
    covariances = np.array([np.eye(n_features)] * n_components)

    for iteration in range(max_iter):
        # E-step
        responsibilities = e_step(X, means, covariances, weights)

        # M-step
        means, covariances, weights = m_step(X, responsibilities)

        # Check for convergence
        log_likelihood = np.sum(np.log(np.dot(responsibilities, weights)))
        print(f"Iteration {iteration + 1}, Log-Likelihood: {log_likelihood:.4f}")

        if iteration > 0 and abs(log_likelihood - prev_log_likelihood) < tol:
            print("Convergence reached.")
            break

        prev_log_likelihood = log_likelihood

    return means, covariances, weights, responsibilities

# Example usage
if __name__ == "__main__":
    # Generate synthetic data
    X, _ = make_blobs(n_samples=300, centers=3, cluster_std=0.60, random_state=0)

    # Fit GMM using EM algorithm
    n_components = 3
    means, covariances, weights, responsibilities = em_algorithm(X, n_components)

    # Visualize results
    plt.scatter(X[:, 0], X[:, 1], s=30, cmap='viridis')
    for k in range(n_components):
        plt.scatter(means[k][0], means[k][1], s=100, color='red', marker='x')
    plt.title('Gaussian Mixture Model using EM Algorithm')
    plt.show()
