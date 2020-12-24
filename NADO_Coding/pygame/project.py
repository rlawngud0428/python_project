import os
import pygame
#################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640 # 가로
screen_height = 480 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("pang") #게임 이름

# FPS
clock = pygame.time.Clock()
#################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background_project.png"))

# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage_project.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해

# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character_project.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# 캐릭터 이동 방향
character_to_x = 0

# 캐릭터 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon_project.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

#무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 발사 속도
weapon_speed = 10

# 공 만들기 (4개 크기에 대해 따로 처리)
enemy_images = [
    pygame.image.load(os.path.join(image_path, "enemy1.png")),
    pygame.image.load(os.path.join(image_path, "enemy2.png")),
    pygame.image.load(os.path.join(image_path, "enemy3.png")),
    pygame.image.load(os.path.join(image_path, "enemy4.png"))
]

# 공 크기에 따른 최초 스피드
enemy_speed_y = [-18, -15, -12, -9] # 인덱스 0,1,2,3 에 해당하는 값

# 공들
enemys = []

# 최초 발생하는 큰 공 생성
enemys.append({
    "pos_x" : 50, # 공의 x 좌표
    "pos_y" : 50, # 공의 y 좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # 공의 x축 이동방향, -3 이면 왼쪽, +3 이면 오른쪽
    "to_y" : -6, # 공의 y축 이동방향
    "init_spd_y" : enemy_speed_y[0] # y 최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
enemy_to_remove = -1

# 폰트 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # 시작 시간 정의


# 게임 종료 메시지 / Time Out (시간초과) , Mission Complete (성공) , Game Over (실패)
game_result = "Game Over"

# 이벤트 루프
running = True #게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수를 설정

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # 무기 위치를 위로

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for enemy_idx, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        enemy_size = enemy_images[enemy_img_idx].get_rect().size
        enemy_width = enemy_size[0]
        enemy_height = enemy_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if enemy_pos_x < 0 or enemy_pos_x > screen_width - enemy_width:
            enemy_val["to_x"] = enemy_val["to_x"] * -1
        
        # 세로 위치
        #스테이지에 튕겨서 올라가는 처리
        if enemy_pos_y >= screen_height - stage_height - enemy_height:
            enemy_val["to_y"] = enemy_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            enemy_val["to_y"] += 0.5

        enemy_val["pos_x"] += enemy_val["to_x"]
        enemy_val["pos_y"] += enemy_val["to_y"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for enemy_idx, enemy_val in enumerate(enemys):
        enemy_pos_x = enemy_val["pos_x"]
        enemy_pos_y = enemy_val["pos_y"]
        enemy_img_idx = enemy_val["img_idx"]

        # 공 rect 정보 업데이트
        enemy_rect = enemy_images[enemy_img_idx].get_rect()
        enemy_rect.left = enemy_pos_x
        enemy_rect.top = enemy_pos_y
        
        # 공과 캐릭터 충돌 체크
        if character_rect.colliderect(enemy_rect):
            game_result = "Game Over"
            running = False
            break
        
        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(enemy_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                enemy_to_remove = enemy_idx # 해당 적 없애기 위한 값 설정

                # 가장 작은 공이 아니면, 2개로 나누어지는 조건설정
                if  enemy_img_idx < 3:
                    # 현재 공 크기 정보
                    enemy_width = enemy_rect.size[0]
                    enemy_height = enemy_rect.size[1]

                    # 나눠진 공 정보
                    small_enemy_rect = enemy_images[enemy_img_idx + 1].get_rect()
                    small_enemy_width = small_enemy_rect.size[0]
                    small_enemy_height = small_enemy_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    enemys.append({
                        "pos_x" : enemy_pos_x + (enemy_width / 2) - (small_enemy_width / 2), # 공의 x 좌표
                        "pos_y" : enemy_pos_y + (enemy_height / 2) - (small_enemy_height / 2), # 공의 y 좌표
                        "img_idx" : enemy_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : -3, # 공의 x축 이동방향, -3 이면 왼쪽, +3 이면 오른쪽
                        "to_y" : -6, # 공의 y축 이동방향
                        "init_spd_y" : enemy_speed_y[enemy_img_idx + 1] # y 최초 속도
                    })

                    # 오른쪽으로 튕겨나가는 작은 공
                    enemys.append({
                        "pos_x" : enemy_pos_x + (enemy_width / 2) - (small_enemy_width / 2), # 공의 x 좌표
                        "pos_y" : enemy_pos_y + (enemy_height / 2) - (small_enemy_height / 2), # 공의 y 좌표
                        "img_idx" : enemy_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : +3, # 공의 x축 이동방향, -3 이면 왼쪽, +3 이면 오른쪽
                        "to_y" : -6, # 공의 y축 이동방향
                        "init_spd_y" : enemy_speed_y[enemy_img_idx + 1] # y 최초 속도
                    })
                break
        else:
            continue
        break

    # 충돌된 공 or 무기 없애기
    if enemy_to_remove > -1:
        del enemys[enemy_to_remove]
        enemy_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공을 없앤 경우
    if len(enemys) == 0:
        game_result = "Mission Complete!"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(enemys):
        enemy_pos_x = val["pos_x"]
        enemy_pos_y = val["pos_y"]
        enemy_img_idx = val["img_idx"]
        screen.blit(enemy_images[enemy_img_idx], (enemy_pos_x, enemy_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))

    # 경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10,10))

    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False

    pygame.display.update() # 게임화면을 다시 그리기! 중요   

msg = game_font.render(game_result, True, (255,255,255))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg,msg_rect)
pygame.display.update()

pygame.time.delay(2000)

# pygame 종료
pygame.QUIT()