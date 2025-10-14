from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT

from state_machine import StateMachine
#이벤트를 체킇는 함수들을 구현
def space_down(e):
    return e[0]=='INPUT'and e[1].type==SDL_KEYDOWN and e[1].key==SDLK_SPACE


class Sleep:

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.dir = 0

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 300, 100, 100, 3.141592/2, '',self.boy.x-25, self.boy.y-25,100,100)
        else: # face_dir == -1: # left
            self.boy.image.clip_composite_draw(self.boy.frame * 100, 200, 100, 100, -3.141592/2, '',self.boy.x+25, self.boy.y-25,100,100)


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self):
        self.boy.dir = 0

    def exit(self):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 8

    def draw(self):
        if self.boy.face_dir == 1: # right
            self.boy.image.clip_draw(self.boy.frame * 100, 300, 100, 100, self.boy.x, self.boy.y)
        else: # face_dir == -1: # left
            self.boy.image.clip_draw(self.boy.frame * 100, 200, 100, 100, self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = -1
        self.dir = 0
        self.image = load_image('animation_sheet.png')

        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)#새로운 SLEEP 상태 생성
        self.state_machine = StateMachine(
            self.SLEEP,
            {
            self.SLEEP : {space_down:self.IDLE},
            self.IDLE : {}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        #들어온 외부 키 입력들을 상태머신에게 전달하기 위해 튜플화시킨 후 전단
        self.state_machine.handle_state_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()


