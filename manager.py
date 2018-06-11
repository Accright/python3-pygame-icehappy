import pygame
import random
from pygame.locals import *


class SoundPlay:
    game_bgm = "sound/GameSceneBGM.ogg"
    world_bgm = 'sound/WorldSceneBGM.ogg'
    eliminate = ('sound/eliminate1.ogg', 'sound/eliminate2.ogg', 'sound/eliminate3.ogg', 'sound/eliminate4.ogg',\
                 'sound/eliminate5.ogg')  # 消除声音
    score_level = ('sound/good.ogg', 'sound/great.ogg', 'sound/amazing.ogg', 'sound/excellent.ogg',\
                   'sound/unbelievable.ogg')   # 得分声音
    click = "sound/click.bubble.ogg"  # 点击选中声音
    board_sound = 'sound/board.ogg'   # 落板子声音
    click_button = 'sound/click_common_button.ogg'  # 点击按钮声音
    money_sound = 'sound/money.ogg'   # 点击银币声音
    ice_break = 'sound/ice_break.ogg'   # 冰消除声音

    def __init__(self, filename, loops=0):
        self.sound = pygame.mixer.Sound(filename)
        self.sound.play(loops)


class Tree(pygame.sprite.Sprite):
    """树类"""
    tree = 'pic2/tree.png'     # 树
    fruit = 'pic2/fruit.png'   # 果子
    energy_num = 'pic2/energy_num.png'  # 精力
    money = 'pic2/money.png'   # 银币
    energy_buy = 'pic2/energy_buy.png'   # 购买精力
    x, y = 340, 510
    h = 90
    position = ([x, y], [x+50, y-25], [x+105, y-45], [x-5, y-h-5], [x+55, y-25-h+10], [x+105, y-45-h], \
                [x, y-h*2], [x+50+10, y-25-h*2-5], [x+105+25, y-45-h*2-14], [x+30, y-h*3-30])   # 果子坐标组
    energy_num_position = (15, 70)  # 精力坐标
    energy_buy_position = (250, 400)

    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position      # 左下角为坐标

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class ManagerTree:
    """管理树类"""
    __screen_size = (900, 600)
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    fruit_list = []
    fruit_image = pygame.image.load(Tree.fruit).convert_alpha()
    fruit_width = fruit_image.get_width()
    fruit_height = fruit_image.get_height()
    type = 0  # 0树界面，1加精力界面
    energy_full = False  # 精力已满标志 初始未满
    money_empty = False  # 银币不足

    def load_text(self, text, position, txt_size=25, txt_color=(255, 255, 255)):
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def draw_tree(self, energy_num, money_num):
        """画tree"""
        Tree(Tree.tree, (0, 600)).draw(self.screen)      # 画树
        Tree(Tree.energy_num, Tree.energy_num_position).draw(self.screen)  # 画精力
        # print("energy", energy_num)
        if energy_num > 30:
            self.load_text(str(30) + '/30', (22, 55), 21)
        else:
            self.load_text(str(energy_num)+'/30', (22, 55), 21)
        # print("money", money_num)
        Tree(Tree.money, (15, 135)).draw(self.screen)  # 画银币
        self.load_text(str(money_num), (32, 124), 21)
        for i in range(0, 10):                            # 画果子
            Tree(Tree.fruit, Tree.position[i]).draw(self.screen)
            self.load_text(str(i+1), (Tree.position[i][0]+15, Tree.position[i][1]-47))
        if self.type == 1:
            Tree(Tree.energy_buy, Tree.energy_buy_position).draw(self.screen)
            if self.energy_full:
                self.load_text("energy is full!", (430, 310), 30, (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(500)
                self.energy_full = False
            if self.money_empty:
                self.load_text("money is not enough!", (410, 310), 30, (255, 0, 0))
                pygame.display.flip()
                pygame.time.delay(500)
                self.money_empty = False

    def mouse_select(self, button, level, energy_num, money_num):
        """鼠标点击"""
        if button.type == MOUSEBUTTONDOWN:
            mouse_down_x, mouse_down_y = button.pos
            print(button.pos)
            if level == 0:
                if self.type == 0:          # 树界面
                    for i in range(0, 10):
                        if Tree.position[i][0] < mouse_down_x < Tree.position[i][0] + self.fruit_width \
                                and Tree.position[i][1] - self.fruit_height < mouse_down_y < Tree.position[i][1]:
                            if energy_num <= 0:
                                self.type = 1
                            else:
                                level = i + 1
                    if Tree.energy_num_position[0] < mouse_down_x < Tree.energy_num_position[0]+60 \
                            and Tree.energy_num_position[1]-60 < mouse_down_y < Tree.energy_num_position[1]:  # 精力60*60
                        SoundPlay(SoundPlay.click)
                        self.type = 1
                else:               # 加精力弹窗界面
                    if 408 < mouse_down_x < 600 and 263 < mouse_down_y < 313:    # 点加精力按钮
                        SoundPlay(SoundPlay.click_button)
                        if money_num < 50:
                            self.money_empty = True
                        if energy_num >= 30:
                            self.energy_full = True
                        elif energy_num < 30 and money_num >= 50:
                            energy_num += 5
                            money_num -= 50
                    elif 619 < mouse_down_x < 638 and 158 < mouse_down_y < 177:   # 点叉号
                        self.type = 0
        if button.type == MOUSEBUTTONUP:
            pass
        return level, energy_num, money_num


class Element(pygame.sprite.Sprite):
    """ 元素类 """
    # 图标元组，包括6个小动物，
    animal = ('pic2/fox.png', 'pic2/bear.png', 'pic2/chick.png', 'pic2/eagle.png', 'pic2/frog.png', 'pic2/cow.png')
    ice = 'pic2/ice.png'  # 冰层
    brick = 'pic2/brick.png'  # 砖
    frame = 'pic2/frame.png'   # 选中框
    bling = ("pic2/bling1.png", "pic2/bling2.png", "pic2/bling3.png", "pic2/bling4.png", "pic2/bling5.png",\
             "pic2/bling6.png", "pic2/bling7.png", "pic2/bling8.png", "pic2/bling9.png")   # 消除动画

    ice_eli = ('pic2/ice0.png', 'pic2/ice1.png', 'pic2/ice2.png', 'pic2/ice3.png', 'pic2/ice4.png', 'pic2/ice5.png',\
               'pic2/ice6.png', 'pic2/ice7.png', 'pic2/ice8.png')    # 消除冰块动画

    # 得分图片
    score_level = ('pic2/good.png', 'pic2/great.png', 'pic2/amazing.png', 'pic2/excellent.png', 'pic2/unbelievable.png')
    none_animal = 'pic2/noneanimal.png'             # 无可消除小动物
    stop = 'pic2/exit.png'       # 暂停键
    stop_position = (20, 530)

    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position         # 左上角坐标
        self.speed = [0, 0]
        self.init_position = position

    def move(self, speed):
        self.speed = speed
        self.rect = self.rect.move(self.speed)
        if self.speed[0] != 0:    # 如果左右移动
            if abs(self.rect.left-self.init_position[0]) == self.rect[2]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]
        else:
            if abs(self.rect.top-self.init_position[1]) == self.rect[3]:
                self.init_position = self.rect.topleft
                self.speed = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Board(pygame.sprite.Sprite):
    step_board = 'pic2/step.png'              # 剩余步数板子
    step = ('pic2/0.png', 'pic2/1.png', 'pic2/2.png', 'pic2/3.png', 'pic2/4.png', 'pic2/5.png',\
            'pic2/6.png', 'pic2/7.png', 'pic2/8.png', 'pic2/9.png', )
    task_board = 'pic2/task.png'              # 任务板子
    ok = 'pic2/ok.png'    # ok勾
    # 关数板子
    levelBoard = ('pic2/level0.png', 'pic2/level1.png', 'pic2/level2.png', 'pic2/level3.png', 'pic2/level4.png', 'pic2/level5.png',
                  'pic2/level6.png', 'pic2/level7.png', 'pic2/level8.png', 'pic2/level9.png', 'pic2/level10.png')
    # xxx = 'pic2/x.png'   # 叉掉
    test = 'pic2/test.png'
    success_board = 'pic2/successtest1.png'  # 过关成功板子
    fail_board = 'pic2/failBoard.png'  # 任务失败
    step_add = 'pic2/step_add.png'  # 增加步数
    next = "pic2/next.png"  # 下一关按钮
    replay = "pic2/replay.png"  # 重玩图片
    stars = 'pic2/startest.png'  # 星星图片
    money = 'pic2/money.png'  # 银币
    energy = 'pic2/energ.png'  # 精力
    button_position = [[300, 465], [500, 465]]
    starts_position = [[280+50, 340], [375+38, 340], [460+35, 340]]

    def __init__(self, icon, position):
        super().__init__()
        self.image = pygame.image.load(icon).convert_alpha()
        self.speed = [0, 45]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = position                  # 左下角为坐标值

    def move(self):
        self.rect = self.rect.move(self.speed)
        if self.rect.bottom >= 543:
            self.speed = [0, -45]
        if self.speed == [0, -45] and self.rect.bottom <= 450:
            self.speed = [0, 0]

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Manager:
    """  数组类 """
    __screen_size = (900, 600)
    screen = pygame.display.set_mode(__screen_size, DOUBLEBUF, 32)
    __brick_size = 50
    __bg = pygame.image.load('pic2/bg.png').convert()
    stop_width = 63
    selected = [-1, -1]   # 现选中[row, col]
    exchange_sign = -1  # 未交换标志
    last_sel = [-1, -1]  # 上一次选中[row, col]
    change_value_sign = False  # 是否交换值标志，初始不交换
    death_sign = True  # 死图标志，初始不是死图
    boom_sel = [-1, -1]   # 四连消特效小动物所在位置 row，col
    level = 0  # 当前关卡数  初始第0关
    money = 100  # 金币
    energy_num = 30  # 精力值
    num_sign = True
    type = 2  # 0代表游戏中； 1代表完成任务，过关； -1代表步数用完，任务未完成，过关失败; 2代表未游戏状态，板子界面
    reset_mode = True     # 是否重新布局（每关布局）
    init_step = 15  # 每关规定步数
    step = init_step     # 代表游戏所剩余的步数
    score = 0        # 得数
    min = 20  # 分数中间值1
    max = 50  # 分数中间值2
    animal_num = [0, 0, 0, 0, 0, 0]   # 本关消除各小动物的个数
    ice_num = 0
    success_board = Board(Board.success_board, [200, 0])  # 过关成功板
    fail_board = Board(Board.fail_board, [200, 0])  # 任务失败板
    height, width = 9, 9
    row, col = 5, 5
    ice_list = [[-1 for col in range(21)]for row in range(21)]   # -1不画，1画冰
    animal = [[-1 for col in range(21)]for row in range(21)]   # -2消除的，-1不画，0-4小动物
    list_x, list_y = (__screen_size[0] - 11 * __brick_size) / 2, (__screen_size[1] - 11 * __brick_size) / 2  # 矩阵坐标

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.list_x = (Manager.__screen_size[0] - self.width * Manager.__brick_size) / 2
        self.list_y = (Manager.__screen_size[1] - self.height * Manager.__brick_size) / 2
        self.row, self.col = Manager.xy_rc(self.list_x, self.list_y)
        self.list_x, self.list_y = Manager.rc_xy(self.row, self.col)
        self.ice_list = [[-1 for col in range(21)]for row in range(21)]
        self.animal = [[-1 for col in range(21)]for row in range(21)]
        self.reset_animal()

    def reset_animal(self):
        for row in range(self.row, self.row + self.height):
            for col in range(self.col, self.col + self.width):
                self.animal[row][col] = random.randint(0, 5)

    @staticmethod
    def rc_xy(row, col):
        """row col 转 x，y坐标"""
        return int(Manager.list_x + (col-Manager.col)*Manager.__brick_size), int\
            (Manager.list_y+(row-Manager.row)*Manager.__brick_size)

    @staticmethod
    def xy_rc(x, y):
        """x，y坐标转row col"""
        return int((y-Manager.list_y)/Manager.__brick_size+Manager.row), int\
            ((x-Manager.list_x)/Manager.__brick_size+Manager.col)

    @staticmethod
    def draw_brick(x, y):
        brick = Element(Element.brick, (x, y))
        Manager.screen.blit(brick.image, brick.rect)

    def draw_task(self, task_animal_num, which_animal, \
                  board_position=(400, 90), animal_position=(430, 35), txt_position=(455, 60)):
        """画任务板子"""
        txt_size = 24
        txt_color = (0, 0, 0)
        Board(Board.task_board, board_position).draw(self.screen)
        if which_animal == 6:
            task_animal = Element(Element.ice, animal_position)
        else:
            task_animal = Element(Element.animal[which_animal], animal_position)
        task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
        task_animal.draw(self.screen)
        if which_animal == 6:
            if task_animal_num-self.ice_num <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num-self.ice_num), txt_position, txt_size, txt_color)
        else:
            if task_animal_num - self.animal_num[which_animal] <= 0:
                Board(Board.ok, (txt_position[0], txt_position[1]+15)).draw(self.screen)
            else:
                self.load_text(str(task_animal_num - self.animal_num[which_animal]), txt_position, txt_size, txt_color)

    def draw(self):
        """ 画背景，小动物等等 """
        # if self.level != 0:
        self.screen.blit(Manager.__bg, (0, 0))                    # 背景
        Board(Board.step_board, (0, 142)).draw(self.screen)       # 剩余步数板子
        tens = self.step//10  # 剩余步数十位数
        single = self.step % 10  # 剩余步数个位数
        if tens == 0:
            Board(Board.step[single], (790, 110)).draw(self.screen)
        else:
            Board(Board.step[tens], (775, 110)).draw(self.screen)
            Board(Board.step[single], (805, 110)).draw(self.screen)   # 剩余步数的数
        Board(Board.levelBoard[self.level], (30, 105)).draw(self.screen)  # 关卡数板子
        Element(Element.stop, Element.stop_position).draw(self.screen)    # 暂停键

        BrickGroup = pygame.sprite.Group()
        AnimalGroup = pygame.sprite.Group()
        IceGroup = pygame.sprite.Group()
        for i in range(0, 21):
            for j in range(0, 21):
                x, y = Manager.rc_xy(i, j)
                if self.animal[i][j] != -1:
                    BrickGroup.add(Element(Element.brick, (x, y)))
                    AnimalGroup.add(Element(Element.animal[self.animal[i][j]], (x, y)))
                if self.ice_list[i][j] != -1:
                    IceGroup.add(Element(Element.ice, (x, y)))
        BrickGroup.draw(self.screen)                                                         # 砖
        IceGroup.draw(self.screen)
        for animallist in AnimalGroup:
            self.screen.blit(animallist.image, animallist.rect)                           # 小动物
        if self.level == 1:
            self.draw_task(10, 4)
        elif self.level == 2:
            self.draw_task(21, 1)
        elif self.level == 3:
            self.draw_task(16, 4, (300, 90), (330, 35), (360, 60))
            self.draw_task(16, 5, (500, 90), (530, 35), (560, 60))
        elif self.level == 4:
            self.draw_task(18, 5, (300, 90), (330, 35), (360, 60))
            self.draw_task(18, 2, (500, 90), (530, 35), (560, 60))
        elif self.level == 5:
            self.draw_task(28, 2, (300, 90), (330, 35), (360, 60))
            self.draw_task(28, 0, (500, 90), (530, 35), (560, 60))
        elif self.level == 6:
            self.draw_task(70, 4)
        elif self.level == 7:
            self.draw_task(36, 1)
            self.draw_task(36, 2, (300, 90), (330, 35), (360, 60))
            self.draw_task(36, 0, (500, 90), (530, 35), (560, 60))
        elif self.level == 8:
            self.draw_task(15, 6)
        elif self.level == 9:
            self.draw_task(49, 6)
        else:
            self.draw_task(39, 6)

        if self.selected != [-1, -1]:
            frame_sprite = Element(Element.frame, Manager.rc_xy(self.selected[0], self.selected[1]))
            self.screen.blit(frame_sprite.image, frame_sprite.rect)                          # 选中框

        self.load_text('score:' + str(self.score), (300, 550), 30)                                 # 积分
        pygame.draw.rect(self.screen, (50, 150, 50, 180), Rect(300, 570, self.score * 2, 25))
        pygame.draw.rect(self.screen, (100, 200, 100, 180), Rect(300, 570, 200, 25), 2)
        return AnimalGroup

    def mouse_image(self):
        """"  更换鼠标图片 """
        mouse_cursor = pygame.image.load('pic2/mouse.png').convert_alpha()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 隐藏鼠标
        pygame.mouse.set_visible(False)
        # 计算光标的左上角位置
        mouse_x -= mouse_cursor.get_width() / 2
        mouse_y -= mouse_cursor.get_height() / 2
        self.screen.blit(mouse_cursor, (mouse_x, mouse_y))

    def mouse_select(self, button):
        """鼠标点击"""
        if button.type == MOUSEBUTTONDOWN:
            mouse_down_x, mouse_down_y = button.pos
            if self.type == 1:                                                       # 过关成功
                if Board.button_position[0][0] < mouse_down_x < Board.button_position[0][0]+100 \
                        and Board.button_position[0][1]-50 < mouse_down_y < Board.button_position[0][1]:  # 点击再来一次按钮
                    if self.energy_num < 5:
                        self.level = 0
                    self.reset_mode = True
                    # self.set_level_mode(self.level)
                elif Board.button_position[1][0] < mouse_down_x < Board.button_position[1][0]+100 \
                        and Board.button_position[1][1]-50 < mouse_down_y < Board.button_position[1][1]:  # 点击下一关按钮
                    if self.energy_num < 5:
                        self.level = 0
                    else:
                        self.level += 1                                                   # 关卡数加一
                    self.reset_mode = True
                    # self.set_level_mode(self.level)
                # elif self.success_board.rect[0]+410 < mouse_down_x < self.success_board.rect[0]+410+55 \
                #         and self.success_board.rect.bottom+245-55 < mouse_down_x < self.success_board.rect.bottom+245:
                elif 610 < mouse_down_x < 610 + 55 and 205 - 55 < mouse_down_y < 205:   # x
                    self.level = 0
                    self.reset_mode = True

            elif self.type == -1:                                                    # 过关失败
                if Board.button_position[1][0] < mouse_down_x < Board.button_position[1][0]+100 \
                        and Board.button_position[1][1]-50 < mouse_down_y < Board.button_position[1][1]:  # 点击再来一次按钮
                    if self.energy_num < 5:
                        self.level = 0
                    self.reset_mode = True
                elif Board.button_position[0][0] < mouse_down_x < Board.button_position[0][0]+100 \
                        and Board.button_position[0][1]-50 < mouse_down_y < Board.button_position[0][1]:   # 点击再来5步按钮
                    if self.money < 5:
                        self.level = 0
                    else:
                        self.money -= 5
                        self.step += 5
                        self.type = 0                           # 游戏中
                        self.fail_board = Board(Board.fail_board, [200, 0])
                # elif self.success_board.rect[0] + 410 < mouse_down_x < self.success_board.rect[0] + 410 + 55 \
                #         and self.success_board.rect.bottom+245-55 < mouse_down_x < self.success_board.rect.bottom+245:
                elif 610 < mouse_down_x < 610 + 55 and 205 - 55 < mouse_down_y < 205:   # x
                    self.level = 0
                    self.reset_mode = True

            elif self.type == 0:
                if self.list_x < mouse_down_x < self.list_x + Manager.__brick_size * self.width \
                        and self.list_y < mouse_down_y < self.list_y + Manager.__brick_size * self.height:
                    mouse_selected = Manager.xy_rc(mouse_down_x, mouse_down_y)
                    if self.animal[mouse_selected[0]][mouse_selected[1]] != -1:
                        SoundPlay(SoundPlay.click)
                        self.selected = mouse_selected
                        if (self.last_sel[0] == self.selected[0] and abs(self.last_sel[1] - self.selected[1]) == 1) \
                                or (self.last_sel[1] == self.selected[1] and abs(self.last_sel[0] - self.selected[0]) == 1):
                            self.exchange_sign = 1              # 点击相邻的，交换
                elif Element.stop_position[0] < mouse_down_x < Element.stop_position[0]+self.stop_width\
                        and Element.stop_position[1] < mouse_down_y < Element.stop_position[1]+self.stop_width:   # 点推出
                    SoundPlay(SoundPlay.click_button)
                    self.level = 0
                    self.reset_mode = True
                else:
                    self.selected = [-1, -1]

        if button.type == MOUSEBUTTONUP:
            pass

    def exchange(self, spritegroup):
        """点击后交换"""
        if self.exchange_sign == -1:      # 未交换
            self.last_sel = self.selected
        if self.exchange_sign == 1:
            last_x, last_y = Manager.rc_xy(self.last_sel[0], self.last_sel[1])
            sel_x, sel_y = Manager.rc_xy(self.selected[0], self.selected[1])
            if self.last_sel[0] == self.selected[0]:  # 左右相邻
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [self.selected[1]-self.last_sel[1], 0]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [self.last_sel[1]-self.selected[1], 0]
            else:   # 上下相邻
                for animallist in spritegroup:
                    if animallist.rect.topleft == (last_x, last_y):
                        last_sprite = animallist
                        last_sprite.speed = [0, self.selected[0]-self.last_sel[0]]
                    elif animallist.rect.topleft == (sel_x, sel_y):
                        selected_sprite = animallist
                        selected_sprite.speed = [0, self.last_sel[0]-self.selected[0]]
            while last_sprite.speed != [0, 0]:
                pygame.time.delay(5)
                self.draw_brick(last_x, last_y)
                self.draw_brick(sel_x, sel_y)
                last_sprite.move(last_sprite.speed)
                selected_sprite.move(selected_sprite.speed)
                self.screen.blit(last_sprite.image, last_sprite.rect)
                self.screen.blit(selected_sprite.image, selected_sprite.rect)
                pygame.display.flip()

            self.change_value()
            if self.eliminate_animal():
                self.step -= 1
            else:
                self.change_value()
            self.change_value_sign = False
            self.boom_sel = self.selected
            self.exchange_sign = -1
            self.selected = [-1, -1]

    def change_value(self):
        """交换值"""
        temp = self.animal[self.last_sel[0]][self.last_sel[1]]
        self.animal[self.last_sel[0]][self.last_sel[1]] = self.animal[self.selected[0]][self.selected[1]]
        self.animal[self.selected[0]][self.selected[1]] = temp

    def load_text(self, text, position, txt_size, txt_color=(255, 255, 255)):
        my_font = pygame.font.SysFont(None, txt_size)
        text_screen = my_font.render(text, True, txt_color)
        self.screen.blit(text_screen, position)

    def death_map(self):
        """判断死图，更新图"""
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] != -1:
                    if self.animal[i][j] == self.animal[i][j+1]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i+1][j-1]] \
                                    and self.animal[i][j-1] != -1) or \
                                (self.animal[i][j] in [self.animal[i-1][j+2], self.animal[i+1][j+2]] \
                                         and self.animal[i][j+2] != -1):
                            """a     b
                                 a a
                               c     d"""
                            self.death_sign = False
                            break
                    if self.animal[i][j] == self.animal[i+1][j]:
                        if (self.animal[i][j] in [self.animal[i-1][j-1], self.animal[i-1][j+1]] \
                                    and self.animal[i-1][j] != -1) or \
                                (self.animal[i][j] in [self.animal[i+2][j - 1], self.animal[i+2][j + 1]] \
                                         and self.animal[i+2][j] != -1):
                            """a   b
                                 a
                                 a 
                               c   d"""
                            self.death_sign = False
                            break
                    else:
                        if self.animal[i-1][j-1] == self.animal[i][j]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i-1][j] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i][j-1] != -1):
                                """a   a      a   b
                                     a          a
                                   c          a    """
                                self.death_sign = False
                                break
                        if self.animal[i][j] == self.animal[i+1][j+1]:
                            if (self.animal[i][j] == self.animal[i-1][j+1] and self.animal[i][j+1] != -1)\
                                    or (self.animal[i][j] == self.animal[i+1][j-1] and self.animal[i+1][j] != -1):
                                """    a          b
                                     a          a
                                   b   a      a   a"""
                                self.death_sign = False
                                break
        if self.death_sign:
            pygame.time.delay(500)
            Element(Element.none_animal, (230, 150)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)
            temp = [self.step, self.score, self.animal_num, self.ice_num, self.energy_num]
            self.reset_mode = True
            self.set_level_mode(self.level)
            self.step = temp[0]
            self.score = temp[1]
            self.animal_num = temp[2]
            self.ice_num = temp[3]
            self.energy_num = temp[4]
        else:
            self.death_sign = True

    # def eliminate_animal(self):
    #     """消除小动物"""
    #     score_level = self.score       # 当前得分
    #     """543连消"""
    #     for i in range(self.row, self.row + self.height):
    #         for j in range(self.col, self.col + self.width):
    #             if self.animal[i][j] == self.animal[i][j+1] == self.animal[i][j+2] == self.animal[i][j-1] == self.animal[i][j-2] \
    #                     and self.animal[i][j] != -1:            # 横五
    #                 if self.selected != [-1, -1]:
    #                     self.change_value_sign = True
    #                 self.score += 5
    #                 # print("5", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[4])                         # 消除声音4
    #                 self.animal_num[self.animal[i][j]] += 5                     # 消除某种小动物计数
    #                 self.animal[i][j-2] = self.animal[i][j+1] = self.animal[i][j+2] = self.animal[i][j-1] = -2
    #                 # self.animal[i][j + 2] = 15
    #                 self.animal[i][j] = -2
    #             elif self.animal[i][j] == self.animal[i][j+1] == self.animal[i][j+2] == self.animal[i][j+3] \
    #                     and self.animal[i][j] != -1:            # 横四
    #                 if self.selected != [-1, -1]:
    #                     self.change_value_sign = True
    #                 self.score += 3
    #                 # print("横四", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[3])                                # 消除声音3
    #                 self.animal_num[self.animal[i][j]] += 4                            # 消除某种小动物计数
    #                 if i == self.boom_sel[0] and j+1 == self.boom_sel[1]:
    #                     # self.animal[i][j+1] += 5
    #                     self.animal[i][j + 1] = -2
    #                     self.animal[i][j] = self.animal[i][j + 2] = self.animal[i][j + 3] = -2
    #                 else:
    #                     # self.animal[i][j+2] += 5
    #                     self.animal[i][j + 2] = -2
    #                     self.animal[i][j] = self.animal[i][j + 1] = self.animal[i][j + 3] = -2
    #             elif self.animal[i][j] == self.animal[i][j + 1] == self.animal[i][j + 2] and self.animal[i][j] != -1:
    #                 if self.selected != [-1, -1]:              # 横3
    #                     self.change_value_sign = True
    #                 self.score += 2
    #                 # print("横三", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[0])  # 消除声音0
    #                 self.animal_num[self.animal[i][j]] += 3  # 消除某种小动物计数
    #                 self.animal[i][j] = self.animal[i][j + 1] = self.animal[i][j + 2] = -2
    #             if self.animal[i][j] == self.animal[i+1][j] == self.animal[i+2][j] == self.animal[i-1][j] == self.animal[i-2][j] \
    #                     and self.animal[i][j] != -1:             # 纵五
    #                 if self.selected != [-1, -1]:
    #                     self.change_value_sign = True
    #                 self.score += 5
    #                 # print("55", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[4])                         # 消除声音4
    #                 self.animal_num[self.animal[i][j]] += 5                     # 消除某种小动物计数
    #                 self.animal[i+2][j] = self.animal[i + 1][j] = self.animal[i-1][j] = self.animal[i-2][j] = -2
    #                 # self.animal[i + 2][j] = 15
    #                 self.animal[i][j] = -2
    #             elif self.animal[i][j] == self.animal[i+1][j] == self.animal[i+2][j] == self.animal[i+3][j] \
    #                     and self.animal[i][j] != -1:            # 纵四
    #                 if self.selected != [-1, -1]:
    #                     self.change_value_sign = True
    #                 self.score += 3
    #                 # print("纵四", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[3])                                 # 消除声音3
    #                 self.animal_num[self.animal[i][j]] += 4                             # 消除某种小动物计数
    #                 if i+1 == self.boom_sel[0] and j == self.boom_sel[1]:
    #                     # self.animal[i + 1][j] += 5
    #                     self.animal[i + 1][j] = -2
    #                     self.animal[i][j] = self.animal[i + 2][j] = self.animal[i + 3][j] = -2
    #                 else:
    #                     # self.animal[i + 2][j] += 5
    #                     self.animal[i + 2][j] = -2
    #                     self.animal[i][j] = self.animal[i + 1][j] = self.animal[i + 3][j] = -2
    #             elif self.animal[i][j] == self.animal[i + 1][j] == self.animal[i + 2][j] and self.animal[i][j] != -1:
    #                 if self.selected != [-1, -1]:           # 纵3
    #                     self.change_value_sign = True
    #                 self.score += 2
    #                 # print("纵三", [i, j])
    #                 SoundPlay(SoundPlay.eliminate[0])  # 消除声音0
    #                 self.animal_num[self.animal[i][j]] += 3  # 消除某种小动物计数
    #                 self.animal[i][j] = self.animal[i + 1][j] = self.animal[i + 2][j] = -2
    #
    #     """丁字，勾连消"""
    #     for i in range(self.row, self.row + self.height):
    #         for j in range(self.col, self.col + self.width):
    #             # 丁字
    #             if self.animal[i][j] == self.animal[i][j-1] == self.animal[i][j+1] and self.animal[i][j] != -1:
    #                 if self.animal[i][j] == self.animal[i+1][j] == self.animal[i+2][j]:  # 下丁
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("下丁", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[2])                                              # 消除声音2
    #                     self.animal_num[self.animal[i][j]] += 5                                        # 消除某种小动物计数
    #                     self.animal[i + 1][j] = self.animal[i + 2][j] = self.animal[i][j-1] = self.animal[i][j+1] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #                 elif self.animal[i][j] == self.animal[i-1][j] == self.animal[i-2][j]:  # 上丁
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("上丁", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[2])                                                   # 消除声音2
    #                     self.animal_num[self.animal[i][j]] += 5                                       # 消除某种小动物计数
    #                     self.animal[i][j - 1] = self.animal[i][j + 1] = self.animal[i-1][j] = self.animal[i-2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #             if self.animal[i][j] == self.animal[i-1][j] == self.animal[i+1][j] and self.animal[i][j] != -1:
    #                 if self.animal[i][j] == self.animal[i][j-1] == self.animal[i][j-2]:  # 左丁
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("下丁", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[2])  # 消除声音2
    #                     self.animal_num[self.animal[i][j]] += 5  # 消除某种小动物计数
    #                     self.animal[i + 1][j] = self.animal[i + 2][j] = self.animal[i][j - 1] = self.animal[i][j + 1] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #                 elif self.animal[i][j] == self.animal[i][j+1] == self.animal[i][j+2]:  # 右丁
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("上丁", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[2])  # 消除声音2
    #                     self.animal_num[self.animal[i][j]] += 5  # 消除某种小动物计数
    #                     self.animal[i][j - 1] = self.animal[i][j + 1] = self.animal[i - 1][j] = self.animal[i - 2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #             # 勾
    #             elif self.animal[i][j] == self.animal[i][j+1] == self.animal[i][j+2] and self.animal[i][j] != -1:
    #                 if self.animal[i][j] == self.animal[i+1][j] == self.animal[i+2][j]:  # 右下
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("右下", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[1])                                                   # 消除声音1
    #                     self.animal_num[self.animal[i][j]] += 5                                        # 消除某种小动物计数
    #                     self.animal[i][j + 1] = self.animal[i][j + 2] = self.animal[i+1][j] = self.animal[i+2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #                 elif self.animal[i][j] == self.animal[i-1][j] == self.animal[i-2][j]:            # 右上
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("右上", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[1])                                                   # 消除声音1
    #                     self.animal_num[self.animal[i][j]] += 5                                       # 消除某种小动物计数
    #                     self.animal[i][j + 1] = self.animal[i][j + 2] = self.animal[i-1][j] = self.animal[i-2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #             elif self.animal[i][j] == self.animal[i][j-1] == self.animal[i][j-2] and self.animal[i][j] != -1:
    #                 if self.animal[i][j] == self.animal[i+1][j] == self.animal[i+2][j]:  # 左下
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("左下", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[1])                                                   # 消除声音1
    #                     self.animal_num[self.animal[i][j]] += 5                                        # 消除某种小动物计数
    #                     self.animal[i][j - 1] = self.animal[i][j - 2] = self.animal[i+1][j] = self.animal[i+2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #                 elif self.animal[i][j] == self.animal[i-1][j] == self.animal[i-2][j]:            # 左上
    #                     if self.selected != [-1, -1]:
    #                         self.change_value_sign = True
    #                     self.score += 3
    #                     # print("左上", [i, j])
    #                     SoundPlay(SoundPlay.eliminate[1])                                                   # 消除声音1
    #                     self.animal_num[self.animal[i][j]] += 5                                        # 消除某种小动物计数
    #                     self.animal[i][j - 1] = self.animal[i][j - 2] = self.animal[i-1][j] = self.animal[i-2][j] = -2
    #                     # self.animal[i][j] += 10
    #                     self.animal[i][j] = -2
    #     eliminate_ice = []
    #     for i in range(self.row, self.row + self.height):
    #         for j in range(self.col, self.col + self.width):
    #             if self.animal[i][j] == 5 and (-2 in [self.animal[i+1][j], self.animal[i-1][j], self.animal[i][j+1], self.animal[i][j-1]]):
    #                 eliminate_ice.append((i, j))
    #     # print(len(eliminate_ice))
    #     for n in range(len(eliminate_ice)):
    #         self.animal[eliminate_ice[n][0]][eliminate_ice[n][1]] = -2
    #
    #     self.fall_animal()
    #
    #     score_level = self.score-score_level     # 一次点击交换后消除的得分值
    #
    #     # 根据得分差值，播放不同声音，画不同图片，good，great，amazing，excellent，unbelievable，
    #     if score_level < 5:
    #         pass
    #     elif score_level < 8:           # 5 good
    #         SoundPlay(SoundPlay.score_level[0])
    #         Element(Element.score_level[0], (350, 250)).draw(self.screen)
    #         pygame.display.flip()
    #         pygame.time.delay(500)
    #     elif score_level < 10:          # 8 great
    #         SoundPlay(SoundPlay.score_level[1])
    #         Element(Element.score_level[1], (350, 250)).draw(self.screen)
    #         pygame.display.flip()
    #         pygame.time.delay(500)
    #     elif score_level < 15:          # 10 amazing
    #         SoundPlay(SoundPlay.score_level[2])
    #         Element(Element.score_level[2], (350, 250)).draw(self.screen)
    #         pygame.display.flip()
    #         pygame.time.delay(500)
    #     elif score_level < 20:          # 15 excellent
    #         SoundPlay(SoundPlay.score_level[3])
    #         Element(Element.score_level[3], (350, 250)).draw(self.screen)
    #         pygame.display.flip()
    #         pygame.time.delay(500)
    #     elif score_level >= 20:         # 20 unbelievable
    #         SoundPlay(SoundPlay.score_level[4])
    #         Element(Element.score_level[4], (350, 250)).draw(self.screen)
    #         pygame.display.flip()
    #         pygame.time.delay(500)
    #     return self.change_value_sign      # 返回是否交换值标志

    def exist_left(self, i, j, num):
        sl = 0
        for temp in range(0,int(num)):
            # print("leftxxxxxx", temp,self.animal[i][j], self.animal[i + temp][j])
            if self.animal[i][j] == self.animal[i][j-temp] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                # j = j - 1
                # self.animal[i][j] = self.animal[i][j-1]
                sl += 1
                # print('left', 'judge num',sl,num,i, j)
                if sl == num:
                    # print('left', 'return true')
                    return True
            else:
                # print('left', 'return false')
                return False

    def exist_right(self, i, j, num):
        sr = 0
        for temp in range(0, int(num)):
            # print("rightxxxxxx",temp, self.animal[i][j], self.animal[i + temp][j])
            if self.animal[i][j] == self.animal[i][j + temp] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                # j = j + 1
                # self.animal[i][j] = self.animal[i][j + 1]
                sr = sr + 1
                # print('right', 'judge num',sr,num,i, j)
                if sr == num:
                    # print('right','return true')
                    return True
            else:
                # print('right', 'return false')
                return False

    def exist_up(self, i, j, num):
        su = 0
        for temp in range(0, int(num)):
            # print("upxxxxxx", temp,self.animal[i][j], self.animal[i + temp][j])
            if self.animal[i][j] == self.animal[i - temp][j] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                # self.animal[i][j] = self.animal[i - 1][j]
                # i = i - 1
                su = su + 1
                # print('up', 'judge num',su,num,i, j)
                if su == num:
                    # print('up', 'return true')
                    return True
            else:
                # print('up', 'return false')
                return False

    def exist_down(self, i, j, num):
        sd = 0
        for temp in range(0, int(num)):
            # print("downxxxxxx",temp,self.animal[i][j],self.animal[i+temp][j])
            if self.animal[i][j] == self.animal[i + temp][j] and self.animal[i][j]!= -1 and self.animal[i][j] != -2:
                # self.animal[i][j] = self.animal[i + 1][j]
                # i = i + 1
                sd = sd + 1
                # print('down', 'judge num',sd,num,i, j)
                if sd == num:
                    # print('down', 'return true')
                    return True
                else:pass
            else:
                # print('down', 'return false')
                return False

    def change_left(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        print('excute changeleft')
        for k in range(0,int(num)):
            print('location',i, j-k,self.animal[i][j-k])
            self.animal[i][j-k] = -2
        # cl = 1
        # for temp in (0, num):
        #     if self.animal[i][j] == self.animal[i][j - 1] :
        #         self.animal[i][j] = self.animal[i][j - 1] = -2
        #         cl = cl + 1
        #         print('changeleft', 'judge num')
        #         if cl == num:
        #             print('changeleft', 'return true')
        #             return True
        #     else:
        #         print('changeleft', 'return false')
        #         return False

    def change_right(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        print('excute changeright')
        for k in range(0,int(num)):
            print('location', i, j + k, self.animal[i][j + k])
            self.animal[i][j+k] = -2
        # cr = 1
        # for temp in (0, num):
        #     if self.animal[i][j] == self.animal[i][j + 1] :
        #         self.animal[i][j] = self.animal[i][j + 1] = -2
        #         cr = cr + 1
        #         print('changeright', 'judge num')
        #         if cr == num:
        #             print('changeright', 'return true')
        #             return True
        #     else:
        #         print('changeright', 'return false')
        #         return False

    def change_up(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        print('excute changeup')
        for k in range(0,int(num)):
            print('location', i - k, j, self.animal[i - k][j ])
            self.animal[i-k][j] = -2
        # cu = 1
        # for temp in (0, num):
        #     if self.animal[i][j] == self.animal[i - 1][j] :
        #         self.animal[i][j] = self.animal[i - 1][j] = -2
        #         cu = cu + 1
        #         print('changeup', 'judge num')
        #         if cu == num:
        #             print('changeup', 'return true')
        #             return True
        #     else:
        #         print('changeup', 'return false')
        #         return False

    def change_down(self, i, j, num):
        self.change_value_sign = True
        self.score += num
        print('excute changedown')
        for k in range(0,int(num)):
            print('location', i + k, j, self.animal[i + k][j])
            self.animal[i+k][j] = -2
        # cd = 1
        # for temp in (0, num):
        #     if self.animal[i][j] == self.animal[i + 1][j]:
        #         self.animal[i][j] = self.animal[i + 1][j] = -2
        #         cd = cd + 1
        #         print('changedown', 'judge num')
        #         if cd == num:
        #             print('changedown', 'return true')
        #             return True
        #     else:
        #         print('changedown', 'return false')
        #         return False

    def eliminate_animal(self):
        score_level = self.score
        self.change_value_sign = False
        for i in range(self.row, self.row + self.height):
            for j in range(self.col, self.col + self.width):
                if self.exist_right(i, j, 5):
                    self.change_value_sign = True
                    if self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  # 消除声音4
                        self.change_right(i, j, 5)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_right(i, j, 5)
                elif self.exist_right(i, j, 4):
                    self.change_value_sign = True
                    if self.exist_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_right(i, j, 4)
                        self.change_down(i, j+1, 3)
                    elif self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_right(i, j, 4)
                        self.change_down(i, j+2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        SoundPlay(SoundPlay.eliminate[1])  # 消除声音4
                        self.change_right(i, j, 4)
                elif self.exist_right(i, j, 3):
                    self.change_value_sign = True
                    if self.exist_down(i, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_right(i, j, 3)
                        self.change_down(i, j, 3)
                    elif self.exist_down(i, j+1, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_right(i, j, 3)
                        self.change_down(i, j+1, 3)
                    elif self.exist_down(i, j+2, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_right(i, j, 3)
                        self.change_down(i, j + 2, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        SoundPlay(SoundPlay.eliminate[0])  # 消除声音4
                        self.change_right(i, j, 3)
                elif self.exist_down(i, j, 5):
                    self.change_value_sign = True
                    if self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  # 消除声音4
                        self.change_down(i, j, 5)
                        self.change_right(i+2, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  # 消除声音4
                        self.change_down(i, j, 5)
                        self.change_left(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 5)
                elif self.exist_down(i, j, 4):
                    self.change_value_sign = True
                    if self.exist_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 4)
                        self.change_left(i+1, j, 3)
                    elif self.exist_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 4)
                        self.change_right(i+1, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 4)
                        self.change_left(i+2, j, 3)
                    elif self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 4)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 4
                        SoundPlay(SoundPlay.eliminate[1])  # 消除声音4
                        self.change_down(i, j, 4)
                elif self.exist_down(i, j, 3):
                    self.change_value_sign = True
                    if self.exist_left(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+1, j, 3)
                    elif self.exist_right(i+1, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_right(i+1, j, 3)
                    elif self.exist_left(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                    elif self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_right(i+2, j, 3)
                    # elif self.exist_left(i, j, 2) and self.exist_right(i, j, 2):
                    #     self.change_down(i, j, 3)
                    #     self.change_left(i, j, 2)
                    #     self.change_right(i, j, 2)
                    elif self.exist_left(i+2, j, 2) and self.exist_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 5
                        SoundPlay(SoundPlay.eliminate[2])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 2)
                    elif self.exist_left(i+2, j, 2) and self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 2)
                        self.change_right(i+2, j, 3)
                    elif self.exist_left(i+2, j, 3) and self.exist_right(i+2, j, 2):
                        self.animal_num[self.animal[i][j]] += 6
                        SoundPlay(SoundPlay.eliminate[3])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 2)
                    elif self.exist_left(i+2, j, 3) and self.exist_right(i+2, j, 3):
                        self.animal_num[self.animal[i][j]] += 7
                        SoundPlay(SoundPlay.eliminate[4])  # 消除声音4
                        self.change_down(i, j, 3)
                        self.change_left(i+2, j, 3)
                        self.change_right(i+2, j, 3)
                    else:
                        self.animal_num[self.animal[i][j]] += 3
                        SoundPlay(SoundPlay.eliminate[0])  # 消除声音4
                        self.change_down(i, j, 3)

        self.fall_animal()
        score_level = self.score - score_level  # 一次点击交换后消除的得分值

        # 根据得分差值，播放不同声音，画不同图片，good，great，amazing，excellent，unbelievable，
        if score_level < 5:
            pass
        elif score_level < 8:           # 5 good
            SoundPlay(SoundPlay.score_level[0])
            Element(Element.score_level[0], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)
        elif score_level < 10:          # 8 great
            SoundPlay(SoundPlay.score_level[1])
            Element(Element.score_level[1], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)
        elif score_level < 15:          # 10 amazing
            SoundPlay(SoundPlay.score_level[2])
            Element(Element.score_level[2], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)
        elif score_level < 20:          # 15 excellent
            SoundPlay(SoundPlay.score_level[3])
            Element(Element.score_level[3], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)
        elif score_level >= 20:         # 20 unbelievable
            SoundPlay(SoundPlay.score_level[4])
            Element(Element.score_level[4], (350, 250)).draw(self.screen)
            pygame.display.flip()
            pygame.time.delay(500)

        return self.change_value_sign      # 返回是否交换值标志

    # def fall_animal(self):
    #     """下落函数"""
    #     index = 0
    #     for i in range(self.row, self.row + self.height):
    #         for j in range(self.col, self.col + self.width):
    #             if self.animal[i][j] == -2:
    #                 x, y = self.rc_xy(i, j)
    #                 for index in range(0, 6):
    #                     pygame.time.delay(100)
    #                     self.draw_brick(x, y)
    #                     Element(Element.bling[index], (x, y)).draw(self.screen)
    #                     pygame.display.flip()
    #
    #                 for m in range(i, self.row - 1, -1):
    #                     if self.animal[m - 1][j] != -1:
    #                         x, y = self.rc_xy(m - 1, j)
    #                         animal = Element(Element.animal[self.animal[m - 1][j]], self.rc_xy(m - 1, j))
    #                         animal.move([0, 10])
    #                         # pygame.time.delay(5)
    #                         self.draw_brick(x, y)
    #                         animal.draw(self.screen)
    #                         pygame.display.flip()
    #                         self.animal[m][j] = self.animal[m - 1][j]
    #                     else:
    #                         self.animal[m][j] = random.randint(0, 4)
    #                         break

    # def eliminate_animal_test(self):
    #     s = 1
    #     for i in range(self.row, self.row+self.height):
    #         for j in range(self.col, self.col+self.width):
    #             # current_rc = [i, j]
    #             if self.animal[i][j] ==self.animal[i][j+1]:
    #                 s += 1
    #             else:
    #                 if s

    # def judge_animal(self, rc1, rc2):
    #     """判断两坐标之间小动物是否相等"""
    #     judge_sign = True
    #     if rc1[0] == rc2[0]:
    #         i = rc1[0]
    #         for j in range(rc1[1], rc2[1]):
    #             if self.animal[i][j] != self.animal[i][j+1]:
    #                 judge_sign = False
    #                 break
    #     elif rc1[1] == rc2[1]:
    #         j = rc1[1]
    #         for i in range(rc1[0], rc2[0]):
    #             if self.animal[i][j] != self.animal[i+1][j]:
    #                 judge_sign = False
    #                 break
    #     else:
    #         print("rc error!")
    #     return judge_sign

    # def fall_animal(self):
    #     """下落函数"""
    #     for i in range(self.row, self.row+self.height):
    #         for j in range(self.col, self.col+self.width):
    #             if self.animal[i][j] == -2:
    #                 for m in range(i, self.row-1, -1):
    #                     if self.animal[m-1][j] != -1:
    #                         self.animal[m][j] = self.animal[m-1][j]
    #                     else:
    #                         self.animal[m][j] = random.randint(0, 5)
    #                         break

    def fall_animal(self):
        """下落函数"""
        clock = pygame.time.Clock()
        position = []
        ice_position = []
        for i in range(self.row, self.row+self.height):
            for j in range(self.col, self.col+self.width):
                if self.animal[i][j] == -2:
                    x, y = self.rc_xy(i, j)
                    position.append((x, y))
                    if self.ice_list[i][j] == 1:
                        ice_position.append((x, y))
        if position != []:
            for index in range(0, 9):
                # pygame.time.delay(50)
                # clock.tick()
                clock.tick(20)
                for pos in position:
                    self.draw_brick(pos[0], pos[1])
                    if pos in ice_position:
                        Element(Element.ice_eli[index], (pos[0], pos[1])).draw(self.screen)
                    Element(Element.bling[index], (pos[0], pos[1])).draw(self.screen)
                    pygame.display.flip()
        # speed = [0, 1]
        # while speed != [0, 0]:
        #     for i in range(self.row, self.row+self.height):
        #         for j in range(self.col, self.col+self.width):
        #             if self.animal[i][j] == -2:
        #                 self.ice_list[i][j] = -1
        #                 for m in range(i, self.row - 1, -1):
        #                     if self.animal[m - 1][j] != -1:
        #                         x, y = self.rc_xy(m - 1, j)
        #                         animal = Element(Element.animal[self.animal[m - 1][j]], (x, y))
        #                         # clock.tick(20)
        #                         animal.move([0, 1])
        #                         speed = animal.speed
        #                         self.draw_brick(x, y)
        #                         animal.draw(self.screen)
        #                         pygame.display.flip()
        #                         # self.animal[m][j] = self.animal[m - 1][j]
        #                     else:
        #                         # self.animal[m][j] = random.randint(0, 5)
        #                         break
        # fall_animal_list = []
        # for i in range(self.row, self.row + self.height):
        #     for j in range(self.col, self.col + self.width):
        #         if self.animal[i][j] == -2:
        #             brick_position = []
        #             x, y = self.rc_xy(i, j)
        #             if self.ice_list[i][j] == 1:
        #                 SoundPlay(SoundPlay.ice_break)
        #                 self.ice_num += 1
        #                 self.ice_list[i][j] = -1
        #             fall_animal_list = []
        #             brick_position.append((x, y))
        #             speed = [0, 1]
        #             for m in range(i, self.row - 1, -1):
        #                 if self.animal[m - 1][j] != -1:
        #                     x, y = self.rc_xy(m - 1, j)
        #                     brick_position.append((x, y))
        #                     animal = Element(Element.animal[self.animal[m - 1][j]], (x, y))
        #                     fall_animal_list.append(animal)
        #                     self.animal[m][j] = self.animal[m - 1][j]
        #                 else:
        #                     self.animal[m][j] = random.randint(0, 5)
        #                     break
        #             while speed != [0, 0] and fall_animal_list != []:
        #                 # clock.tick(300)
        #                 for position in brick_position:
        #                     self.draw_brick(position[0], position[1])
        #                 for animal_sprite in fall_animal_list:
        #                     animal_sprite.move(speed)
        #                     animal_sprite.draw(self.screen)
        #                     print('animal speed', animal_sprite.speed)
        #                     speed = animal_sprite.speed
        #                 pygame.display.flip()
        for i in range(self.row, self.row + self.height):
            brick_position = []
            fall_animal_list = []
            speed = [0, 1]
            for j in range(self.col, self.col + self.width):
                if self.animal[i][j] == -2:

                    x, y = self.rc_xy(i, j)
                    if self.ice_list[i][j] == 1:
                        SoundPlay(SoundPlay.ice_break)
                        self.ice_num += 1
                        self.ice_list[i][j] = -1

                    brick_position.append((x, y))

                    for m in range(i, self.row - 1, -1):
                        if self.animal[m - 1][j] != -1:
                            x, y = self.rc_xy(m - 1, j)
                            brick_position.append((x, y))
                            animal = Element(Element.animal[self.animal[m - 1][j]], (x, y))
                            fall_animal_list.append(animal)
                            self.animal[m][j] = self.animal[m - 1][j]
                        else:
                            self.animal[m][j] = random.randint(0, 5)
                            break
            while speed != [0, 0] and fall_animal_list != []:
                # clock.tick(300)
                for position in brick_position:
                    self.draw_brick(position[0], position[1])
                for animal_sprite in fall_animal_list:
                    animal_sprite.move(speed)
                    animal_sprite.draw(self.screen)
                    print('animal speed', animal_sprite.speed)
                    speed = animal_sprite.speed
                pygame.display.flip()



    def judgeNext(self, type, score):
        """判断下一步是过关还是失败"""
        if type == 1:      # 过关
            self.loadFnsWindow(score)
        elif type == -1:   # 过关失败
            self.loadFailWindow()

    def loadFailWindow(self):
        """画失败板子及相关按钮"""
        sound_sign = 0
        retry = Board(Board.replay, Board.button_position[1])               # 右再来一次按钮
        step_add = Board(Board.step_add, Board.button_position[0])          # 左再来5步按钮
        self.screen.blit(self.fail_board.image, self.fail_board.rect)   # 过关失败板
        self.screen.blit(step_add.image, step_add.rect)
        self.screen.blit(retry.image, retry.rect)
        while self.fail_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.fail_board.image, self.fail_board.rect)
            self.fail_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                SoundPlay(SoundPlay.board_sound)
                sound_sign = 1

    def loadFnsWindow(self, score):
        """过关成功及相关按钮"""
        sound_sign = 0
        next_level = Board(Board.next, Board.button_position[1])              # 右下一关按钮
        replay = Board(Board.replay, Board.button_position[0])                # 左再来一次按钮
        self.screen.blit(self.success_board.image, self.success_board.rect)     # 过关成功板
        self.screen.blit(next_level.image, next_level.rect)
        self.screen.blit(replay.image, replay.rect)
        while self.success_board.speed != [0, 0]:
            self.draw()
            self.screen.blit(self.success_board.image, self.success_board.rect)
            self.success_board.move()
            pygame.display.flip()
            if sound_sign == 0:
                SoundPlay(SoundPlay.board_sound)
                sound_sign = 1
        self.displayStars(score)                 # 画星星
        # 画银币
        self.load_text(str(self.score*2), (Board.starts_position[0][0]+75, Board.starts_position[0][0]+46), 20, (0, 0, 0))

    def displayStars(self, score):
        """画星星"""
        star1 = Board(Board.stars, Board.starts_position[0])
        star2 = Board(Board.stars, Board.starts_position[1])
        star3 = Board(Board.stars, Board.starts_position[2])
        if 0 <= score < self.min:
            self.load_text(str(1), (Board.starts_position[1][0]+48, Board.starts_position[1][1]+35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
        elif self.min <= score <= self.max:
            self.load_text(str(2), (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
        elif score > self.max:
            self.load_text(str(5), (Board.starts_position[1][0] + 48, Board.starts_position[1][1] + 35), 20, (0, 0, 0))
            self.screen.blit(star1.image, star1.rect)
            self.screen.blit(star2.image, star2.rect)
            self.screen.blit(star3.image, star3.rect)
        # print("m.energy_num", self.energy_num)
        pygame.display.flip()

    def set_level_mode(self, level):
        """每关布局和规定步数"""
        self.level = level
        if self.reset_mode:                 # 如果需要重新布局
            self.num_sign = True
            if level == 1:
                self.__init__(7, 7)
                self.animal[7][9] = self.animal[7][10] = self.animal[7][11] = self.animal[8][10] = self.animal[11][7] = \
                    self.animal[11][13] = self.animal[12][7] = self.animal[12][8] = self.animal[12][12] = self.animal[12][13] = \
                    self.animal[13][7] = self.animal[13][8] = self.animal[13][9] = self.animal[13][11] = self.animal[13][12] = \
                    self.animal[13][13] = -1
                self.init_step = 17            # 规定17步
            elif level == 2:
                self.__init__(4, 8)
                self.init_step = 16          # 规定16步
            elif level == 3:
                self.__init__(7, 7)
                self.init_step = 18      # 规定18步
            elif level == 4:
                self.__init__(9, 7)
                row, col = self.row, self.col
                self.animal[row][col] = self.animal[row][col+7] = self.animal[row][col+8] = self.animal[row+1][col+8] = \
                    self.animal[row+5][col] = self.animal[row+6][col] = self.animal[row+6][col+1] = self.animal[row+6][col+8] = -1
                self.init_step = 20
            elif level == 5:
                self.__init__(8, 9)
                row, col = self.row, self.col
                self.animal[row][col+7] = self.animal[row+2][col] = self.animal[row+5][col] = self.animal[row+3][col+7] = \
                    self.animal[row+6][col+7] = self.animal[row+8][col] = -1
                self.init_step = 20
            elif level == 6:
                self.__init__(9, 9)
                row, col = self.row, self.col
                self.animal[row][col] = self.animal[row][col+8] = self.animal[row+2][col+4] = self.animal[row+3][col+2] = \
                    self.animal[row+3][col+6] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+6):
                    for j in range(col+3, col+6):
                        self.animal[i][j] = -1
                self.init_step = 28
            elif level == 7:
                self.__init__(9, 9)
                row, col = self.row, self.col
                for i in range(row, row+9):
                    self.animal[i][col+4] = -1
                for j in range(col, col+4):
                    self.animal[row+3][j] = -1
                for j in range(col+5, col+9):
                    self.animal[row+5][j] = -1
                self.init_step = 25
            elif level == 8:
                self.__init__(7, 8)
                row, col = self.row, self.col
                for i in range(row+2, row+5):
                    for j in range(col+1, col+6):
                        self.ice_list[i][j] = 1
                self.init_step = 21
            elif level == 9:
                self.__init__(9, 9)
                row, col = self.row, self.col
                self.animal[row][col+4] = self.animal[row+4][col] = self.animal[row+4][col+8] = self.animal[row+8][col+4] = -1
                for i in range(row+1, row+8):
                    for j in range(col+1, col+8):
                        self.ice_list[i][j] = 1
                self.init_step = 35
            else:
                self.__init__(9, 9)
                row, col = self.row, self.col
                for i in range(row, row+2):
                    for j in range(col, col+9):
                        self.animal[i][j] = -1
                self.animal[row][col+4] = random.randint(0, 5)
                self.animal[row+1][col+2] = random.randint(0, 5)
                self.animal[row+1][col+4] = random.randint(0, 5)
                self.animal[row+1][col+6] = random.randint(0, 5)
                self.animal[row+2][col+1] = self.animal[row+3][col+1] = self.animal[row+2][col+3] = self.animal[row+3][col+3] =\
                    self.animal[row+2][col+5] = self.animal[row+3][col+5] = self.animal[row+2][col+7] = \
                    self.animal[row+3][col+7] = self.animal[row+8][col] = self.animal[row+8][col+8] = -1
                for i in range(row+4, row+8):
                    for j in range(col, col+9):
                        self.ice_list[i][j] = 1
                self.ice_list[row+2][col+4] = self.ice_list[row+3][col+2] = self.ice_list[row+3][col+4] = \
                    self.ice_list[row+3][col+6] = 1
                self.init_step = 40
            self.type = 0
            self.energy_num -= 5
            self.success_board = Board(Board.success_board, [200, 0])  # 过关成功板
            self.fail_board = Board(Board.fail_board, [200, 0])  # 任务失败板
            self.step = self.init_step
            self.score = 0
            self.animal_num = [0, 0, 0, 0, 0, 0]
            self.ice_num = 0
            self.reset_mode = False

    # def draw_task(self):
    #     board_center_position = (400, 90)
    #     animal_center_position = (430, 35)
    #     txt_center_position = (460, 60)
    #     txt_size = 30
    #     color = (0, 0, 0)
    #     if self.level == 1:
    #         Board(Board.task_board, board_center_position).draw(self.screen)
    #         task_animal = Element(Element.animal[4], animal_center_position)
    #         task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
    #         task_animal.draw(self.screen)
    #         self.load_text(str(10-self.animal_num[4]), txt_center_position, txt_size, color)
    #     if self.level == 2:
    #         Board(Board.task_board, board_center_position).draw(self.screen)
    #         task_animal = Element(Element.animal[1], animal_center_position)
    #         task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
    #         task_animal.draw(self.screen)
    #         self.load_text(str(21-self.animal_num[1]), txt_center_position, txt_size, color)
    #     if self.level == 3:
    #         Board(Board.task_board, (board_center_position[0]-100, board_center_position[1])).draw(self.screen)
    #         Board(Board.task_board, (board_center_position[0]+100, board_center_position[1])).draw(self.screen)
    #         task_animal = Element(Element.animal[4], (430, 35))
    #         task_animal.image = pygame.transform.smoothscale(task_animal.image, (40, 40))
    #         task_animal.draw(self.screen)
    #         self.load_text(str(10 - self.animal_num[1]), (460, 60), 30)

    def num_add(self):
        if self.num_sign:
            self.money += self.score * 2
            if self.score < self.min:
                self.energy_num += 1
            elif self.score < self.max:
                self.energy_num += 2
            else:
                self.energy_num += 5
            self.num_sign = False

    def judge_level(self):
        """每关任务判断过关"""
        if self.step <= 0:
            self.type = -1  # 失败
        if self.level == 1:
            if self.animal_num[4] >= 10:  # 第一关任务消除2个青蛙
                self.type = 1             # 过关
                self.num_add()
        elif self.level == 2:
            if self.animal_num[1] >= 21:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()
        elif self.level == 3:
            if self.animal_num[4] >= 16 and self.animal_num[5] >= 16:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()
        elif self.level == 4:
            if self.animal_num[5] >= 18 and self.animal_num[2] >= 18:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 5:
            if self.animal_num[2] >= 28 and self.animal_num[0] >= 28:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 6:
            if self.animal_num[4] >= 70:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 7:
            if self.animal_num[2] >= 36 and self.animal_num[1] >= 36 and self.animal_num[0] >= 36:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 8:
            if self.ice_num >= 15:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        elif self.level == 9:
            if self.ice_num >= 49:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        else:
            if self.ice_num >= 39:  # 第二关任务21个熊
                self.type = 1                         # 过关
                self.num_add()

        self.judgeNext(self.type, self.score)


