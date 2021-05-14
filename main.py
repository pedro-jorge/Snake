import sys, pygame
from random import randint as rand 

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 440, 640 # tamanho da tela
RIGHT = pygame.K_RIGHT
LEFT = pygame.K_LEFT
UP = pygame.K_UP
DOWN = pygame.K_DOWN

SIZE = 20
STEP = 20

LIMIT_X_RIGHT, LIMIT_X_LEFT = 420, 0
LIMIT_Y_UP, LIMIT_Y_DOWN = 0, 620

class Snake:
    def __init__(self, x=WIDTH/2, y=HEIGHT/2):
        self.x, self.y = x, y
        self.nodes = [[x,y]]

    def move(self, direction):
        if direction == RIGHT:
            self.x += STEP

        elif direction == LEFT:
            self.x -= STEP
        
        elif direction == UP:
            self.y -= STEP

        elif direction == DOWN:
            self.y += STEP

class Apple:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def new(self):
        self.x, self.y = (rand(SIZE, WIDTH-SIZE)//SIZE)*SIZE, (rand(SIZE, HEIGHT-SIZE)//SIZE)*SIZE

class Game:
    def __init__(self):
        self.WHITE = (pygame.Color(255,255,255)) # tupla branca
        self.GREEN = GREEN = (pygame.Color(0,255,0)) # tupla verde
        self.BACKGROUND = (0,0,0) # cor do fundo (preto) 

        self.FPS = 15
        self.SCREEN_SIZE = (WIDTH, HEIGHT)
        self.LIMIT_X_RIGHT, self.LIMIT_X_LEFT = 420, 0
        self.LIMIT_Y_UP, self.LIMIT_Y_DOWN = 0, 620


        self.SCREEN = pygame.display.set_mode(self.SCREEN_SIZE)
        self.CLOCK = pygame.time.Clock()
        self.FONT = pygame.font.SysFont('Comic Sans MS', 30)

        self.snake = Snake() 
        self.apple = Apple()
        self.key = RIGHT
        self.max_points_text = self.FONT.render('Ponto máximo: ', False, (255,255,255))
        self.current_points_text = self.FONT.render('Ponto atual: ', False, (255,255,255))
        self.max_points = 1
        self.current_points = 1

        pygame.display.set_caption('Pysnake')
        self.apple.new()

    
    def draw_snake(self, is_head=False):
        if is_head:
            pygame.draw.rect(self.SCREEN, self.WHITE, [self.snake.x, self.snake.y, SIZE, SIZE])
            self.snake.nodes[0] = [self.snake.x, self.snake.y]
            return

        i = len(self.snake.nodes) - 1
        while i > 0:
            self.snake.nodes[i][0], self.snake.nodes[i][1] = self.snake.nodes[i-1][0], self.snake.nodes[i-1][1]
            pygame.draw.rect(self.SCREEN, self.WHITE, [self.snake.nodes[i][0], self.snake.nodes[i][1], SIZE, SIZE])
            i-=1

    def draw_apple(self):
        pygame.draw.rect(self.SCREEN, self.GREEN, [self.apple.x, self.apple.y, SIZE, SIZE])
    
    def try_eat_apple(self):
        if self.snake.x == self.apple.x and self.snake.y == self.apple.y:
            self.snake.nodes.insert(0, [self.snake.x, self.snake.y])
            self.apple.new()

            self.current_points += 1
            if self.current_points > self.max_points:
                self.max_points = self.current_points

    
    def check_game_over(self):
        if self.snake.x == self.LIMIT_X_RIGHT or \
           self.snake.x == self.LIMIT_X_LEFT or \
           self.snake.y == self.LIMIT_Y_DOWN or \
           self.snake.y == self.LIMIT_X_LEFT:
            self.current_points = 1
            return True
        
        if len(self.snake.nodes) > 2:
            i = len(self.snake.nodes)
            while i > 2:
                i-=1
                if self.snake.x == self.snake.nodes[i][0] and self.snake.y == self.snake.nodes[i][1]:
                    self.current_points = 1
                    return True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.key = event.key    

            self.SCREEN.fill(self.BACKGROUND)
            self.draw_snake()
            self.draw_snake(is_head=True)
            self.draw_apple()

            self.SCREEN.blit(self.max_points_text, (0,0))
            max_points_txt = self.FONT.render(str(self.max_points), False, (255,255,255))
            self.SCREEN.blit(max_points_txt, (220, 0))

            self.SCREEN.blit(self.current_points_text, (0,40))
            current_points_txt = self.FONT.render(str(self.current_points), False, (255,255,255))
            self.SCREEN.blit(current_points_txt, (220, 40))



            if self.check_game_over():
                self.snake = Snake()

            self.snake.move(self.key)
            self.try_eat_apple()

            pygame.display.flip()
            self.CLOCK.tick(self.FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
