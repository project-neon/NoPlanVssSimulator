# NoPlanVssSimulator
Simple Neon robot's simulator for IEEE-VSS robots adapted for NoPlan


# Pre-requisites

- Python 3
- Pip

## How to Install

Install NoPlanVssSimulator dependencies:

```
pip install requirements.txt
```

Done! now you have all you need to run NoPlanVssSimulator!

## How to run

Before run make sure you have enable ports 5778 and 5777, these are the sender and receiver ports for UDP connection with NoPlan on simulated mode. In linux you can run ```fuser X/tcp``` being X the ports to make sure tha any process is using (and empty result means enable port).

To run:

```python
python main.py
```

You will see a screen with an empty field with a ball. The simulations needs to have NoPlan messages to start working. Run [NoPlan on Simulated Mode](https://github.com/project-neon/NoPlan).
