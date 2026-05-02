# Political Delay
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
        'intervention_year': 6,  # Acts quickly due to food crisis
        # Louisiana's specific Food Crisis Policy
        'policy_up': 0.8,
        'policy_us': 0.05,
        'policy_ue': 0.05,
        'color': 'red'
    },
    'Connecticut (Avg Insecurity)': {
        'pop': 3600000,
        'base_y0': [110.0, 0.75, 85.0, 0.40],
        'alpha': 0.25,
        'gamma': 0.04,
        'base_delta': 0.001,
        'intervention_year': 22, 
        # Connecticut's specific Environmental Bailout Policy
        'policy_up': 0.4,
        'policy_us': 0.50,
        'policy_ue': 0.10,
        'color': 'orange'
    },
     'New Hampshire (Low Insecurity)': {
        'pop': 1400000,
        'base_y0': [130.0, 0.90, 70.0, 0.85], 
        'alpha': 0.28,       
        'gamma': 0.03,       
        'base_delta': 0.0002, 
        'intervention_year': 30,  
        # New Hampshire's Preventative Maintenance Policy
        'policy_up': 0.5,
        'policy_us': 0.05,
        'policy_ue': 0.05,
        'color': 'green'
    }
}

# 3. Setup Integration Variables
dt = 0.01  
t = np.arange(0, 50, dt) 
results = {}

# 4. Run the Simulation for Each State
for state_name, params in scenarios.items():
    P = params['pop']
    scale = P / BASE_POP
    
    D = BASE_D * scale
    F_start = params['base_y0'][0] * scale
    C_start = params['base_y0'][2] * scale
    N_start = params['base_y0'][1]
    Eq_start = params['base_y0'][3]
    
    delta = params['base_delta'] / scale
    k2 = BASE_k2 / scale
    alpha = params['alpha']
    gamma = params['gamma']
    target_year = params['intervention_year'] 
    
    F = np.zeros(len(t))
    N = np.zeros(len(t))
    C = np.zeros(len(t))
    Eq = np.zeros(len(t))
    
    F[0], N[0], C[0], Eq[0] = F_start, N_start, C_start, Eq_start
    
    policy_triggered = False
    trigger_year = None
    
    for i in range(1, len(t)):
        prev_F, prev_N, prev_C, prev_Eq = F[i-1], N[i-1], C[i-1], Eq[i-1]
        
        # Check against this specific state's intervention year
        if t[i-1] < target_year:
            # Phase 1: High Profit Drive (Default for everyone)
            up, us, ue = 0.7, 0.02, 0.02    
        else:
            # Phase 2: NEW - Pulls the specific policy from the dictionary!
            up = params['policy_up']
            us = params['policy_us']
            ue = params['policy_ue']
            
            # Record the year for the graph
            if not policy_triggered:
                policy_triggered = True
                trigger_year = t[i]
            
        # NEW: Restored the Economic and Equity math fixes so LA survives
        actual_sales = min(beta * P, prev_F)
        
        # Calculate derivatives
        dF = alpha * prev_C * prev_N * up - actual_sales - gamma * prev_F
        dN = r * prev_N * (1 - prev_N / K) - delta * prev_F * up + sigma * us
        dC = p_margin * actual_sales - c * prev_F - (us + ue) * prev_C
        dEq = k1 * ue + k2 * max(0, prev_F - D) - mu * prev_Eq
        
        # Euler update
        F[i] = max(0, prev_F + (dF * dt))
        N[i] = max(0, prev_N + (dN * dt))
        C[i] = max(0, prev_C + (dC * dt))
        
        # Caps Equity at 1.0, while keeping the floor at 0
        Eq[i] = min(1.0, max(0, prev_Eq + (dEq * dt)))

    results[state_name] = {
        'F': F, 'N': N, 'C': C, 'Eq': Eq, 
        'color': params['color'], 
        'trigger': trigger_year
    }

# 5. Generate the Plot with Dynamic Policy Lines
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Hardcoded Policy Interventions by State', fontsize=16, fontweight='bold')

variables = [
    ('F', 'Food Production Dynamics', 'Total Food / Biomass (Millions)', axs[0, 0]),
    ('N', 'Natural Resource Health', 'Health Index (0 to 1)', axs[0, 1]),
    ('C', 'Economic Capital', 'Capital (Wealth in Millions)', axs[1, 0]),
    ('Eq', 'Equity Index', 'Equity (0 to 1)', axs[1, 1])
]

for key, title, ylabel, ax in variables:
    for name, data in results.items():
        # Scale down large numbers for readability on the Y-axis
        plot_data = data[key] / 1000000 if key in ['F', 'C'] else data[key]
        ax.plot(t, plot_data, label=name, color=data['color'], linewidth=2)
        
        # Draw a vertical line exactly where this state's policy kicked in
        if data['trigger'] is not None:
            ax.axvline(data['trigger'], color=data['color'], linestyle=':', alpha=0.8, linewidth=2)
            
    ax.set_title(title, fontsize=12)
    ax.set_xlabel('Time (Years)')
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    
    # Ensure legend only prints state names, not a million policy lines
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='best', fontsize=9)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
