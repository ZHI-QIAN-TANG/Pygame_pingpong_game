import pygame
import sys

#進行初始化
pygame.init()

#設定視窗長與寬
WIDTH, HEIGHT = 800, 600

#製作出視窗
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

#視窗取名
pygame.display.set_caption("Pong Game")

#設置基礎顏色與背景放置
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
background = pygame.image.load("background.jpg")

#載入音效
wall_hit_sound = pygame.mixer.Sound("PongHit.mp3") #球碰到牆壁的音效
paddle_hit_sound = pygame.mixer.Sound("PongHit.mp3") #球碰到板子的音效
score_sound = pygame.mixer.Sound("cheers.mp3") #球進入得分區的音效

#設置音效音量
wall_hit_sound.set_volume(0.5)  # 設置音量為 50%
paddle_hit_sound.set_volume(0.5)  # 設置音量為 50%
score_sound.set_volume(0.5)  # 設置音量為 50%

# 載入背景音樂
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.set_volume(0.1)  # 設定背景音樂音量為10%
pygame.mixer.music.play(-1)  # -1 表示無限循環播放


# 設定一條線
middle_line = pygame.Rect(WIDTH // 2 - 2, 0, 4, HEIGHT)

#設置球與球拍
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)
paddle1 = pygame.Rect(10, HEIGHT // 2 - 60, 10, 120)
paddle2 = pygame.Rect(WIDTH - 20, HEIGHT // 2 - 60, 10, 120)

#設定球的速度:
ball_speed = [5, 5]

#設定球拍移動速度
paddle_speed = 10

# 設定分數
score1 = 0
score2 = 0

# 字型設計
font = pygame.font.SysFont('arial', 36)

# 設定倒計時
countdown = 6000  # 倒計時6000幀
countdown_font = pygame.font.SysFont('arial', 100)

# 遊戲迴圈
clock = pygame.time.Clock()

#遊戲主迴圈
while countdown > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.blit(background, (0, 0))  # 繪製背景

    # 移動球
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    #可以使用鍵盤
    keys = pygame.key.get_pressed()

    # 控制玩家1的板
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= paddle_speed
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += paddle_speed
    # 控制玩家2的板
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= paddle_speed
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += paddle_speed

    # 碰撞檢測
    if ball.top < 0 or ball.bottom > HEIGHT:
        ball_speed[1] = -ball_speed[1]
        wall_hit_sound.play()  # 播放碰撞牆壁音效

    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed[0] = -ball_speed[0]
        paddle_hit_sound.play()  # 播放碰撞板子音效

    # 球越過左邊界
    if ball.left <= 0:
        score2 += 1
        ball.x = WIDTH // 2 - 15
        ball_speed[0] = -ball_speed[0]
        score_sound.play()  # 播放得分音效

    # 球越過右邊界
    if ball.right >= WIDTH:
        score1 += 1
        ball.x = WIDTH // 2 - 15
        ball_speed[0] = -ball_speed[0]
        score_sound.play()  # 播放得分音效

    #繪製中間線
    pygame.draw.rect(WIN, WHITE, middle_line)

    #繪製球拍與球
    pygame.draw.rect(WIN, WHITE, paddle1)
    pygame.draw.rect(WIN, WHITE, paddle2)
    pygame.draw.ellipse(WIN, WHITE, ball)
    
    #分數
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    WIN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # 倒計時
    countdown_text = font.render(str(countdown // 100), True, WHITE)
    WIN.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
    countdown -= 1

    pygame.display.flip() #使遊戲可以畫面更新
    
    clock.tick(120)

if score1 > score2:
    winner_text = font.render("Player 1 Wins!", True, WHITE)
elif score2 > score1:
    winner_text = font.render("Player 2 Wins!", True, WHITE)
else:
    winner_text = font.render("It's a Tie!", True, WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    WIN.blit(background, (0, 0))  # 繪製背景
    WIN.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2 - winner_text.get_height() // 2))
    
    pygame.display.flip()