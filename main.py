import pygame, random, sys

pygame.init()

# layer
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the cat")

# font and warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont("pixel", 24)

# bck
bg_home = pygame.transform.scale(pygame.image.load("bg_home.png"), (WIDTH, HEIGHT))
bg_game1 = pygame.transform.scale(pygame.image.load("bg_game1.png"), (WIDTH, HEIGHT))
bg_game2 = pygame.transform.scale(pygame.image.load("bg_game2.png"), (WIDTH, HEIGHT))

#gmbr
player_img = pygame.image.load("Player.png")
player_img = pygame.transform.scale(player_img, (80, 80))
player_img_flipped = pygame.transform.flip(player_img, True, False)

cat_imgs = [
    pygame.transform.scale(pygame.image.load("Cat1.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load("Cat2.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load("Cat3.png"), (40, 40)),
    pygame.transform.scale(pygame.image.load("Cat4.png"), (40, 40))
]
enemy_img = pygame.transform.scale(pygame.image.load("Enemy.png"), (45, 45))
bullet_img = pygame.transform.scale(pygame.image.load("gun.png"), (10, 20))

win_img = pygame.transform.scale(pygame.image.load("win.jpg"), (WIDTH, HEIGHT))
lose_img = pygame.transform.scale(pygame.image.load("lose.jpg"), (WIDTH, HEIGHT))

# buttonnnn
btn_game1 = pygame.transform.scale(pygame.image.load("btn_game1.png"), (100, 100))
btn_game2 = pygame.transform.scale(pygame.image.load("btn_game2.png"), (100,100))
home_button_img = pygame.transform.scale(pygame.image.load("home_button.png"), (100,100))

# sound effect
shoot_sound = pygame.mixer.Sound("shoot.mp3"); shoot_sound.set_volume(0.5)
cat_sound = pygame.mixer.Sound("catch_cat.mp3");cat_sound.set_volume(0.5) 
hit_sound = pygame.mixer.Sound("hit.mp3"); hit_sound.set_volume(0.7)
shoot_sound = pygame.mixer.Sound("shoot.mp3"); hit_sound.set_volume(0.5)
win_sound = pygame.mixer.Sound("win.mp3"); win_sound.set_volume(1.0)
lose_sound = pygame.mixer.Sound("lose.mp3"); lose_sound.set_volume(1.0)

def play_backsound():
    pygame.mixer.music.load("backsound.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

# falling cat
def play_game1():
    global state
    score = 0
    lives = 5
    player_rect = player_img.get_rect(center=(WIDTH//2, HEIGHT-60))
    player_speed = 7
    facing_left = False

    objects, enemies, bullets = [], [], []
    fall_speed = 5
    spawn_event = pygame.USEREVENT + 1
    pygame.time.set_timer(spawn_event, 1000)

    clock = pygame.time.Clock()
    running = True
    play_backsound()

    while running and state == "GAME1":
        screen.blit(bg_game1, (0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == spawn_event:
                if random.random() < 0.2: 
                    rect = enemy_img.get_rect(center=(random.randint(20, WIDTH-20), -20))
                    enemies.append(rect)
                else: 
                    obj_img = random.choice(cat_imgs)
                    obj_rect = obj_img.get_rect(center=(random.randint(20, WIDTH-20), -20))
                    objects.append((obj_img, obj_rect))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = bullet_img.get_rect(center=(player_rect.centerx, player_rect.top))
                    bullets.append(bullet_rect)
                    shoot_sound.play()

        # playeh
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
            facing_left = False
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed
            facing_left = True

        # kucing
        new_objects = []
        for img, rect in objects:
            rect.y += fall_speed
            if rect.colliderect(player_rect):
                score += 1
                cat_sound.play()
            elif rect.top >= HEIGHT:
                score -= 1
            else:
                new_objects.append((img, rect))
        objects = new_objects

        # enemy
        new_enemies = []
        for rect in enemies:
            rect.y += fall_speed
            if rect.colliderect(player_rect):
                lives -= 1
                hit_sound.play()
            elif rect.top < HEIGHT:
                new_enemies.append(rect)
        enemies = new_enemies

        # gun
        new_bullets = []
        for b in bullets:
            b.y -= 10
            hit_enemy = None
            for e in enemies:
                if b.colliderect(e):
                    hit_enemy = e
                    break
            if hit_enemy:
                enemies.remove(hit_enemy)
                score += 2
                shoot_sound.play()
            elif b.bottom > 0:
                new_bullets.append(b)
        bullets = new_bullets

        # mirroring ceuk aku mah
        if facing_left:
            screen.blit(player_img_flipped, player_rect)
        else:
            screen.blit(player_img, player_rect)

        # yayh gituh
        for img, rect in objects:
            screen.blit(img, rect)
        for e in enemies:
            screen.blit(enemy_img, e)
        for b in bullets:
            screen.blit(bullet_img, b)

        # Uhmmm begituh lah
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH-120, 10))

        # makin lama makin cepet
        fall_speed = 7 + score // 5

        # win/lose
        if score >= 50:
            pygame.mixer.music.stop()
            win_sound.play()
            state = "WIN1"
            break
        if lives <= 0 or score <= -10:  # kalah kalau nyawa habis ATAU score <= -10
            pygame.mixer.music.stop()
            lose_sound.play()
            state = "LOSE1"
            break


        pygame.display.flip()
        clock.tick(60)

# poto

cat_imgs2 = [
    pygame.transform.scale(pygame.image.load("Cat1.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("Cat2.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("Cat3.png"), (100, 100)),
    pygame.transform.scale(pygame.image.load("Cat4.png"), (100, 100))
]


enemy_img_big = pygame.transform.scale(enemy_img, (90, 90))

# game 2 nggak sih??
def play_game2():
    global state
    score = 0
    lives = 5
    time_limit = 25
    start_time = pygame.time.get_ticks()

    # gridd
    positions = [
        (120, 170), (250, 170), (380, 170),
        (120, 310), (250, 310), (380, 310),
        (120, 450), (250, 450), (380, 450)
    ]

    current_objs = [] 
    obj_timer = 0
    obj_duration = 1000  
    obj_lifetime = 1000  

    clock = pygame.time.Clock()
    running = True
    play_backsound()

    while running and state == "GAME2":
        screen.blit(bg_game2, (0,0))

        # waktu tersisa
        elapsed = (pygame.time.get_ticks() - start_time) // 1000
        remaining = max(0, time_limit - elapsed)

        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for obj in current_objs[:]:
                    img, rect, otype, spawn_time = obj
                    if rect.collidepoint(event.pos):
                        if otype == "cat":
                            score += 1
                            cat_sound.play()
                        elif otype == "enemy":
                            lives -= 1
                            hit_sound.play()
                        current_objs.remove(obj)
                        break

        # hapus objek
        current_objs = [obj for obj in current_objs if now - obj[3] < obj_lifetime]

        # spawn object baru
        if now - obj_timer > obj_duration:
            spawn_count = random.randint(2, 3)
            available_positions = positions.copy()

            # hapus posisi
            for obj in current_objs:
                _, rect, _, _ = obj
                if rect.center in available_positions:
                    available_positions.remove(rect.center)

            for _ in range(spawn_count):
                if not available_positions:
                    break
                pos = random.choice(available_positions)
                available_positions.remove(pos)

                if random.random() < 0.7:
                    img = random.choice(cat_imgs2)
                    otype = "cat"
                else:
                    img = enemy_img_big
                    otype = "enemy"

                rect = img.get_rect(center=pos)
                current_objs.append((img, rect, otype, now))
            obj_timer = now

        #objek aktif
        for img, rect, _, _ in current_objs:
            screen.blit(img, rect)

        # score, lives, timer
        score_text = font.render(f"Score: {score}", True, BLACK)
        lives_text = font.render(f"Lives: {lives}", True, BLACK)
        timer_text = font.render(f"Time: {remaining}", True, BLACK)
        screen.blit(score_text, (50, 50))
        screen.blit(lives_text, (WIDTH-150, 50))
        screen.blit(timer_text, (WIDTH//2 - 40, 10))

        # kondisi menang/kalah
        if remaining <= 0: 
            pygame.mixer.music.stop()
            if score >= 20: 
                win_sound.play()
                state = "WIN2"
            else:
                lose_sound.play()
                state = "LOSE2"
            break
        if lives <= 0:
            pygame.mixer.music.stop()
            lose_sound.play()
            state = "LOSE2"
            break

        pygame.display.flip()
        clock.tick(60)

# HHHOOOOMEEEEE
state = "HOME"
clock = pygame.time.Clock()

while True:
    if state == "HOME":
        screen.blit(bg_home, (0,0))
        screen.blit(btn_game1, (WIDTH//2 - 90, HEIGHT//2 - 80))
        screen.blit(btn_game2, (WIDTH//2 - 90, HEIGHT//2 + 20))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if (WIDTH//2 - 90 <= x <= WIDTH//2 + 90) and (HEIGHT//2 - 80 <= y <= HEIGHT//2 - 20):
                    state = "GAME1"
                if (WIDTH//2 - 90 <= x <= WIDTH//2 + 90) and (HEIGHT//2 + 20 <= y <= HEIGHT//2 + 80):
                    state = "GAME2"

    elif state == "GAME1":
        play_game1()
    elif state == "GAME2":
        play_game2()

    elif state in ["WIN1", "LOSE1", "WIN2", "LOSE2"]:
        if "WIN" in state: screen.blit(win_img, (0,0))
        else: screen.blit(lose_img, (0,0))
        screen.blit(home_button_img, (WIDTH//2 - 60, HEIGHT - 100))
        pygame.display.flip()

        waiting = True
        while waiting and state in ["WIN1", "LOSE1", "WIN2", "LOSE2"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if (WIDTH//2 - 60 <= x <= WIDTH//2 + 60) and (HEIGHT - 100 <= y <= HEIGHT - 50):
                        state = "HOME"; waiting = False
