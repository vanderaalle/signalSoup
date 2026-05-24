"""
Signal Soup - Usage Examples

This script demonstrates the main features of Signal Soup, including:
- Creating and running simulations
- Visualizing agent topologies
- Analyzing emergent sharedness
- Tracking convergence over time
"""

from signalSoup import CommunicativeAgent, Band
import random

print("=" * 60)
print("Signal Soup - Examples")
print("=" * 60)

# Example 1: Single Agent Exploration
print("\n1. Single Agent Topology")
print("-" * 60)

agent = CommunicativeAgent(sign_function_num=3, word_length=3, memory_length=10)
agent.make_sign_functions()

print(f"Initial sign functions:")
for i in range(len(agent.detectors)):
    print(f"  {agent.detectors[i]} → {agent.effectors[i]} (r={agent.values[i]})")

# Simulate interaction with a simple environment
test_env = [agent.make_word(3) for _ in range(5)]
print(f"\nTest environment: {test_env}")

agent.retrieve(test_env)
matches = agent.count_matches()

if matches:
    print(f"Matches found: {matches}")
    agent.respond(matches)
    print(f"After response, environment: {agent.comm_env}")
else:
    print("No matches - agent will adapt")
    agent.adapt()
    print(f"New sign function added")

# Visualize the agent (uncomment to generate visualization)
# agent_graph = agent.plot_agent()
# agent_graph.render('single_agent', view=True)

# Example 2: Band Simulation
print("\n2. Band Simulation")
print("-" * 60)

# Create a band with 20 agents
band = Band(num_agents=20, word_length=3, memory_length=10, seed=42)

print(f"Band created with {len(band.agents)} agents")
print(f"Initial CEnv: {band.comm_env}")
print(f"Initial CEnv size: {len(band.comm_env)} tokens, {len(set(band.comm_env))} types")

# Run simulation
print("\nRunning 2000 turns...")
for i in range(2000):
    band.turn()
    if (i + 1) % 500 == 0:
        types = len(set(band.comm_env))
        tokens = len(band.comm_env)
        ratio = types / tokens
        print(f"  Turn {i+1}: {types} types / {tokens} tokens = {ratio:.3f}")

print("\nSimulation complete!")
print(f"Final CEnv: {band.comm_env}")
print(f"Final type-token ratio: {len(set(band.comm_env))}/{len(band.comm_env)}")

# Example 3: Sharedness Analysis
print("\n3. Sharedness Analysis")
print("-" * 60)

sign_function_dict = band.get_sign_function_dict()
total_sfs = len(sign_function_dict)
shared_sfs = {sf: count for sf, count in sign_function_dict.items() if count > 1}
num_shared = len(shared_sfs)

print(f"Total unique sign functions: {total_sfs}")
print(f"Shared sign functions (2+ agents): {num_shared} ({100*num_shared/total_sfs:.1f}%)")

print("\nMost shared sign functions:")
sorted_shared = sorted(shared_sfs.items(), key=lambda x: x[1], reverse=True)
for (detector, effector), count in sorted_shared[:5]:
    print(f"  {detector} → {effector}: shared by {count} agents")

# Example 4: Agent-Level Analysis
print("\n4. Individual Agent Analysis")
print("-" * 60)

example_agent = band.agents[0]
print(f"Agent 0 has {len(example_agent.detectors)} sign functions")
print(f"\nSign functions:")
for i in range(len(example_agent.detectors)):
    detector = example_agent.detectors[i]
    effector = example_agent.effectors[i]
    value = example_agent.values[i]
    
    # Check if this is a feedback loop
    is_loop = detector == effector
    loop_marker = " [LOOP]" if is_loop else ""
    
    # Check if in CEnv
    in_env = detector in band.comm_env or effector in band.comm_env
    env_marker = " [in CEnv]" if in_env else ""
    
    print(f"  {detector} → {effector} (r={value}){loop_marker}{env_marker}")

# Visualizations (uncomment to generate)
# print("\n5. Generating Visualizations...")
# print("-" * 60)
# 
# # Visualize the full band
# band_graph = band.plot_band()
# band_graph.render('band_visualization', view=True)
# print("✓ Band visualization saved as 'band_visualization.pdf'")
# 
# # Visualize sharedness
# sharedness_graph = band.plot_sharedness(sign_function_dict)
# sharedness_graph.render('sharedness', view=True)
# print("✓ Sharedness visualization saved as 'sharedness.pdf'")
# 
# # Visualize a single agent
# agent_graph = example_agent.plot_agent()
# agent_graph.render('agent_0_topology', view=True)
# print("✓ Agent topology saved as 'agent_0_topology.pdf'")
# 
# # Compact visualization
# compact_graph = example_agent.plot_compact_agent()
# compact_graph.render('agent_0_compact', view=True)
# print("✓ Compact agent visualization saved as 'agent_0_compact.pdf'")

# Example 5: Time Series Analysis
print("\n5. Time Series Analysis (Convergence)")
print("-" * 60)

print("Running new simulation to track convergence...")
band2 = Band(num_agents=30, word_length=3, memory_length=10, seed=123)

type_token_ratios = []
avg_sign_functions = []
turns = [0, 500, 1000, 2000, 5000, 10000]

for target_turn in turns:
    if target_turn == 0:
        ratio = len(set(band2.comm_env)) / len(band2.comm_env)
        avg_sf = sum(len(agent.detectors) for agent in band2.agents) / len(band2.agents)
    else:
        current = turns[turns.index(target_turn) - 1]
        for _ in range(target_turn - current):
            band2.turn()
        
        ratio = len(set(band2.comm_env)) / len(band2.comm_env)
        avg_sf = sum(len(agent.detectors) for agent in band2.agents) / len(band2.agents)
    
    type_token_ratios.append(ratio)
    avg_sign_functions.append(avg_sf)
    print(f"  Turn {target_turn:5d}: type/token={ratio:.3f}, avg_SF/agent={avg_sf:.2f}")

print("\n" + "=" * 60)
print("Examples complete!")
print("=" * 60)
print("\nTo generate visualizations, uncomment the visualization")
print("section in example.py and ensure Graphviz is installed.")
print("\nFor more information, see README.md")
