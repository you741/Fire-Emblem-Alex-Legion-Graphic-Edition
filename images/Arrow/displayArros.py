from pygame import *
screen = display.set_mode((800,600))
arrowHead = image.load("arrowHead.png")
bentArrow = image.load("arrowBent.png")
straightArrow = image.load("arrowStraight.png")
screen.blit(straightArrow,(0,0))
screen.blit(transform.flip(bentArrow,0,0),(30,0))
screen.blit(transform.rotate(straightArrow,90),(30,30))
screen.blit(transform.flip(bentArrow,1,1),(30,60))
screen.blit(arrowHead,(60,60))
running = True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    display.flip()
quit()
