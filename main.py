
# Importera nödvändiga bibliotek och initiera Pygame
import pygame
from pygame.locals import *

pygame.init()

# Skapa en klocka för att styra fps
clock = pygame.time.Clock()
fps = 60

# Skärmens dimensioner
screen_width = 800
screen_height = 600

# Skapa skärmen och ange titel
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy Bird')

# Definiera spelvariabler
ground_scroll = 0
scroll_speed = 4
flying = False
game_over = False

# Ladda in bilder
bg = pygame.image.load('fågel1.png')
ground_img = pygame.image.load('16364.png')

# Definiera klassen för fågeln
class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0
		self.counter = 0
		# Ladda in fågelns bilder och lägg till dem i listan
		for num in range(1, 4):
			img = pygame.image.load('fågel1.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.vel = 0
		self.clicked = False

	# Uppdatera fågeln
	def update(self):
		if flying == True:  # Om fågeln flyger
			# Gravitationseffekt
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 768:
				self.rect.y += int(self.vel)

		if game_over == False:
			# Hantera hopp
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				self.vel = -10
			if pygame.mouse.get_pressed()[0] == 0:
				self.clicked = False

			# Hantera animationen
			self.counter += 1
			flap_cooldown = 5
			if self.counter > flap_cooldown:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			# Rotera fågeln baserat på dess hastighet
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			# Om spelet är över, rotera fågeln vertikalt
			self.image = pygame.transform.rotate(self.images[self.index], -90)

# Skapa en grupp för fågeln
bird_group = pygame.sprite.Group()
flappy = Bird(100, int(screen_height / 2))
bird_group.add(flappy)

# Huvudspelloopen
run = True
while run:
	clock.tick(fps)

	# Rita bakgrundsbilden
	screen.blit(bg, (0, 0))

	# Rita och uppdatera fågeln
	bird_group.draw(screen)
	bird_group.update()

	# Rita marken och låt den scrolla
	screen.blit(ground_img, (ground_scroll, 768))
	ground_scroll -= scroll_speed
	if abs(ground_scroll) > 35:
		ground_scroll = 0

	# Kontrollera om fågeln har kolliderat med marken
	if flappy.rect.bottom > 768:
		game_over = True
		flying = False

	# Hantera händelser
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
			flying = True

	# Uppdatera skärmen
	pygame.display.update()

# Avsluta Pygame när loopen är klar
pygame.quit()