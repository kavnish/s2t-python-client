import pygame
import sys
import time
from demo import Listener


# initializing the constructor
pygame.init()

# screen resolution
res = (500,500)

# opens up a window
screen = pygame.display.set_mode(res)

# white color
color = (255,255,255)

# light shade of the button
color_light = (170,170,170)

# dark shade of the button
color_dark = (100,100,100)

# stores the width of the
# screen into a variable
width = screen.get_width()

# stores the height of the
# screen into a variable
height = screen.get_height()

# defining a font
smallfont = pygame.font.SysFont('Corbel',35)

# rendering a text written in
# this font

recording = False

start = None

transcript = ''


def quitButton():
	position = [200,400,100,50]
	if position[0] <= mouse[0] <= position[0] + position[2] and position[1] <= mouse[1] <= position[1] + position[3]:
		pygame.draw.rect(screen,color_light, position)
	else:
		pygame.draw.rect(screen,color_dark, position)
	text = smallfont.render('Quit' , True , color)
	screen.blit(text , (position[0]+20, position[1]+10))
	return

def recordButton():
	position = [200,200,100,50]
	if position[0] <= mouse[0] <= position[0] + position[2] and position[1] <= mouse[1] <= position[1] + position[3]:
		pygame.draw.rect(screen,color_light, position)
	else:
		pygame.draw.rect(screen,color_dark, position)

	global recording, start

	if not recording:
		text = smallfont.render('Rec.' , True , color)
		screen.blit(text , (position[0]+20, position[1]+10))
	else:
		play = smallfont.render(str(round(float(time.time() - start), 2))+' sec' , True , color)
		screen.blit(play , (position[0]+20, position[1]+10))
	return

def checkmouseclick():

	quit_position = [200,400,100,50]
	record_position = [200,200,100,50]

	global recording, start

	#checks if a mouse is clicked
	if ev.type == pygame.MOUSEBUTTONDOWN:
		start = time.time()
		if quit_position[0] <= mouse[0] <= quit_position[0] + quit_position[2] and quit_position[1] <= mouse[1] <= quit_position[1] + quit_position[3]:
			pygame.quit()
		if record_position[0] <= mouse[0] <= record_position[0] + record_position[2] and record_position[1] <= mouse[1] <= record_position[1] + record_position[3]:
			recording = True
			recordStart()
	if ev.type == pygame.MOUSEBUTTONUP:
		if record_position[0] <= mouse[0] <= record_position[0] + record_position[2] and record_position[1] <= mouse[1] <= record_position[1] + record_position[3]:
			recording = False
			start = time.time()
			recordsStop()

	return

def recordsStart():
	stub = getStub()
    session = onlineSession()
    session.startTranscription(stub)
	return

def recordStop():
	session.stopTranscription()
	return

def printTranscript(position = [20, 250]):
	global recording, transcript
	if recording:
		text = smallfont.render(transcript , True , color)
		screen.blit(text , (position[0]+20, position[1]+10))
	return 

while True:
	
	for ev in pygame.event.get():
		
		if ev.type == pygame.QUIT:
			pygame.quit()
			
		#checks if a mouse is clicked
		checkmouseclick()
		
	# fills the screen with a color
	screen.fill((255,255,255))
	
	mouse = pygame.mouse.get_pos()

	recordButton()
	quitButton()

	printTranscript()

	# updates the frames of the game
	pygame.display.update()




