import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class LorenzAttractor:
    def __init__(self, sigma=10, rho=28, beta=8/3, x0=0.0, y0=1.0, z0=1.05, t_span=(0, 50), num_points=10000):
        """
        Initialize the Lorenz attractor with the given parameters.
        
        :param sigma: The sigma parameter (default is 10).
        :param rho: The rho parameter (default is 28).
        :param beta: The beta parameter (default is 8/3).
        :param x0, y0, z0: Initial conditions for the system.
        :param t_span: Tuple (t_start, t_end), the time span of the simulation.
        :param num_points: Number of points for time resolution.
        """
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.x0 = x0
        self.y0 = y0
        self.z0 = z0
        self.t_span = t_span
        self.num_points = num_points
        self.solution = None

    def lorenz_system(self, t, state):
        """
        Define the Lorenz system of differential equations.
        
        :param t: Time variable (not used in calculations but required for ODE solver).
        :param state: State of the system [x, y, z].
        :return: Derivative [dx/dt, dy/dt, dz/dt].
        """
        x, y, z = state
        dxdt = self.sigma * (y - x)
        dydt = x * (self.rho - z) - y
        dzdt = x * y - self.beta * z
        return [dxdt, dydt, dzdt]

    def solve(self):
        """
        Solve the Lorenz system using the initial conditions and parameters.
        """
        t_eval = np.linspace(self.t_span[0], self.t_span[1], self.num_points)
        initial_conditions = [self.x0, self.y0, self.z0]
        
        # Use scipy.integrate.solve_ivp to solve the ODE system
        self.solution = solve_ivp(self.lorenz_system, self.t_span, initial_conditions, t_eval=t_eval)

    def plot(self):
        """
        Plot the 3D trajectory of the Lorenz attractor.
        """
        if self.solution is None:
            self.solve()  # Solve the system if not already solved
        
        # Extract the solution data
        t = self.solution.t
        x, y, z = self.solution.y
        
        # Plot the Lorenz attractor in 3D
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x, y, z, lw=0.5, color='b')
        
        ax.set_title("Lorenz Attractor")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.show()

# Example usage
if __name__ == '__main__':
    lorenz = LorenzAttractor(sigma=10, rho=28, beta=8/3, x0=0.0, y0=1.0, z0=1.05, t_span=(0, 50), num_points=10000)
    lorenz.solve()  # Solve the Lorenz system
    lorenz.plot()  # Plot the Lorenz attractor
