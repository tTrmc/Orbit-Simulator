import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1500, 1500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Orbit Simulation")
FONT = pygame.font.SysFont('Consolas', 16)

class Planet:
    AU = 149597870.7 * 1000
    G = 6.67430 * 10**-11 
    SCALE = 100 / AU 
    TIMESTEP = 60*60*24
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        
        self.x_vel = 0
        self.y_vel = 0
        
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        
        pygame.draw.circle(win, self.color, (x, y), self.radius)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, (255, 255, 255))
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))
        
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if other.sun:
            self.distance_to_sun = distance
            
        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
            
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        

def main():
    run = True
    clock = pygame.time.Clock()
    
    sun = Planet(0, 0, 8, (255, 223, 0), 1.98892 * 10**30)
    sun.sun = True
    
    earth = Planet(-1 * Planet.AU, 0, 2.5, (70, 130, 180), 5.97219 * 10**24)
    earth.y_vel = 29.783 * 1000
    
    mars = Planet(-1.524 * Planet.AU, 0, 1.5, (188, 39, 50), 6.4171 * 10**23)
    mars.y_vel = 24.077 * 1000
    
    mercury = Planet(-0.39 * Planet.AU, 0, 1, (169, 169, 169), 3.285 * 10**23)
    mercury.y_vel = 47.87 * 1000
    
    venus = Planet(-0.723 * Planet.AU, 0, 2, (205, 200, 149), 4.8675 * 10**24)
    venus.y_vel = 35.02 * 1000
    
    jupiter = Planet(-5.203 * Planet.AU, 0, 5, (238, 232, 170), 1.898 * 10**27)
    jupiter.y_vel = 13.07 * 1000
    
    saturn = Planet(-9.537 * Planet.AU, 0, 4.5, (210, 180, 140), 5.683 * 10**26)
    saturn.y_vel = 9.69 * 1000
    
    uranus = Planet(-19.191 * Planet.AU, 0, 3.5, (135, 206, 235), 8.681 * 10**25)
    uranus.y_vel = 6.81 * 1000
    
    neptune = Planet(-30.069 * Planet.AU, 0, 3.5, (30, 144, 255), 1.024 * 10**26)
    neptune.y_vel = 5.43 * 1000
    
    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]
    
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        
        pygame.display.update()

    pygame.quit()
    
main()