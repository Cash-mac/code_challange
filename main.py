import pygame
import requests
from os.path import join

#set up screen
pygame.init()
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
display_title = pygame.display.set_caption('Word Guessing Game')
running = True

#import font
font_title = pygame.font.Font(join('DynaPuff-VariableFont_wdth,wght.ttf'), 60)
font_header = pygame.font.Font(join('DynaPuff-VariableFont_wdth,wght.ttf'), 40)
#create title screen text
text_surf = font_title.render('HANG MAN!', True, 'lightgray')
text_surf_2 = font_header.render('Coding Challenge: Word Guessing Game', True, 'lightgray')
text_surf_3 = font_title.render('PLAY', True, 'lightgray')
text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2, 200) )
text_rect_2 = text_surf_2.get_frect(center = (WINDOW_WIDTH/2, 300))
text_rect_3 = text_surf_3.get_frect(center = (WINDOW_WIDTH/2, 400))

def end(ending, word): #end screen
    #print(ending)

    

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect_3.collidepoint(mouse_pos):
                    #Restart Game
                    main()
                    return
        #different screen endings
        if ending == 'lost':
            text_surf = font_title.render('You Lost!', True, 'lightgray')
            text_surf_2 = font_header.render(word, True, 'lightgray')
            text_surf_3 = font_title.render('Try again?', True, 'lightgray')
            display_surface.fill("#713535")


        else:
            text_surf = font_title.render('You Won!', True, 'lightgray')
            text_surf_2 = font_header.render(word, True, 'lightgray')
            text_surf_3 = font_title.render('go again?', True, 'lightgray')
            display_surface.fill("#447137")

        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2, 200) )
        text_rect_2 = text_surf_2.get_frect(center = (WINDOW_WIDTH/2, 300))
        text_rect_3 = text_surf_3.get_frect(center = (WINDOW_WIDTH/2, 400))
        display_surface.blit(text_surf, text_rect)
        display_surface.blit(text_surf_2, text_rect_2)
        display_surface.blit(text_surf_3, text_rect_3)
        #update screen
        pygame.display.update()

def play(dif): #play game
    #get random word from random word API
    #random word length 6 letters
    try:
        response = requests.get(f"https://random-word-api.vercel.app/api?words=1&length={dif}")
        word = response.json()[0]
    #if the api breaks
    except Exception as e:
        print(f"Error fetching word: {e}")
        word = 'broken'
    #print(word) #if you want to cheat
    #create list and variables
    letters_guessed = []
    
    wrong_guesses = 0
    state = 'go'

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            #key input
            if event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                #only letters
                if len(key) == 1 and key.isalpha():
                    #no repeats
                    if key in letters_guessed:
                        state = 'already'
                    else:
                        if key in word:
                            state = 'right'
                        else:
                            state = 'wrong'
                            wrong_guesses += 1
                            
                        letters_guessed.append(key.lower()) # add letter to letters_guessed

        #show wrong guesses
        guesses_display = ''
        for i in letters_guessed:
            if not i in word:
                
                guesses_display += i
                guesses_display += '  '


        #process data to display guessed word
        word_display = ''
        for letter in word:
            if letter in letters_guessed:
                word_display += letter
            else:
                word_display += ' _ '

        #Is the game won or lost yet?
        if word_display == word:
            end('won', word)
            break
        elif wrong_guesses > 7:
            end('lost', word)
            break

        word_display = word_display.upper()


        #background
        if state == 'wrong':
            display_surface.fill("#713535")
            text_surf = font_title.render('WRONG :( Try again.', True, 'lightgray')
        elif state == 'right':
            display_surface.fill("#447137")
            text_surf = font_title.render('RIGHT! Keep it up!', True, 'lightgray')
        elif state == 'already':
            display_surface.fill('#525252')
            text_surf = font_title.render('Already Guessed. Try again!', True, 'lightgray')
        else:
            display_surface.fill('#525252')
            text_surf = font_title.render('Guess a LETTER!', True, 'lightgray')
        #render text
        
        text_surf_2 = font_header.render(word_display, True, 'lightgray')
        text_surf_3 = font_title.render(f'Letters used: {guesses_display}', True, 'lightgray')
        text_surf_4 = font_header.render(f'Errors left: {7 - wrong_guesses}', True, 'lightgray')

        
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2, 200) )
        text_rect_2 = text_surf_2.get_frect(center = (WINDOW_WIDTH/2, 300))
        text_rect_3 = text_surf_3.get_frect(center = (WINDOW_WIDTH/2, 400))
        text_rect_4 = text_surf_3.get_frect(center = (WINDOW_WIDTH/2, 500))
        #display
        
        display_surface.blit(text_surf, text_rect)
        display_surface.blit(text_surf_2, text_rect_2)
        display_surface.blit(text_surf_3, text_rect_3)
        display_surface.blit(text_surf_4, text_rect_4)
        


        pygame.display.update()

def difficulty():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        text_surf = font_title.render('Difficulty?', True, 'lightgray')
        text_surf_2 = font_header.render('Hard', True, '#713535')
        text_surf_3 = font_header.render('Easy', True, '#447137')
        text_rect = text_surf.get_frect(center = (WINDOW_WIDTH/2, 200) )
        text_rect_2 = text_surf_2.get_frect(center = (WINDOW_WIDTH/1.5, 300))
        text_rect_3 = text_surf_3.get_frect(center = (WINDOW_WIDTH/2.5, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect_3.collidepoint(mouse_pos):
                    return 4
                elif text_rect_2.collidepoint(mouse_pos):
                    return 9
                
        display_surface.fill('#525252')
        display_surface.blit(text_surf, text_rect)
        display_surface.blit(text_surf_2, text_rect_2)
        display_surface.blit(text_surf_3, text_rect_3)


        pygame.display.update()




def main(): #menu screen
    running = True
    while running:

        mouse_pos = pygame.mouse.get_pos()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if text_rect_3.collidepoint(mouse_pos):
                    dif = difficulty()
                    #Start Game
                    play(dif)
        

        #display
        display_surface.fill('#525252')
        display_surface.blit(text_surf, text_rect)
        display_surface.blit(text_surf_2, text_rect_2)
        display_surface.blit(text_surf_3, text_rect_3)


        pygame.display.update()
    pygame.quit()




main()