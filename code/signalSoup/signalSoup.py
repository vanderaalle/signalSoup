"""
Signal Soup: A communicative agent simulation system.

This module implements agents that learn detector-effector mappings through
interaction with a shared symbolic environment, exploring emergence of
communication and coordination in multi-agent systems.
"""

import random
from typing import List, Dict, Tuple, Optional, Set
import graphviz


# Constants
ALPHABET_START = 97  # ASCII code for 'a'
ALPHABET_SIZE = 26
MAX_ASSOCIATION_VALUE = 10
MIN_ASSOCIATION_VALUE = 0


class CommunicativeAgent:
    """
    A communicative agent with detector-effector mappings (sign functions).
    
    Agents perceive patterns in the communicative environment (detectors) and respond
    with actions (effectors). They learn through reinforcement: successful matches
    strengthen associations, while weak associations are replaced when memory is full.
    
    Each detector-effector pair represents a sign function: a learned association
    between a perceived signal and a corresponding response.
    """

    def __init__(self, sign_function_num: int = 1, word_length: int = 3, memory_length: int = 10):
        """
        Initialize a communicative agent.
        
        Args:
            sign_function_num: Initial number of detector-effector pairs (sign functions)
            word_length: Length of randomly generated signal words
            memory_length: Maximum number of sign functions to retain
        """
        self.sign_function_num = sign_function_num
        self.detectors: List[str] = []
        self.effectors: List[str] = []
        self.values: List[int] = []
        self.word_length = word_length
        self.memory_length = memory_length
        self.comm_env: Optional[List[str]] = None

    def make_word(self, length: int = 3) -> str:
        """
        Generate a random word of specified length.
        
        Args:
            length: Number of characters in the word
            
        Returns:
            A random lowercase string
        """
        letters = [chr(x) for x in range(ALPHABET_START, ALPHABET_START + ALPHABET_SIZE)]
        return ''.join(random.choice(letters) for _ in range(length))

    def make_sign_functions(self) -> None:
        """Initialize sign functions (detector-effector pairs) with random signals."""
        self.detectors = [self.make_word(self.word_length) for _ in range(self.sign_function_num)]
        self.effectors = [self.make_word(self.word_length) for _ in range(self.sign_function_num)]
        self.values = [MIN_ASSOCIATION_VALUE for _ in range(self.sign_function_num)]
    
    def retrieve(self, comm_env: List[str]) -> None:
        """
        Perceive the communicative environment.
        
        Args:
            comm_env: List of signals in the communicative environment
        """
        self.comm_env = comm_env.copy()

    def count_matches(self) -> Dict[int, List[int]]:
        """
        Find which detectors match signals in the communicative environment.
        
        Returns:
            Dictionary mapping environment indices to lists of matching detector indices
        """
        match_dict = {}
        for env_idx, signal in enumerate(self.comm_env):
            if signal in self.detectors:
                # Find all detector indices that match this signal
                detector_indices = [i for i, detector in enumerate(self.detectors) if detector == signal]
                match_dict[env_idx] = detector_indices
        return match_dict

    def check_and_act(self, match_dict: Dict[int, List[int]]) -> None:
        """
        Decide whether to respond (if matches found) or adapt (learn new sign function).
        
        Args:
            match_dict: Dictionary of matches from count_matches()
        """
        if not match_dict:
            self.adapt()
        else:
            self.respond(match_dict)

    def adapt(self) -> None:
        """
        Learn a new sign function (detector-effector association) from the communicative environment.
        
        If memory is full, replaces the weakest (minimum value) sign function.
        """
        selected_signal = random.choice(self.comm_env)
        
        if len(self.detectors) >= self.memory_length:
            # Find indices with minimum value and replace one randomly
            min_value = min(self.values)
            min_indices = [i for i, value in enumerate(self.values) if value == min_value]
            replace_idx = random.choice(min_indices)
            
            self.detectors[replace_idx] = selected_signal
            self.effectors[replace_idx] = random.choice(self.comm_env)
            self.values[replace_idx] = 1
        else:
            # Add new sign function
            self.detectors.append(selected_signal)
            self.effectors.append(random.choice(self.comm_env))
            self.values.append(1)
        
    def respond(self, match_dict: Dict[int, List[int]]) -> None:
        """
        Emit an effector response based on detected patterns using sign functions.
        
        Randomly selects one match and emits its corresponding effector into
        the communicative environment, then reinforces the sign function (increases its value).
        
        By design, homonymy (one detector linked to multiple effectors) is excluded:
        once a detector matches, its corresponding effector is deterministically selected.
        
        Args:
            match_dict: Dictionary mapping environment indices to detector indices
        """
        # Choose a random matched position in the environment
        env_idx = random.choice(list(match_dict.keys()))
        # Choose a random detector that matched at that position
        detector_idx = random.choice(match_dict[env_idx])
        
        # Emit the corresponding effector
        self.comm_env[env_idx] = self.effectors[detector_idx]
        
        # Reinforce the sign function (capped at maximum)
        self.values[detector_idx] = min(self.values[detector_idx] + 1, MAX_ASSOCIATION_VALUE)

    def remove_zero_values(self) -> None:
        """Remove sign functions with zero value (unused associations)."""
        # Create lists of non-zero sign functions
        filtered = [(d, e, v) for d, e, v in zip(self.detectors, self.effectors, self.values) 
                    if v != MIN_ASSOCIATION_VALUE]
        
        if filtered:
            self.detectors, self.effectors, self.values = zip(*filtered)
            self.detectors = list(self.detectors)
            self.effectors = list(self.effectors)
            self.values = list(self.values)
        else:
            self.detectors = []
            self.effectors = []
            self.values = []
    
    def get_sign_functions(self) -> List[List[str]]:
        """
        Get all sign functions (detector-effector pairs).
        
        Returns:
            List of [detector, effector] pairs
        """
        return [[self.detectors[i], self.effectors[i]] for i in range(len(self.detectors))]

    # PLOTTING METHODS

    def plot_agent(self) -> graphviz.Digraph:
        """
        Visualize agent's sign functions (detector-effector mappings).
        
        Returns:
            Graphviz diagram showing detectors, effectors, and their associations
        """
        dot = graphviz.Digraph(name="agent")
        
        # Create detector subgraph
        detectors_graph = graphviz.Digraph(name="cluster_detectors")
        for i, detector in enumerate(self.detectors):
            detectors_graph.node(str(i), label=str(detector), style='filled', 
                               shape='box', fontcolor='white', fontname='Gill Sans')
        
        # Create effector subgraph
        effectors_graph = graphviz.Digraph(name="cluster_effectors")
        for i, effector in enumerate(self.effectors):
            effectors_graph.node(str(i + len(self.detectors)), label=str(effector), 
                               style='filled', shape='box', fontname='Gill Sans')
        
        # Create edges with values
        for i in range(len(self.detectors)):
            dot.edge(str(i), str(i + len(self.detectors)), 
                    label=f" {self.values[i]}", fontname='Gill Sans')
        
        dot.subgraph(detectors_graph)
        dot.subgraph(effectors_graph)
        return dot

    def plot_topology(self) -> graphviz.Digraph:
        """
        Visualize the network topology of sign functions.
        
        Signals that are both detectors and effectors are highlighted in red,
        indicating feedback loops or recurring patterns in the sign function network.
        
        Returns:
            Graphviz diagram showing sign function topology
        """
        dot = graphviz.Digraph(name="agent")
        dot.graph_attr['rankdir'] = 'LR'
        
        detector_set = set(self.detectors)
        effector_set = set(self.effectors)
        
        # Detectors only (input signals)
        for signal in detector_set - effector_set:
            dot.node(signal, style='filled', shape='box', 
                    fontcolor='white', fontname='Gill Sans')
        
        # Effectors only (output signals)
        for signal in effector_set - detector_set:
            dot.node(signal, style='filled', shape='box', fontname='Gill Sans')
        
        # Both detector and effector (feedback loops) - highlighted in red
        for signal in detector_set & effector_set:
            dot.node(signal, style='filled', shape='box', 
                    fontname='Gill Sans', fontcolor='red')
        
        # Create edges with association values
        for i in range(len(self.detectors)):
            dot.edge(self.detectors[i], self.effectors[i], 
                    fontname='Gill Sans', label=f" {self.values[i]}")
        
        return dot


class Band:
    """
    A collection of communicative agents sharing a common communicative environment.
    
    Agents take turns perceiving and acting on the 'comm_env' - a shared
    list of signals. This creates stigmergic communication where agents influence
    each other through environment modification. Over time, agents may develop
    shared sign functions, representing convergent behavior or emergent coordination.
    """

    def __init__(self, num_agents: int = 10, word_length: int = 3, 
                 memory_length: int = 10, comm_env_size: Optional[int] = None,
                 seed: Optional[int] = None):
        """
        Initialize a band of communicative agents.
        
        Args:
            num_agents: Number of agents in the band
            word_length: Length of signal words (default 3, yielding 26³ = 17,576 possible signals)
            memory_length: Memory capacity for each agent (max sign functions, default 10)
            comm_env_size: Size of shared communicative environment (defaults to num_agents,
                          reflecting the sum of agents' communicative actions)
            seed: Random seed for reproducibility (optional)
        """
        if seed is not None:
            random.seed(seed)
        
        self.agents = [CommunicativeAgent(word_length=word_length, memory_length=memory_length) 
                      for _ in range(num_agents)]
        
        for agent in self.agents:
            agent.make_sign_functions()
        
        if comm_env_size is None:
            comm_env_size = num_agents
        
        # Initialize shared communicative environment with random signals
        self.comm_env = [self.agents[0].make_word(word_length) for _ in range(comm_env_size)]

    def turn(self) -> None:
        """
        Execute one interaction turn: a random agent perceives and acts on the communicative environment.
        """
        agent = random.choice(self.agents)
        agent.retrieve(self.comm_env)
        matches = agent.count_matches()
        agent.check_and_act(matches)
        self.comm_env = agent.comm_env.copy()

    def remove_zero_values(self) -> None:
        """Remove unused sign functions from all agents."""
        for agent in self.agents:
            agent.remove_zero_values()

    def explode(self) -> List[Tuple[str, str]]:
        """
        Aggregate all sign functions (detector-effector pairs) across all agents.
        
        Returns:
            List of (detector, effector) tuples from all agents
        """
        exploded = []
        for agent in self.agents:
            exploded.extend([(detector, effector) 
                           for detector, effector in zip(agent.detectors, agent.effectors)])
        return exploded
    
    def get_sign_function_dict(self) -> Dict[Tuple[str, str], int]:
        """
        Get frequency distribution of sign functions across all agents.
        
        Returns:
            Dictionary mapping (detector, effector) tuples to their occurrence count.
            Counts > 1 indicate shared/convergent sign functions across agents.
        """
        sign_functions = []
        for agent in self.agents:
            sign_functions.extend([tuple(sf) for sf in agent.get_sign_functions()])
        
        # Count occurrences of each unique sign function
        unique_functions = set(sign_functions)
        return {func: sign_functions.count(func) for func in unique_functions}
        
    # PLOTTING METHODS
    
    def plot_band(self, rankdir: str = "LR", format: Optional[str] = None) -> graphviz.Digraph:
        """
        Visualize the band with agents and their connections to the communicative environment.
        
        Args:
            rankdir: Graph layout direction ('LR' for left-right, 'TB' for top-bottom)
            format: Output format for rendering
            
        Returns:
            Graphviz diagram showing agents, environment signals, and their interactions
        """
        graph = graphviz.Digraph(name="band", format=format)
        graph.graph_attr['rankdir'] = rankdir
        graph.graph_attr['color'] = 'red'
        
        # Draw communicative environment signals
        for signal in self.comm_env:
            graph.node(signal, style='filled', shape='note', 
                      fillcolor="darkgreen", fontcolor='white', fontname='Gill Sans')
        
        # Draw agents
        for i, agent in enumerate(self.agents):
            graph.node(str(i), label=str(i), style='filled', shape='circle', 
                      color='black', fillcolor="darkorange", 
                      fontcolor='white', fontname='Gill Sans')
        
        # Draw connections based on sign functions
        for i, agent in enumerate(self.agents):
            # Detector connections (environment -> agent)
            for detector in agent.detectors:
                if detector in self.comm_env:
                    graph.edge(detector, str(i))
            
            # Effector connections (agent -> environment)
            for effector in agent.effectors:
                if effector in self.comm_env:
                    graph.edge(str(i), effector)
        
        return graph

    def plot_exploded(self, exploded: List[Tuple[str, str]]) -> graphviz.Digraph:
        """
        Visualize all sign functions from all agents.
        
        Args:
            exploded: List of (detector, effector) tuples from explode()
            
        Returns:
            Graphviz diagram showing all sign functions
        """
        graph = graphviz.Digraph()
        for detector, effector in exploded:
            graph.node(detector, style='filled', shape='box', 
                      fontcolor='red', fontname='Gill Sans')
            graph.node(effector, style='filled', shape='box', 
                      fontcolor='red', fontname='Gill Sans')
            graph.edge(detector, effector)
        return graph

    def plot_sharedness(self, sign_function_dict: Dict[Tuple[str, str], int]) -> graphviz.Digraph:
        """
        Visualize convergent sign functions across agents.
        
        Sign functions shared by multiple agents are highlighted in red with
        their occurrence count, indicating emergent coordination or communication
        through shared detector-effector associations.
        
        Args:
            sign_function_dict: Dictionary from get_sign_function_dict()
            
        Returns:
            Graphviz diagram highlighting shared vs. unique sign functions
        """
        graph = graphviz.Digraph(engine="dot")
        graph.graph_attr['rankdir'] = 'LR'
        
        for (detector, effector), count in sign_function_dict.items():
            # Shared sign functions (count > 1) are highlighted in red
            if count > 1:
                edge_color = "red"
                label = str(count)
            else:
                edge_color = "black"
                label = ""
            
            graph.node(detector, style='filled', shape='box', 
                      fontcolor="black", fontname='Gill Sans')
            graph.node(effector, style='filled', shape='box', 
                      fontcolor="black", fontname='Gill Sans')
            graph.edge(detector, effector, color=edge_color, 
                      label=label, fontname='Gill Sans', fontcolor=edge_color)
        
        return graph
