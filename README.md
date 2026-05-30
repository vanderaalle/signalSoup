# Signal Soup

**A multi-agent model of emergent communication through semiotic sign functions**

*Signal Soup* investigates how communicative alignment can emerge in a population of agents without assuming shared code. Agents interact exclusively through a shared symbolic environment — reading signals, responding to them, and gradually developing overlapping repertoires of sign functions. The result is not a common dictionary, but a *soup* of partially shared associations that nonetheless sustains stable communication.

Presented at [Evolang 2026](https://evolang2026.github.io/).

---

## Contents

| Path | Description |
|------|-------------|
| [`docs/signalSoup.pdf`](docs/signalSoup.pdf) | Conference paper |
| [Evolang 2026 slides](https://vanderaalle.github.io/signalSoup/presentations/sigSoupPres.html) · [PDF](docs/presentations/sigSoupPres.pdf) | Evolang 2026 presentation |
| [*Inheriting Eco* slides](https://vanderaalle.github.io/signalSoup/presentations/ecoSoupPres.html) · [PDF](docs/presentations/ecoSoupPres.pdf) | Inheriting Eco (Bologna, 2026) presentation |
| [`signalSoup.ipynb`](signalSoup.ipynb) | Main documented notebook — model walkthrough with examples |
| [`simulations.ipynb`](simulations.ipynb) | Simulation experiments — generates figures |
| [`figures/`](figures/) | Figures used in the paper (`sf.pdf`, `10k.pdf`) |
| [`code/signalSoup/`](code/signalSoup/) | Python package (`pip install`) |
| [`agent.drawio.png`](agent.drawio.png) | Agent architecture diagram |
| [`agentsAndEnv.drawio.png`](agentsAndEnv.drawio.png) | Agent–environment interaction diagram |

---

## The Model

A **communicative environment** (CEnv) holds a pool of signals — three-letter words over a 26-letter alphabet (17,576 possible signals). A **band** is a population of agents sharing this environment.

On each turn, a randomly selected agent:
1. Scans CEnv for signals matching its **detectors**
2. If a match is found → fires the paired **effector**, replacing the matched signal in CEnv (and strengthens the association)
3. If no match → borrows two signals from CEnv to form a new **sign function** (detector → effector)

Over time, agents develop idiosyncratic but partially overlapping repertoires. Communication emerges not through full code alignment, but through *sharedness*: a subset of sign functions converge across agents, enabling coordinated behaviour.

Key emergent phenomena:
- **Type-token convergence** — CEnv stabilises around ~3 tokens per signal type
- **Feedback loops** — signals that serve as both detector and effector type
- **Shared sign functions** — ~26% of associations become convergent across agents
- **Autocatalytic circuits** — interconnected sign functions form self-sustaining networks

---

## Quick Start

```python
from signalSoup import Band

b = Band(num_agents=20, word_length=3)

for _ in range(2000):
    b.turn()

# Visualise the band–environment topology
b.plot_band().render('band', view=True)

# Inspect shared sign functions
sf_dict = b.get_sign_function_dict()
shared = {k: v for k, v in sf_dict.items() if v > 1}
print(f"Shared: {len(shared)} / {len(sf_dict)}")

# Visualise sharedness
b.plot_sharedness(sf_dict).render('sharedness', view=True)
```

See [`signalSoup.ipynb`](signalSoup.ipynb) for a full walkthrough.

---

## Installation

```bash
git clone https://github.com/vanderaalle/signalSoup.git
cd signalSoup/code/signalSoup
pip install -r requirements.txt
```

Requires [Graphviz](https://graphviz.org/download/) (system package + Python binding).

---

## Citation

```bibtex
@inproceedings{valle2026signalsoup,
  title     = {Signal Soup: Sharedness vs. code alignment},
  author    = {Valle, Andrea},
  booktitle = {Proceedings of the Evolution of Language Conference (Evolang 2026)},
  year      = {2026}
}
```

---

## Main references

- Eco, U. (1976). *A Theory of Semiotics*. Indiana University Press.
- Holland, J. H. (2014). *Complexity: A Very Short Introduction*. Oxford University Press.
- Kauffman, S. (1995). *At Home in the Universe*. Oxford University Press.
- Steels, L. (2011). Modeling the cultural evolution of language. *Physics of Life Reviews*, 8, 339–356.

---

## Author

**Andrea Valle** — University of Turin
[andrea.valle@unito.it](mailto:andrea.valle@unito.it) · [github.com/vanderaalle](https://github.com/vanderaalle)

MIT License
