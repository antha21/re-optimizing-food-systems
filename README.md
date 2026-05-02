# Re-Optimizing Food Systems: A Dynamic Analysis of Production, Sustainability, and Equity

**Authors:** Anthony Artino and Sarah Decipeda  
**Institution:** Kent State University, Department of Mathematical Sciences  
**Course:** Modeling Projects (MATH 52039)  

## Project Overview
Modern food systems prioritize production efficiency and economic profit, often at the direct expense of environmental health and equitable distribution. This research project models agriculture as a highly dynamic system, analyzing the mathematical tension between raw economic growth, ecological collapse, and social fairness. 

By utilizing Ordinary Differential Equations (ODEs) and Stochastic Partial Differential Equations (SPDEs), this project simulates the long-term viability of the food architecture. We apply dynamic feedback loops and hypothetical government policies to adjust and improve the systems across three distinct state profiles:
* **Louisiana:** High food insecurity 
* **Connecticut:** Average food insecurity 
* **New Hampshire:** Low food insecurity 

## Interactive Web Platform (Model Playground)
This repository hosts a live, interactive "Model Playground" via GitHub Pages. Visitors can directly engage with the simulations, adjusting intervention parameters and viewing real-time systemic outcomes directly in their browser.

**[Link to Live Project Website]**(https://antha21.github.io/re-optimizing-food-systems/)

### The Mathematical Framework
The interactive models and underlying Python architecture are driven by four linked state variables:
1. **Food Production Dynamics (F):** The agricultural biomass generated to meet population demands.
2. **Natural Resource Health (N):** The limiting biological factor, tracking soil fertility, water availability, and ecological decay.
3. **Economic Capital (C):** The available wealth utilized to fund agricultural operations, sustainability initiatives, and equity programs.
4. **Equity Index (Eq):** A measurement of the fairness of food distribution and general accessibility.

### Simulation Scenarios
* **General ODE Models:** The baseline mathematical foundation observing the food system without government intervention.
* **Immediate Intervention:** A theoretical benchmark measuring the maximum possible effectiveness of instantaneous crisis-response policies.
* **Political Delay:** A realistic model introducing human friction, where legislative drafting, public skepticism, and lobbying create time-lagged responses to ecological and social crises.
* **Spatial Considerations & SPDE Modeling:** A 3D simulation tracking the physical flow of food and capital across a geographic space (a 100-mile highway route) while subjecting the system to unpredictable environmental and market shocks (Geometric Brownian Motion).

---

## Standalone Bonus Section: ODEs 3D
Included in the Model Playground is **ODEs 3D**, an interactive First-Person Shooter (FPS) and scavenger hunt game. 

*Note: This game is a standalone bonus section independent of the bioeconomic simulations.* It focuses solely on the mathematical mechanics of Ordinary Differential Equations. Players select levels and navigate a 3D environment to solve equation-based challenges.
