import pygame
import math
from typing import List, Tuple

# Constants
WIDTH, HEIGHT = 1000, 1000
BACKGROUND_COLOR = (0, 0, 0)
FONT_COLOR = (255, 255, 255)
FONT_NAME = 'Eurostile'
FONT_SIZE = 20

# Physics Constants
AU = 149597870.7 * 1000  # Astronomical Unit in meters
G = 6.67430e-11          # Gravitational constant
SCALE_FACTOR = 100 / AU  # Initial scale: 100 pixels per AU
TIMESTEP = 3600 * 24     # 1 day per second (real-time)

class Camera:
    def __init__(self):
        self.offset_x = 0
        self.offset_y = 0
        self.scale = SCALE_FACTOR
        self.dragging = False
        self.mouse_start = (0, 0)
        self.offset_start = (0, 0)

    def world_to_screen(self, x: float, y: float) -> Tuple[float, float]:
        """Convert world coordinates to screen coordinates"""
        screen_x = x * self.scale + WIDTH/2 - self.offset_x
        screen_y = y * self.scale + HEIGHT/2 - self.offset_y
        return screen_x, screen_y

    def screen_to_world(self, x: float, y: float) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        world_x = (x + self.offset_x - WIDTH/2) / self.scale
        world_y = (y + self.offset_y - HEIGHT/2) / self.scale
        return world_x, world_y

class Planet:
    def __init__(self, name: str, x: float, y: float, radius: int, color: Tuple[int, int, int], mass: float):
        self.name = name
        self.x = x
        self.y = y
        self.base_radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit: List[Tuple[float, float]] = []
        self.sun = False
        self.distance_to_sun = 0.0
        
        self.x_vel = 0.0
        self.y_vel = 0.0

    def set_velocity(self, x_vel: float, y_vel: float) -> 'Planet':
        """Set the initial velocity of the planet"""
        self.x_vel = x_vel
        self.y_vel = y_vel
        return self  # Return self for method chaining

    def draw(self, win: pygame.Surface, camera: Camera):
        """Draw the planet and its orbit trail"""
        screen_x, screen_y = camera.world_to_screen(self.x, self.y)
        
        # Draw orbit trail
        if len(self.orbit) > 2:
            trail_points = [camera.world_to_screen(x, y) for x, y in self.orbit]
            pygame.draw.lines(win, self.color, False, trail_points, 1)
        
        # Calculate dynamic radius based on zoom level
        radius = max(1, min(self.base_radius, int(self.base_radius * math.log2(camera.scale / SCALE_FACTOR + 1))))
        pygame.draw.circle(win, self.color, (int(screen_x), int(screen_y)), radius)

        # Draw distance to sun
        if not self.sun:
            distance_km = self.distance_to_sun / 1000
            text = FONT.render(f"{self.name}: {distance_km:,.1f} km", True, FONT_COLOR)
            win.blit(text, (screen_x - text.get_width()/2, screen_y - text.get_height()/2))

    def attraction(self, other: 'Planet') -> Tuple[float, float]:
        """Calculate gravitational attraction between two planets"""
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.hypot(dx, dy)
        
        if distance == 0:
            return 0, 0
            
        if other.sun:
            self.distance_to_sun = distance
            
        force = G * self.mass * other.mass / (distance ** 2)
        angle = math.atan2(dy, dx)
        fx = math.cos(angle) * force
        fy = math.sin(angle) * force
        return fx, fy

    def update_position(self, planets: List['Planet']):
        """Update planet position based on gravitational forces"""
        if self.sun:
            return  # Sun doesn't move

        total_fx = total_fy = 0.0
        for planet in planets:
            if planet is self:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Update velocity using Verlet integration for better stability
        self.x_vel += total_fx / self.mass * TIMESTEP
        self.y_vel += total_fy / self.mass * TIMESTEP

        # Update position
        self.x += self.x_vel * TIMESTEP
        self.y += self.y_vel * TIMESTEP
        
        # Maintain orbit trail (keep last 1000 points)
        self.orbit.append((self.x, self.y))
        if len(self.orbit) > 1000:
            self.orbit.pop(0)

def create_planets() -> List[Planet]:
    """Initialize solar system planets"""
    sun = Planet("Sun", 0, 0, 16, (255, 255, 0), 1.98892e30)
    sun.sun = True  # Mark the Sun as the central body

    planets = [
        sun,
        Planet("Mercury", -0.39 * AU, 0, 4, (169, 169, 169), 3.285e23).set_velocity(0, 47.87e3),
        Planet("Venus", -0.723 * AU, 0, 6, (205, 200, 149), 4.8675e24).set_velocity(0, 35.02e3),
        Planet("Earth", -1 * AU, 0, 6, (70, 130, 180), 5.97219e24).set_velocity(0, 29.783e3),
        Planet("Mars", -1.524 * AU, 0, 4, (188, 39, 50), 6.4171e23).set_velocity(0, 24.077e3),
        Planet("Jupiter", -5.203 * AU, 0, 12, (238, 232, 170), 1.898e27).set_velocity(0, 13.07e3),
        Planet("Saturn", -9.537 * AU, 0, 10, (210, 180, 140), 5.683e26).set_velocity(0, 9.69e3),
        Planet("Uranus", -19.191 * AU, 0, 8, (135, 206, 235), 8.681e25).set_velocity(0, 6.81e3),
        Planet("Neptune", -30.069 * AU, 0, 8, (30, 144, 255), 1.024e26).set_velocity(0, 5.43e3)
    ]
    return planets

def handle_input(camera: Camera, paused: bool) -> bool:
    """Handle user input and return updated pause state"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, paused
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse
                camera.dragging = True
                camera.mouse_start = event.pos
                camera.offset_start = (camera.offset_x, camera.offset_y)
            elif event.button in (4, 5):  # Mouse wheel
                handle_zoom(event, camera)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                camera.dragging = False

        elif event.type == pygame.MOUSEMOTION and camera.dragging:
            handle_pan(event, camera)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused

    return True, paused

def handle_zoom(event: pygame.event.Event, camera: Camera):
    """Handle zooming while keeping mouse position fixed"""
    zoom_factor = 1.1 if event.button == 4 else 1/1.1
    mouse_x, mouse_y = event.pos
    old_scale = camera.scale
    
    # Get world position before zoom
    world_x, world_y = camera.screen_to_world(mouse_x, mouse_y)
    
    # Apply zoom
    camera.scale *= zoom_factor
    
    # Adjust offset to keep mouse position fixed
    new_screen_x, new_screen_y = camera.world_to_screen(world_x, world_y)
    camera.offset_x += (mouse_x - new_screen_x)
    camera.offset_y += (mouse_y - new_screen_y)

def handle_pan(event: pygame.event.Event, camera: Camera):
    """Handle panning of the view"""
    current_x, current_y = event.pos
    dx = current_x - camera.mouse_start[0]
    dy = current_y - camera.mouse_start[1]
    camera.offset_x = camera.offset_start[0] - dx
    camera.offset_y = camera.offset_start[1] - dy

def draw_ui(win: pygame.Surface, camera: Camera, paused: bool):
    """Draw user interface elements"""
    # Display controls
    controls = [
        "Controls:",
        "Left Click + Drag - Pan",
        "Mouse Wheel - Zoom",
        "Space - Pause/Resume",
        "Esc - Quit"
    ]
    
    y_offset = 10
    for line in controls:
        text = FONT.render(line, True, FONT_COLOR)
        win.blit(text, (10, y_offset))
        y_offset += 20

    # Display simulation info
    info = [
        f"Scale: 1 AU = {1/camera.scale * AU/1000:,.0f} km/pixel",
        f"Status: {'Paused' if paused else 'Running'}"
    ]
    
    y_offset = HEIGHT - 60
    for line in info:
        text = FONT.render(line, True, FONT_COLOR)
        win.blit(text, (10, y_offset))
        y_offset += 20

def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Planetary Orbit Simulation")
    
    global FONT
    FONT = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
    
    camera = Camera()
    planets = create_planets()
    paused = False
    running = True
    
    while running:
        win.fill(BACKGROUND_COLOR)
        
        running, paused = handle_input(camera, paused)
        
        if not paused:
            for planet in planets:
                planet.update_position(planets)
        
        for planet in planets:
            planet.draw(win, camera)
        
        draw_ui(win, camera, paused)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()