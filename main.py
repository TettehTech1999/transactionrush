import pygame
import asyncio
import random
import time

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Transaction Rush — Powered by Altius")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 150, 255)
GREEN = (0, 255, 100)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Fonts
font = pygame.font.SysFont("Arial", 32)
small_font = pygame.font.SysFont("Arial", 24)

# Game variables
score = 0
running = True
mode = "Normal"  # Start in normal mode
start_time = None
duration = 10  # seconds

# Function to draw text
def draw_text(text, x, y, color=WHITE, center=False):
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(txt, rect)

# Async function to simulate Altius parallel execution
async def process_transactions_async(count):
    global score
    await asyncio.sleep(0.05)  # simulate delay
    score += count

# Normal sequential processing
def process_transactions_sync(count):
    global score
    time.sleep(0.05)  # simulate delay
    score += count

# Draw button
def draw_button(text, x, y, w, h, color):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, color, rect, border_radius=10)
    label = small_font.render(text, True, BLACK)
    label_rect = label.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(label, label_rect)
    return rect

# Game loop
async def main():
    global running, score, mode, start_time

    clock = pygame.time.Clock()
    start_time = time.time()
    taps = 0

    while running:
        screen.fill(BLACK)

        elapsed = time.time() - start_time
        remaining = max(0, duration - int(elapsed))

        draw_text(f"Mode: {mode}", 20, 20, YELLOW)
        draw_text(f"Score: {score}", 20, 70, GREEN)
        draw_text(f"Time Left: {remaining}s", 20, 120, BLUE)

        # Draw buttons
        normal_btn = draw_button("Normal Mode", 50, 500, 150, 50, BLUE)
        altius_btn = draw_button("Altius Mode", 300, 500, 150, 50, GREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                # Switch modes
                if normal_btn.collidepoint(pos):
                    mode = "Normal"
                    score = 0
                    start_time = time.time()

                elif altius_btn.collidepoint(pos):
                    mode = "Altius"
                    score = 0
                    start_time = time.time()

                else:
                    # Every click = a transaction
                    if mode == "Normal":
                        process_transactions_sync(1)
                    else:
                        await process_transactions_async(1)

        # If time runs out
        if remaining <= 0:
            running = False

        pygame.display.flip()
        clock.tick(60)

    # End screen
    screen.fill(BLACK)
    draw_text("Game Over!", WIDTH / 2, HEIGHT / 2 - 40, RED, center=True)
    draw_text(f"Final Score: {score}", WIDTH / 2, HEIGHT / 2, GREEN, center=True)
    draw_text("Close window to exit", WIDTH / 2, HEIGHT / 2 + 50, YELLOW, center=True)
    pygame.display.flip()

    # Wait for player to close
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False

    pygame.quit()

# Run the async main loop
asyncio.run(main()) 