import pygame
import sys

# Function to load image and set transparent color
def load_image(image_path):
    image = pygame.image.load(image_path)
    return image

# Initialize Pygame
pygame.init()

# Set up window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Transparent Image Window")

# Load image
image_path = './assets/capybara.png'  # Change this to your image path
image = load_image(image_path)
image_rect = image.get_rect()

# Set initial position of image
image_rect.center = window.get_rect().center

# Main loop
running = True
dragging = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if image_rect.collidepoint(event.pos):
                    dragging = True
                    offset_x = event.pos[0] - image_rect.x
                    offset_y = event.pos[1] - image_rect.y
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                image_rect.x = event.pos[0] - offset_x
                image_rect.y = event.pos[1] - offset_y

    # Fill background
    window.fill((255, 255, 255))  # Fill with white background color

    # Blit image onto window with alpha blending
    window.blit(image, image_rect)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
