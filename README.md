# Neural-Network-Driven-Path-Tracking-Control-for-Autonomous-Planar-Vehicles
## Overview

This project simulates a car navigating a 2D map using **ray sensors** and a **reinforcement learning environment**. The car “sees” its surroundings through five distance rays and can take discrete actions like turning or changing speed. The goal is to train a neural network (or use NEAT/DQN) to **drive the car autonomously without crashing**.

---

## Features

* **2D PyGame simulation** with a car and background map.
* **Ray-based sensors** for detecting walls (like lidar).
* **Discrete action space**:

  | Action | Description        |
  | ------ | ------------------ |
  | 0      | Coast (do nothing) |
  | 1      | Turn left          |
  | 2      | Turn right         |
  | 3      | Speed up           |
  | 4      | Slow down          |
* **Environment class (`DrivingEnv`)**:

  * Returns normalized ray distances as state.
  * Computes reward and detects collisions.
* **Reward shaping**:

  * +1 for being alive
  * -0.5 if too close to walls
  * -10 for collisions
* **Reset and episode handling**: Car resets to starting position `(830, 930)` on crash.

---

## Installation

1. Install Python 3.8+
2. Install required packages:

```bash
pip install pygame numpy
```

3. Make sure you have a map image named `map5.png` in the project folder.

---

## How to Run

```bash
python project.py
```

* Use arrow keys to manually control the car:

  * Up: accelerate
  * Down: decelerate
  * Left/Right: turn
* Press `ESC` to exit.

---

## Reinforcement Learning Integration

1. The `DrivingEnv` class allows easy integration with **DQN or NEAT**.
2. It exposes:

   * `env.get_state()` → normalized ray distances
   * `env.step(action)` → returns `(next_state, reward, done)`
3. Network input: 5 normalized ray distances
4. Network output: 5 Q-values (one per action)

---

## Next Steps

* Implement a **DQN agent** to learn driving behavior using the environment.
* Track **reward vs. episode** and **ε-greedy exploration**.
* Experiment with **different reward shaping** to improve performance.
* Add more **ray sensors or speed/angle info** for more sophisticated control.

---

## Credits

* **PyGame** – game simulation and graphics.
* **Concepts inspired by NEAT and DQN tutorials**.

---

