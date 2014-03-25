#!/usr/bin/env python
# encoding: utf-8

#---------------------------------------------------------------------#
import os, pygame, math, sys
from pygame import *
import random, time
import menu
#---------------------------------------------------------------------#

class Card:
	def __init__(self, id):
		self.backImg = pygame.image.load("data/b.png")
		self.frontImg = pygame.image.load("data/"+id+".png")
		self.img = self.backImg
		self.rect = self.backImg.get_rect()
		self.rect.x = 15
		self.rect.y = 15
		self.selected = 0
		if (int(id[1:] == 13)):
			self.parent = id[:1] + "1"
		else:
			rank_int = int(id[1:])+1
			rank_str = str(rank_int)
			self.parent = id[:1] + rank_str

		if (int(id[1:] == 1)):
			self.child = id[:1] + "13"
		else:
			rank_int = int(id[1:])-1
			rank_str = str(rank_int)
			self.child = id[:1] + rank_str

	def flip(self):
		if(self.side == 1):
			self.side = 0
			self.img = self.bimg
		else:
			self.side = 1
			self.img = self.fimg

	def draw(self,surface):
		surface.blit(self.img,self.rect.topleft)

	#def move(self,dx,dy):
    #    self.rect.x += dx
    #    self.rect.y += dy
    #    if self.child:
    #        self.child.move(dx,dy)

#---------------------------------------------------------------------#

class Deck:
	def __init__(self):
		self.deck = []
		self.create_deck()
		self.apply_images()
		self.shuffle_deck()


	def __str__(self):
		return self.deck.deck

	#N: self.Deck = self.createDeck()
	#F: Ekkert
	#E: Buid er ad bua til spilastokk med 52 spilum
	def create_deck(self):
		suit = ['H', 'L', 'S', 'T']
		rank = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

		for s in suit:
			for r in rank:
				self.deck.append(s+`r`)
		return self.deck

	def apply_images(self):
		for idx, card in enumerate(self.deck):
			self.deck[idx] = Card(self.deck[idx])
		return self.deck


	def shuffle_deck(self):
		random.shuffle(self.deck)
		return self.deck

	#N: self.deck.isEmpty()
	#F: self.deck er spilabúnki
	#E: True ef búnkinn er ekki tómur, annars False
	def isEmpty(self):
		if(len(self.deck) == 0):
			return True
		else:
			return False

	#N: self.deck.get_card()
	#F: self.deck er búnki með spilum
	#E: Búið er að draga aftasta spilið úr búnkanum
	def get_card(self):
		if not self.isEmpty():
			return self.deck.pop()

	def draw(self, surface):
		for card in self.deck:
			card.draw(surface)

#---------------------------------------------------------------------#

class Deck_B:
	def __init__(self):
		self.deck_b = []

	def __str__(self):
		return self.deck_b

	def add_card(self, card):
		self.deck_b.append(card)

	def draw(self, surface):
		for card in self.deck_b:
			surface.blit(card.img, card.rect.topleft)

#---------------------------------------------------------------------#

class Board:
	def __init__(self):
		self.board = [[0,0,0,0,0] for collumn in range (7)]

	def __str__(self):
		result = "\n".join("\t".join(map(str,l)) for l in self.board)
		return result

	def draw(self, surface):
		for collumn in self.board:
			for card in collumn:
				card.draw(surface)

	#N: self.board[x].isEmpty()
	#F: self.board er listi af listum, þar sem ytri listinn er að lengd 7
	#		og innri listarnir eru af lengd 5.
	#E: True ef innri listi x er tómnur, annars False
	def isEmpty(self, id):
		if(len(self.board[id]) == 0):
			return True
		else:
			return False

#---------------------------------------------------------------------#


class GUI:
	def __init__(self):
		width = 800
		height = 500

		pygame.init()
		self.screen = pygame.display.set_mode((width, height))
		pygame.display.set_caption('Dolan n Frens')
		#font = pygame.font.Font('data/menu_font.ttf', 32)
		pygame.mouse.set_visible(1)
		background = pygame.Surface(self.screen.get_size())
		background = background.convert()
		background.fill((0, 0, 0))
		clock = pygame.time.Clock()



		# draw background
		self.screen.blit(background, (0, 0))
		pygame.display.flip()

		# code for our menu 
		ourMenu = ["Start", "Highscores", "About", "Quit"]

		self.myMenu = menu.Menu(ourMenu)
		self.myMenu.drawMenu()

		# main loop for event handling and drawing
		while 1:
		    clock.tick(60)

		# Handle Input Events
		    for event in pygame.event.get():
		        self.myMenu.handleEvent(event)
		        # quit the game if escape is pressed
		        if event.type == QUIT:
		            return
		        elif event.type == KEYDOWN and event.key == K_ESCAPE:
		            self.myMenu.activate()
		        elif event.type == menu.Menu.MENUCLICKEDEVENT:
		        	#Start
		            if event.item == 0:
						isGameActive = True
						self.myMenu.deactivate()
						self.deck_a = Deck()
						self.deck_b = Deck_B()
						self.board = Board()
						#Setja upp kapal
						self.set_up_board(self.screen)
						self.set_up_deck_a(self.screen)
						self.set_up_deck_b(self.screen)
		            #Highscores
		            if event.item == 1:
						self.myMenu = menu.Menu([u"Hjörtur \t 2344", u"Guðni \t 2058", u"Hrolfur", u"Egill"])
						self.myMenu.drawMenu()
		            #About
		            if event.item == 2:
		            	print "About"
		        	#Quit
		            if event.item == 3:
		                return
       
		    self.screen.blit(background, (0, 0))    
		    if self.myMenu.isActive():
		        self.myMenu.drawMenu()	
		    else:
				self.deck_a.draw(self.screen)
				self.deck_b.draw(self.screen)
				self.board.draw(self.screen)
				#if event.type == MOUSEBUTTONDOWN:
				#	if event.button in[1, 2, 3]:
				#		mp = mouse.get_pos()
				#		if self.selectionRect.collidepoint(mp):
				#			print "asdfasdf"
#
#							print "collide"
						

		    pygame.display.flip()

	#N: self.set_up_game()
	#F: Ekkert
	#E: Ef Búnki A var ekki tómur, þá er búið að stilla upp leiknum.l
	#		Þ.e. búa til 7 dálka með 5 spilum hvor, búnka A sem inniheldur
	#		afgangs spilin og búnka B sem inniheldur eitt dregið spil úr A.
	#		Annars eitthvað ???
	def set_up_board(self, surface):
		x = 50
		if(not self.deck_a.isEmpty()):
			for col_idx, collumn in enumerate(self.board.board):
				y = 15
				for i in range(0,5):
					card = self.deck_a.get_card()
					card.rect.x = x
					card.rect.y = y
					card.img = card.frontImg
					collumn[i] = card
					y+=30
				x += 100
			self.deck_b.add_card(self.deck_a.get_card())

	def set_up_deck_a(self, surface):
		x = 50
		y = 300
		for card in self.deck_a.deck:
			card.rect.x = x
			card.rect.y = y
			card.img = card.backImg
			
	def set_up_deck_b(self, surface):
		x = 150
		y = 300
		for card in self.deck_b.deck_b:
			card.rect.x = x
			card.rect.y = y
			card.img = card.frontImg
			x += 30

#---------------------------------------------------------------------#

class Game:
	def __init__(self):
		self.deck_a = Deck()
		self.deck_b = Deck_B()
		self.board = Board()

	#N: self.begin_time()
	#F: Ekkert
	#E: Búið er að setja á stað tímateljara
	def begin_time(self):
		start = time.time()
		while (True):
			end = time.time()
			time.sleep(0.01)
			timi = "%.3f" % (end-start)


	#N: self.reset_game()
	#F: Ekkert
	#E: Búið er að frumstilla leikinn.
	def new_game(self):
		self.__init__()

#---------------------------------------------------------------------#

def main():
	gui = GUI()

if __name__ == '__main__':
    main()