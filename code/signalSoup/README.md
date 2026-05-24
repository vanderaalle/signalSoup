# Signal Soup

**A computational model exploring emergent communication through semiotic sign functions**

Signal Soup is a multi-agent simulation system that investigates how communicative alignment can emerge among agents without assuming complete code sharing. Unlike traditional models of lexical coordination, Signal Soup models a polylogical, environment-mediated form of interaction where multiple communicative agents (CAgs) modify and respond to a shared communicative environment (CEnv).

## Theoretical Background

### Semiotic Foundations

The model is grounded in semiotic theory, particularly drawing from:

- **Sign Functions**: Following Eco (1976, 1986), each agent builds detector-effector mappings that function as sign relationships. A detector perceives a signal pattern (the signifier), and an effector produces a response signal (the signified).

- **Encyclopedic vs. Dictionary**: Rather than converging on a shared "dictionary" of meanings, agents develop idiosyncratic "encyclopedias"—partially overlapping repertoires of sign functions that enable communication through *sharedness* rather than perfect alignment.

- **Pragmatic Focus**: The meaning of a sign is defined by the response it elicits. Sign functions act as adaptive rules prescribing actions when certain patterns are detected, emphasizing the pragmatic dimension of communication.

### Key Innovations

Signal Soup challenges four common assumptions in lexical coordination models:

1. **Beyond Dyadic Communication**: Models polylogical interaction among multiple agents rather than pairwise exchanges
2. **Environment-Mediated**: Communication occurs through stigmergic modification of a shared environment
3. **No Direct Feedback**: Agents don't receive explicit success/failure signals
4. **Loose Alignment**: Demonstrates that partial code sharing (sharedness) is sufficient for stable communication

## How It Works

### Communicative Environment (CEnv)

The CEnv consists of signals—three-letter words generated from lowercase letters (26³ = 17,576 possible signals). Agents can retrieve signals from and dispatch new signals to this shared space.

### Communicative Agents (CAgs)

Each agent has:
- **Detectors**: Signal patterns it can recognize
- **Effectors**: Signal patterns it can produce
- **Sign Functions**: Learned mappings from detectors to effectors (d → e)
- **Relevance Values**: Integer scores (0-10) indicating the strength of each sign function
- **Limited Memory**: Fixed capacity (default: 10 sign functions)

### Agent Behavior

On each turn, a randomly selected agent:

1. **Retrieves** signals from CEnv
2. **Matches** detectors against signals:
   - **If match found**: Triggers the corresponding effector, replaces the matched signal, and increments the sign function's relevance (+1)
   - **If no match**: Creates a new sign function by randomly linking two signals from CEnv (r = 1)
3. **Memory management**: When memory is full, replaces the weakest sign function

### Emergent Phenomena

Simulations reveal several emergent patterns:

- **Feedback Loops**: Signals that function as both detectors and effectors create self-reinforcing patterns
- **Sharedness**: Approximately 26% of sign functions become shared among multiple agents
- **Type-Token Convergence**: CEnv converges to ~3 tokens per signal type, indicating structured redundancy
- **Circuit Formation**: Interconnected sign functions form autocatalytic-like networks
- **Moderate Synonymy**: Multiple detectors mapping to the same effector enhances network connectivity

## Installation

### Using pip (once published)

```bash
pip install signal-soup
```

### From source

```bash
git clone https://github.com/vanderaalle/signal-soup.git
cd signal-soup
pip install -r requirements.txt
```

## Requirements

- Python 3.7+
- graphviz (for visualization)

Install with:
```bash
pip install graphviz
```

Note: You may also need to install the Graphviz system package:
- **Ubuntu/Debian**: `sudo apt-get install graphviz`
- **macOS**: `brew install graphviz`
- **Windows**: Download from [graphviz.org](https://graphviz.org/download/)

## Quick Start

```python
from signalSoup import Band

# Create a band of 20 agents
band = Band(num_agents=20, word_length=3, memory_length=10, seed=42)

# Run simulation for 2000 turns
for _ in range(2000):
    band.turn()

# Visualize the band
graph = band.plot_band()
graph.render('band_visualization', view=True)

# Get shared sign functions
sign_functions = band.get_sign_function_dict()
shared = {sf: count for sf, count in sign_functions.items() if count > 1}
print(f"Shared sign functions: {len(shared)}/{len(sign_functions)}")

# Visualize sharedness
sharedness_graph = band.plot_sharedness(sign_functions)
sharedness_graph.render('sharedness', view=True)
```

## Examples

See `example.py` for a complete demonstration including:
- Basic simulation setup
- Agent topology visualization
- Band-environment relationships
- Sharedness analysis
- Time-series analysis of type-token ratios

## API Reference

### `CommunicativeAgent`

The basic agent class with detector-effector sign functions.

**Key Methods:**
- `make_sign_functions()`: Initialize random sign functions
- `retrieve(comm_env)`: Perceive the communicative environment
- `count_matches()`: Find detector matches in environment
- `respond(match_dict)`: Emit effector response and reinforce sign function
- `adapt()`: Learn new sign function when no match found
- `plot_agent()`: Visualize agent's internal sign function topology
- `plot_compact_agent()`: Simplified visualization showing signal types and feedback loops

### `Band`

A collection of communicative agents sharing a common environment.

**Parameters:**
- `num_agents` (int): Number of agents in the band (default: 10)
- `word_length` (int): Length of signal words (default: 3)
- `memory_length` (int): Maximum sign functions per agent (default: 10)
- `comm_env_size` (int): Size of shared environment (default: num_agents)
- `seed` (int): Random seed for reproducibility (optional)

**Key Methods:**
- `turn()`: Execute one interaction turn
- `explode()`: Aggregate all sign functions from all agents
- `get_sign_function_dict()`: Get frequency distribution of sign functions
- `plot_band()`: Visualize band structure and environment connections
- `plot_exploded()`: Show all sign functions across all agents
- `plot_sharedness()`: Highlight shared vs. unique sign functions (red = shared)

## Visualization

Signal Soup provides rich visualization capabilities using Graphviz:

### Agent Topology
Shows internal structure of a single agent:
- White labels: Detectors (input patterns)
- Black labels: Effectors (output patterns)
- Red labels: Signals that serve as both detector and effector (feedback loops)
- Edge labels: Relevance values

### Band Visualization
Shows the relationship between agents and environment:
- Green note shapes: Signals in CEnv
- Orange circles: Agents
- Edges: Detector/effector connections to environment

### Sharedness Diagram
Reveals convergent sign functions:
- Red edges: Sign functions shared by multiple agents (with count labels)
- Black edges: Unique sign functions
- Highlights emergent coordination

## Theoretical Implications

Signal Soup demonstrates that:

1. **Sharedness ≠ Complete Alignment**: Communication can be stable with only partial overlap in sign functions
2. **Environment as Medium**: Stigmergic communication through shared environment enables coordination without direct agent-to-agent interaction
3. **Emergent Meaning**: The "meaning" of a signal emerges from the network of sign functions, not from pre-established semantics
4. **Autocatalytic Dynamics**: Feedback loops and circuits resemble autocatalytic sets (Kauffman 1995, 2000), suggesting connections to theories of self-organization
5. **Encyclopedia over Dictionary**: Agents maintain idiosyncratic sign repertoires (Eco's "encyclopedic" competence) rather than converging on universal codes

## Research Applications

Signal Soup is useful for exploring:

- Emergence of communication protocols in multi-agent systems
- Evolution of language without assuming complete code sharing
- Role of environment in shaping communication
- Trade-offs between agent memory and communicative efficiency
- Connections between semiotic theory and complex adaptive systems
- Alternatives to traditional naming games and lexical coordination models

## Citation

If you use Signal Soup in your research, please cite:

```bibtex
@inproceedings{valle2025signalsoup,
  title={Signal Soup: Sharedness vs. code alignment},
  author={Valle, Andrea},
  booktitle={Proceedings of the Evolution of Language Conference},
  year={2025}
}
```

## References

- Eco, U. (1976). *A Theory of Semiotics*. Bloomington: Indiana University Press.
- Eco, U. (1986). *Semiotics and the Philosophy of Language*. Bloomington: Indiana University Press.
- Holland, J. H. (2014). *Complexity: A Very Short Introduction*. Oxford: Oxford University Press.
- Kauffman, S. (1995). *At Home in the Universe*. Oxford: Oxford University Press.
- Steels, L. (2011). Modeling the cultural evolution of language. *Physics of Life Reviews*, 8, 339–356.

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please feel free to submit issues and pull requests.

Areas for potential contribution:
- Additional visualization options
- Performance optimizations for large-scale simulations
- Alternative agent architectures
- Extensions to the model (e.g., signal grounding, spatial environments)
- Statistical analysis tools

## Author

Andrea Valle  
University of Turin  
andrea.valle@unito.it  
https://github.com/vanderaalle

## Acknowledgments

This model builds on theoretical foundations from semiotics (Eco), complex adaptive systems (Holland), and evolutionary linguistics (Steels, Kirby). The implementation was refined with assistance from Claude (Anthropic).
