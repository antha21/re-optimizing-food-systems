#General Models
import numpy as np
import matplotlib.pyplot as plt

# Define the system parameters
alpha = 0.35      
beta = 0.05       
gamma = 0.02      
P = 100           
r = 0.2           
K = 1.0           
delta = 0.001     
sigma = 0.1       
p_margin = 2.5    
c = 0.05           
k1 = 0.8          
k2 = 0.005        
D = 80            
mu = 0.05         

# Setup Custom Integration (Euler Method)
dt = 0.01  # DECREASED time step size for better mathematical stability
t = np.arange(0, 50, dt)  # Time array from 0 to 50 years

# Create empty arrays to store the results
F = np.zeros(len(t))
N = np.zeros(len(t))
C = np.zeros(len(t))
Eq = np.zeros(len(t))

# Set initial conditions at index 0
F[0] = 100.0
N[0] = 0.9
C[0] = 30.0
Eq[0] = 0.3

# Run the simulation loop step-by-step
for i in range(1, len(t)):
    # Determine the policy levers for the current time
    current_time = t[i-1]

    up, us, ue = 1.0, 0.01, 0.01

    # Get the previous values
    prev_F = F[i-1]
    prev_N = N[i-1]
    prev_C = C[i-1]
    prev_Eq = Eq[i-1]
    
    # 1. Calculate how much food can actually be sold
    # It's either the full population demand, or whatever food is left—whichever is smaller.
    actual_sales = min(beta * P, prev_F)
    
    # 2. Update derivatives (using actual_sales instead of beta * P for revenue)
    dF = alpha * prev_C * prev_N * up - actual_sales - gamma * prev_F        
    dN = r * prev_N * (1 - prev_N / K) - delta * prev_F * up + sigma * us
    dC = p_margin * actual_sales - c * prev_F - (us + ue) * prev_C
    dEq = k1 * ue + k2 * max(0, prev_F - D) - mu * prev_Eq
    
    # Update each state variable SEPARATELY
    # Added max(0, ...) to prevent unphysical negative values!
    F[i] = max(0, prev_F + (dF * dt))
    N[i] = max(0, prev_N + (dN * dt))
    C[i] = max(0, prev_C + (dC * dt))
    Eq[i] = min(1.0, max(0, prev_Eq + (dEq * dt)))
    
# 5. Generate the 4 separate plots
plt.figure(figsize=(8, 4))
plt.plot(t, F, color='blue', linewidth=2)
plt.title('Food Production Dynamics Over Time')
plt.grid(True, alpha=0.3)
plt.xlabel('Time (Years)')
plt.ylabel('Total Food / Biomass')
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t, N, color='green', linewidth=2)
plt.title('Natural Resource Health Over Time')
plt.grid(True, alpha=0.3)
plt.xlabel('Time (Years)')
plt.ylabel('Health Index (0 to 1)')
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t, C, color='gold', linewidth=2)
plt.title('Economic Capital Over Time')
plt.grid(True, alpha=0.3)
plt.xlabel('Time (Years)')
plt.ylabel('Capital (Wealth)')
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t, Eq, color='purple', linewidth=2)
plt.title('Equity Index Over Time')
plt.grid(True, alpha=0.3)
plt.xlabel('Time (Years)')
plt.ylabel('Equity (0 to 1)')
plt.show()
