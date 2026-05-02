import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 1. SPDE System Parameters
alpha = 0.35        # Production efficiency
beta = 0.05         # Consumption rate
gamma = 0.02        # Spoilage/Waste
P = 100             # Localized population demand
up = 1.0            # Aggressive production effort
us = 0.02           # Baseline sustainability policy
ue = 0.02           # Baseline equity policy
p_margin = 2.5      # Profit margin
c = 0.05            # Base production cost

# Spatial & Stochastic Parameters
D_F = 5.0           # Food Diffusion coefficient (Supply Chain Infrastructure)
sigma_F = 0.15      # Food Volatility (Weather/Agricultural Shocks)
D_C = 2.0           # Capital Diffusion coefficient (Financial Trade)
sigma_C = 0.05      # Capital Volatility (Market fluctuations)

# 2. Setup the Spatial Grid (Method of Lines)
L = 100.0           # Total physical distance (e.g., 100 miles)
nx = 100            # Number of spatial grid points
dx = L / (nx - 1)   # Spatial step size
x = np.linspace(0, L, nx)

# 3. Setup the Time Domain
T = 20.0            # Total time (Years)
dt = 0.005          # Time step (Must be very small for SPDE stability)
nt = int(T / dt)
time = np.linspace(0, T, nt)

# 4. Initialize State Variables Arrays
F = np.zeros((nt, nx))
C = np.zeros((nt, nx))
N = np.ones(nx) * 0.8   # Assume uniform baseline health initially

# Define Initial Conditions
# Food is highly concentrated in the rural center (x = 50), sparse at edges
F[0, :] = 20 + 80 * np.exp(-0.05 * (x - L/2)**2)

# Capital is highly concentrated in urban edges (x=0, 100), low in rural center
C[0, :] = 80 - 60 * np.exp(-0.05 * (x - L/2)**2)

# 5. Euler-Maruyama Integration with Finite Differences
for i in range(1, nt):
    # Retrieve previous time step
    F_prev = F[i-1, :]
    C_prev = C[i-1, :]
    
    # Calculate the spatial Laplacians using Central Finite Differences
    laplacian_F = np.zeros(nx)
    laplacian_F[1:-1] = (F_prev[2:] - 2 * F_prev[1:-1] + F_prev[:-2]) / (dx**2)
    laplacian_F[0] = (F_prev[1] - F_prev[0]) / (dx**2)
    laplacian_F[-1] = (F_prev[-2] - F_prev[-1]) / (dx**2)
    
    laplacian_C = np.zeros(nx)
    laplacian_C[1:-1] = (C_prev[2:] - 2 * C_prev[1:-1] + C_prev[:-2]) / (dx**2)
    laplacian_C[0] = (C_prev[1] - C_prev[0]) / (dx**2)
    laplacian_C[-1] = (C_prev[-2] - C_prev[-1]) / (dx**2)
    
    # Generate spatial Gaussian White Noise
    dW_F = np.random.normal(0, np.sqrt(dt), nx)
    dW_C = np.random.normal(0, np.sqrt(dt), nx)
    
    # Calculate Deterministic Drift (The ODE part + Diffusion)
    actual_sales = np.minimum(beta * P, F_prev)
    
    drift_F = alpha * C_prev * N * up - actual_sales - gamma * F_prev + D_F * laplacian_F
    drift_C = p_margin * actual_sales - c * F_prev - (us + ue) * C_prev + D_C * laplacian_C
    
    # Calculate Stochastic Diffusion (The Noise part)
    diffusion_F = sigma_F * F_prev * dW_F
    diffusion_C = sigma_C * C_prev * dW_C
    
    # Update the arrays for the next time step
    F[i, :] = F_prev + drift_F * dt + diffusion_F
    C[i, :] = C_prev + drift_C * dt + diffusion_C
    
    # Ensure variables don't drop below absolute zero
    F[i, :] = np.maximum(0, F[i, :])
    C[i, :] = np.maximum(0, C[i, :])

# 6. Generate 3D Surface Plots of the SPDEs
render_step = int(nt / 100)
T_mesh, X_mesh = np.meshgrid(time[::render_step], x)
F_render = F[::render_step, :].T
C_render = C[::render_step, :].T

# PLOT 1: FOOD
fig1 = plt.figure(figsize=(12, 8))
ax1 = fig1.add_subplot(111, projection='3d')
surf1 = ax1.plot_surface(X_mesh, T_mesh, F_render, cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_title('SPDE Simulation: Food Diffusion with Stochastic Market Shocks', fontsize=14, fontweight='bold')
ax1.set_xlabel('Spatial Distance (Miles)', fontsize=12, labelpad=10)
ax1.set_ylabel('Time (Years)', fontsize=12, labelpad=10)
ax1.set_zlabel('Local Food Biomass', fontsize=12, labelpad=10)
fig1.colorbar(surf1, shrink=0.5, aspect=5, label='Food Concentration')
ax1.view_init(elev=35, azim=-125)
fig1.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
plt.show()

# PLOT 2: CAPITAL
fig2 = plt.figure(figsize=(12, 8))
ax2 = fig2.add_subplot(111, projection='3d')
surf2 = ax2.plot_surface(X_mesh, T_mesh, C_render, cmap='plasma', edgecolor='none', alpha=0.9)
ax2.set_title('SPDE Simulation: Capital Diffusion Flowing Inward', fontsize=14, fontweight='bold')
ax2.set_xlabel('Spatial Distance (Miles)', fontsize=12, labelpad=10)
ax2.set_ylabel('Time (Years)', fontsize=12, labelpad=10)
ax2.set_zlabel('Local Capital (Wealth)', fontsize=12, labelpad=10)
fig2.colorbar(surf2, shrink=0.5, aspect=5, label='Capital Concentration')
ax2.view_init(elev=35, azim=-125)
fig2.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
plt.show()