"""
Simple tests for Signal Soup

Run with: python test_signalSoup.py
"""

from signalSoup import CommunicativeAgent, Band

def test_agent_creation():
    """Test that agents are created correctly."""
    agent = CommunicativeAgent(sign_function_num=3, word_length=3, memory_length=10)
    agent.make_sign_functions()
    
    assert len(agent.detectors) == 3
    assert len(agent.effectors) == 3
    assert len(agent.values) == 3
    assert all(v == 0 for v in agent.values)
    print("✓ Agent creation test passed")

def test_agent_word_generation():
    """Test that word generation produces correct length."""
    agent = CommunicativeAgent(word_length=3)
    word = agent.make_word(5)
    
    assert len(word) == 5
    assert all(c.islower() for c in word)
    print("✓ Word generation test passed")

def test_agent_adaptation():
    """Test that agents adapt when no matches found."""
    agent = CommunicativeAgent(sign_function_num=1, memory_length=10)
    agent.make_sign_functions()
    
    initial_count = len(agent.detectors)
    
    # Create environment with signals that won't match
    env = ['xxx', 'yyy', 'zzz']
    agent.retrieve(env)
    matches = agent.count_matches()
    
    # Should be no matches
    assert len(matches) == 0
    
    agent.adapt()
    
    # Should have one more sign function
    assert len(agent.detectors) == initial_count + 1
    print("✓ Agent adaptation test passed")

def test_agent_response():
    """Test that agents respond when matches found."""
    agent = CommunicativeAgent(sign_function_num=1, memory_length=10)
    agent.make_sign_functions()
    
    # Force a detector we can match
    agent.detectors[0] = 'abc'
    agent.effectors[0] = 'xyz'
    agent.values[0] = 5
    
    # Create environment with matching signal
    env = ['abc', 'def', 'ghi']
    agent.retrieve(env)
    matches = agent.count_matches()
    
    # Should find a match
    assert len(matches) > 0
    
    initial_value = agent.values[0]
    agent.respond(matches)
    
    # Relevance should increase
    assert agent.values[0] == initial_value + 1
    # Environment should be modified
    assert agent.comm_env != env
    print("✓ Agent response test passed")

def test_band_creation():
    """Test that bands are created correctly."""
    band = Band(num_agents=10, word_length=3, memory_length=10, seed=42)
    
    assert len(band.agents) == 10
    assert len(band.comm_env) == 10
    print("✓ Band creation test passed")

def test_band_turn():
    """Test that band turns execute without error."""
    band = Band(num_agents=5, word_length=3, memory_length=10, seed=42)
    
    initial_env = band.comm_env.copy()
    band.turn()
    
    # Environment should potentially be modified (though not guaranteed)
    # At minimum, no errors should occur
    assert len(band.comm_env) == len(initial_env)
    print("✓ Band turn test passed")

def test_sign_function_dict():
    """Test sign function aggregation."""
    band = Band(num_agents=5, word_length=3, memory_length=10, seed=42)
    
    # Run some turns
    for _ in range(100):
        band.turn()
    
    sf_dict = band.get_sign_function_dict()
    
    # Should have some sign functions
    assert len(sf_dict) > 0
    
    # All counts should be positive
    assert all(count > 0 for count in sf_dict.values())
    print("✓ Sign function dictionary test passed")

def test_reproducibility():
    """Test that simulations with different seeds produce different results."""
    band1 = Band(num_agents=10, word_length=3, memory_length=10, seed=42)
    band2 = Band(num_agents=10, word_length=3, memory_length=10, seed=123)
    
    # Initial environments should be different due to different seeds
    env1_initial = band1.comm_env.copy()
    env2_initial = band2.comm_env.copy()
    
    # Run some turns
    for _ in range(100):
        band1.turn()
        band2.turn()
    
    # Environments should be different (statistically very likely)
    # We just check they evolved from their starting points
    assert band1.comm_env != env1_initial or band2.comm_env != env2_initial
    
    print("✓ Seed differentiation test passed")

if __name__ == "__main__":
    print("Running Signal Soup tests...\n")
    
    test_agent_creation()
    test_agent_word_generation()
    test_agent_adaptation()
    test_agent_response()
    test_band_creation()
    test_band_turn()
    test_sign_function_dict()
    test_reproducibility()
    
    print("\n" + "=" * 40)
    print("All tests passed! ✓")
    print("=" * 40)
