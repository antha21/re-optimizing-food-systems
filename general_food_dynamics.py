# No intervention
import numpy as np
import matplotlib.pyplot as plt

# 1. Define the Global Base Parameters
beta = 0.05       # Population consumption rate per capita
r = 0.25           # Natural resource regeneration rate
K = 1.0           # Natural carrying capacity (Index max = 1.0)
sigma = 0.3       # Regeneration from sustainability investments
p_margin = 2.5    # Profit margin on food sales
c = 0.05          # Base cost to produce food
k1 = 0.7          # Impact of equity investment
mu = 0.05         # Natural decay of equity

# The "Base" constants from our 100-population model
BASE_POP = 100
BASE_D = 80       # Base demand threshold
BASE_k2 = 0.005   # Base equity impact from surplus

# 2. Define the State-Specific Scenarios
scenarios = {
    'Louisiana (High Insecurity)': {
        'pop': 4600000,
        'base_y0': [40.0, 0.9, 10.0, 0.1], # [Base_F, N, Base_C, Eq]
        'alpha': 0.3,
        'gamma': 0.07,
        'base_delta': 0.001,
        'color': 'red'
    },
    'Connecticut (Avg Insecurity)': {
        'pop': 3600000,
        'base_y0': [110.0, 0.75, 85.0, 0.40],
        'alpha': 0.25,
        'gamma': 0.04,
        'base_delta': 0.001,
        'color': 'orange'
    },
     'New Hampshire (Low Insecurity)': {
        'pop': 1400000,
        'base_y0': [130.0, 0.90, 70.0, 0.85], # [Moderate Food, High Nature, High Capital, High Equity]
        'alpha': 0.28,       # Lower crop yield rate
        'gamma': 0.03,       # Lower waste rate
        'base_delta': 0.0002, # Very low environmental degradation
        'color': 'green'
    }
}

# 3. Setup Integration Variables
dt = 0.01  
t = np.arange(0, 50, dt) 
results = {}

# 4. Run the Simulation for Each State
for state_name, params in scenarios.items():
    # Calculate the scaling factor for this specific state
    P = params['pop']
    scale = P / BASE_POP
    
    # Scale the Volume-Based variables (Food, Capital, Demand)
    D = BASE_D * scale
    F_start = params['base_y0'][0] * scale
    C_start = params['base_y0'][2] * scale
    
    # The Indexes (Nature, Equity) remain unscaled (0 to 1)
    N_start = params['base_y0'][1]
    Eq_start = params['base_y0'][3]
    
    # Inversely scale constants interacting with indexes to maintain proportions
    delta = params['base_delta'] / scale
    k2 = BASE_k2 / scale

    # Extract remaining parameters
    alpha = params['alpha']
    gamma = params['gamma']
    
    # Create empty arrays
    F = np.zeros(len(t))
    N = np.zeros(len(t))
    C = np.zeros(len(t))
    Eq = np.zeros(len(t))
    
    # Set initial conditions
    F[0], N[0], C[0], Eq[0] = F_start, N_start, C_start, Eq_start
    
    # Run the Euler Method
    for i in range(1, len(t)):
        up, us, ue = 0.7, 0.02, 0.02    
        
        prev_F, prev_N, prev_C, prev_Eq = F[i-1], N[i-1], C[i-1], Eq[i-1]   
      
        # 1. Calculate how much food can actually be sold
        # It's either the full population demand, or whatever food is left—whichever is smaller.
        actual_sales = min(beta * P, prev_F)

        # 2. Update derivatives (using actual_sales instead of beta * P for revenue)
        dF = alpha * prev_C * prev_N * up - actual_sales - gamma * prev_F
        dN = r * prev_N * (1 - prev_N / K) - delta * prev_F * up + sigma * us
        dC = p_margin * actual_sales - c * prev_F - (us + ue) * prev_C
        dEq = k1 * ue + k2 * max(0, prev_F - D) - mu * prev_Eq
        
        
        # Euler update with max(0, ...) boundary enforcement
        F[i] = max(0, prev_F + (dF * dt))
        N[i] = max(0, prev_N + (dN * dt))
        C[i] = max(0, prev_C + (dC * dt))
        #Eq[i] = max(0, prev_Eq + (dEq * dt))
    
        # Caps Equity at 1.0, while keeping the floor at 0
        Eq[i] = min(1.0, max(0, prev_Eq + (dEq * dt)))        

    # Store results for plotting
    results[state_name] = {'F': F, 'N': N, 'C': C, 'Eq': Eq, 'color': params['color']}

# 5. Generate the Plot
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Food Systems by State: Louisiana, Connecticut, New Hampshire', fontsize=16, fontweight='bold')

variables = [
    ('F', 'Food Production Dynamics', 'Total Food / Biomass (Millions of Units)', axs[0, 0]),
    ('N', 'Natural Resource Health', 'Health Index (0 to 1)', axs[0, 1]),
    ('C', 'Economic Capital', 'Capital (Wealth in Millions)', axs[1, 0]),
    ('Eq', 'Equity Index', 'Equity (0 to 1)', axs[1, 1])
]

for key, title, ylabel, ax in variables:
    for name, data in results.items():
        # For readability, plot Food and Capital in millions (divided by 1,000,000)
        plot_data = data[key] / 1000000 if key in ['F', 'C'] else data[key]
        ax.plot(t, plot_data, label=name, color=data['color'], linewidth=2)
        
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('Time (Years)')
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()