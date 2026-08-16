import pygame


class Controller:
    DEADZONE = 0.5

    def __init__(self):
        pygame.init()
        pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No controller detected.")

        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

        self.stick_active = False

        print(f"Controller connected: {self.controller.get_name()}")

    def update(self, snake):
        pygame.event.pump()

        x = self.controller.get_axis(0)
        y = self.controller.get_axis(1)

        # Stick has returned to neutral
        if abs(x) < self.DEADZONE and abs(y) < self.DEADZONE:
            self.stick_active = False
            return

        # Ignore the stick until it returns to neutral
        if self.stick_active:
            return

        if abs(x) > abs(y):
            if x < -self.DEADZONE:
                snake.left()
            elif x > self.DEADZONE:
                snake.right()

        else:
            if y < -self.DEADZONE:
                snake.up()
            elif y > self.DEADZONE:
                snake.down()

        self.stick_active = True