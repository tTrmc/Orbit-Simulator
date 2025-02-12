# Orbit Simulator

This is a Python-based orbit simulation built using the `pygame` library. It simulates the motion of planets in our solar system, including the Sun, Earth, Mars, Mercury, Venus, Jupiter, Saturn, Uranus, and Neptune. The simulation allows you to pan and zoom the view to explore the orbits of these celestial bodies.

## Features

- **Realistic Gravitational Simulation**: Planets are influenced by gravitational forces based on Newton's law of universal gravitation.
- **Interactive Controls**:
  - **Panning**: Click and drag to move the view.
  - **Zooming**: Use the mouse wheel to zoom in and out.
- **Orbit Trails**: Each planet leaves a trail showing its orbit over time.
- **Distance Display**: The distance of each planet from the Sun is displayed in kilometers.
- **Pause/Resume**: Pause the simulation to inspect the current state.
- **Dynamic Scaling**: Planets and their orbits are dynamically scaled based on the zoom level.

## Requirements

- Python 3.x
- Pygame library

To install Pygame, run:
```bash
pip install pygame
```

## How to Run

1. Clone or download this repository.
2. Navigate to the project directory.
3. Run the simulation:
   ```bash
   python orbit_simulation.py
   ```

## Controls

- **Left Click + Drag**: Pan the view in the same direction as the mouse movement.
- **Mouse Wheel Up**: Zoom in centered on the cursor.
- **Mouse Wheel Down**: Zoom out centered on the cursor.
- **Space**: Pause/Resume the simulation.
- **Close the Window**: Click the close button or press `Esc` to exit the simulation.

## Code Overview

### Key Components

- **Planet Class**:
  - Represents a celestial body with properties like position, velocity, mass, and color.
  - Calculates gravitational forces and updates positions based on the forces.
  - Draws the planet and its orbit trail.

- **Camera Class**:
  - Manages the view transformation, including panning and zooming.
  - Converts between world coordinates and screen coordinates.

- **Main Loop**:
  - Handles user input (panning, zooming, and pausing).
  - Updates planet positions and redraws the simulation.

### Key Variables

- `SCALE_FACTOR`: Converts astronomical units (AU) to pixels for rendering.
- `TIMESTEP`: Represents the time step for the simulation (1 day per frame).
- `offset_x`, `offset_y`: Track the view offset for panning.
- `dragging`: Tracks whether the user is currently panning.

## Customization

You can modify the simulation by:

- Adding more planets or celestial bodies.
- Adjusting the initial positions, velocities, or masses of the planets.
- Changing the `SCALE_FACTOR` or `TIMESTEP` to alter the simulation speed or scale.

## Example

```python
# Example of adding a new planet
new_planet = Planet("New Planet", -2 * Planet.AU, 0, 3, (255, 0, 0), 5.97219e24)  # Red planet
new_planet.set_velocity(0, 25e3)  # Set initial velocity
planets.append(new_planet)
```

## License

This project is open-source and available under the [MIT License](LICENSE).
