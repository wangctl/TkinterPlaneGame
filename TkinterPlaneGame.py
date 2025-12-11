from tkinter import *
from PIL import Image, ImageTk
import random

class PlaneGame:
    def __init__(self):
        self.root = Tk()
        self.root.title("Ares Plane")
        self.canvas_width = 420
        self.canvas_height = 640
        self.bullet_speed = 6
        self.auto_shoot_interval = 500

        self.enemy_bullet_speed = self.bullet_speed / 4
        self.enemy_shoot_interval = self.auto_shoot_interval * 4

        self.canvas = Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg='black')
        self.canvas.pack()
        bg = Image.open("image/bg2.png")
        bg = bg.resize((self.canvas_width, self.canvas_height))
        self.img_bg = ImageTk.PhotoImage(bg)
        self.canvas.create_image(0, 0, anchor=NW, image=self.img_bg)
        self.Ares_size = 30
        self.Ares_x = self.canvas_width // 2
        self.Ares_y = self.canvas_height - 60
        self.Ares_speed = 5
        self.enem_size = 20
        self.enemy_move_speed = 1

        ares_img = Image.open("image/AresPlane.png")
        ares_img = ares_img.resize((100, 100))
        self.img_Ares_body = ImageTk.PhotoImage(ares_img)

        self.Ares_body = self.canvas.create_image(self.Ares_x, self.Ares_y, image=self.img_Ares_body, tags="Ares_body")

        self.enemy_images = []
        for i in range(1, 5):
            img = Image.open("image/emey{}.png".format(i))  # 使用 format 插入变量
            img = img.resize((70, 70))
            self.enemy_images.append(ImageTk.PhotoImage(img))
        boss_img = Image.open("image/BOSS.png")
        boss_img = boss_img.resize((300, 300))
        self.img_boss = ImageTk.PhotoImage(boss_img)

        bullet_img = Image.open("image/fire1.png")
        bullet_img = bullet_img.resize((20, 50))
        self.img_bullet = ImageTk.PhotoImage(bullet_img)

        enemy_bullet_img = Image.open("image/emeyFire.png")
        enemy_bullet_img = enemy_bullet_img.resize((20, 40))
        self.img_enemy_bullet = ImageTk.PhotoImage(enemy_bullet_img)

        self.level = 1
        self.enemy_count = 5
        self.boss_hp = 10
        self.enemies = []
        self.enemy_texts = []
        self.bullets = []
        self.enemy_bullets = []
        self.game_running = True
        self.enemy_directions = []
        self.enemy_change_direction_interval = 1000
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<space>", self.shoot)
        self.canvas.bind("<Motion>", self.mouse_move)
        self.canvas.after(30, self.game_loop)
        self.canvas.after(self.enemy_change_direction_interval, self.change_enemy_directions)
        self.auto_shoot()
        self.start_enemy_shooting()

        self.player_hp = 10
        self.player_max_hp = 10
        self.player_hp_bar = self.canvas.create_rectangle(
            0, 10, self.canvas_width, 30, fill="yellow", outline="white", tags="player_hp_bar"
        )
        self.canvas.create_text(220, 20, text="玩家血量", fill="white", font=("Arial", 12), tags="player_hp_text")

    def auto_shoot(self):
        self.shoot(None)
        if self.game_running:
            self.root.after(self.auto_shoot_interval, self.auto_shoot)

    def create_enemy(self):
        if self.level == 1:
            for _ in range(self.enemy_count):
                x = random.randint(self.enem_size, self.canvas_width - self.enem_size)
                y = random.randint(50, 150)
                enemy_img = random.choice(self.enemy_images)
                enemy = self.canvas.create_image(x, y, image=enemy_img, tags="enemy")
                hp = 2
                hp_bar = self.canvas.create_rectangle(
                    x - 25, y - 40, x + 25, y - 35, fill="green", tags="enemy_hp_bar"
                )
                self.enemies.append({'id': enemy, 'x': x, 'y': y, 'hp': hp, 'hp_bar': hp_bar})
                self.enemy_directions.append({'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1])})
        elif self.level == 2:
            x = self.canvas_width // 2
            y = 100
            boss = self.canvas.create_image(x, y, image=self.img_boss, tags="boss")
            hp = 50
            self.boss_hp_bar = self.canvas.create_rectangle(
                x - 150, y + 160, x + 150, y + 170, fill="red", outline="white", tags="boss_hp_bar"
            )
            self.enemies = [{'id': boss, 'x': x, 'y': y, 'hp': hp, 'hp_bar': self.boss_hp_bar}]
            self.enemy_directions = [{'dx': random.choice([-1, 1]), 'dy': random.choice([-1, 1])}]

    def change_enemy_directions(self):
        for direction in self.enemy_directions:
            direction['dx'] = random.choice([-1, 0, 1])
            direction['dy'] = random.choice([-1, 0, 1])
        if self.game_running:
            self.canvas.after(self.enemy_change_direction_interval, self.change_enemy_directions)

    def move_left(self, event):
        self.Ares_x -= self.Ares_speed
        self.canvas.move(self.Ares_body, -self.Ares_speed, 0)
        if self.Ares_x < 0:
            self.Ares_x = 0

    def move_right(self, event):
        self.Ares_x += self.Ares_speed
        self.canvas.move(self.Ares_body, self.Ares_speed, 0)
        if self.Ares_x > self.canvas_width:
            self.Ares_x = self.canvas_width

    def shoot(self, event):
        bullet = self.canvas.create_image(self.Ares_x, self.Ares_y-40, image=self.img_bullet, tags="bullet")
        self.bullets.append({'id': bullet, 'x': self.Ares_x, 'y': self.Ares_y-40})

    def mouse_move(self, event):
        x = max(self.Ares_size, min(event.x, self.canvas_width - self.Ares_size))
        y = max(self.Ares_size, min(event.y, self.canvas_height - self.Ares_size))
        self.canvas.coords(self.Ares_body, x, y)
        self.Ares_x = x
        self.Ares_y = y

    def start_enemy_shooting(self):
        for enemy in self.enemies:
            if self.game_running:
                bullet = self.canvas.create_image(
                    enemy['x'], enemy['y'] + 20, image=self.img_enemy_bullet, tags="enemy_bullet"
                )
                self.enemy_bullets.append({'id': bullet, 'x': enemy['x'], 'y': enemy['y'] + 20})
        if self.game_running:
            self.root.after(self.enemy_shoot_interval, self.start_enemy_shooting)

    def game_loop(self):
        if not self.enemies:
            self.create_enemy()
        for bullet in self.bullets[:]:
            self.canvas.move(bullet['id'], 0, -self.bullet_speed)
            bullet['y'] -= self.bullet_speed
            for idx, enemy in enumerate(self.enemies):
                ex, ey = enemy['x'], enemy['y']
                if self.level == 2:
                    collision_radius = 75
                else:
                    collision_radius = 17.5

                distance_squared = (bullet['x'] - ex) ** 2 + (bullet['y'] - ey) ** 2
                if distance_squared < collision_radius ** 2:
                    enemy['hp'] -= 1
                    if self.level == 2:
                        hp_ratio = enemy['hp'] / 50
                        self.canvas.coords(self.boss_hp_bar, ex - 150, ey + 160, ex - 150 + 300 * hp_ratio, ey + 170)
                    else:
                        hp_bar = enemy['hp_bar']
                        hp_ratio = enemy['hp'] / 2
                        self.canvas.coords(hp_bar, ex - 25, ey - 40, ex - 25 + 50 * hp_ratio, ey - 35)
                    if enemy['hp'] <= 0:
                        self.canvas.delete(enemy['id'])
                        if self.level == 2:
                            self.canvas.delete(self.boss_hp_bar)
                        else:
                            self.canvas.delete(hp_bar)
                        self.enemies.pop(idx)
                        self.enemy_directions.pop(idx)
                    self.canvas.delete(bullet['id'])
                    self.bullets.remove(bullet)
                    break
            if bullet['y'] < 0:
                self.canvas.delete(bullet['id'])
                self.bullets.remove(bullet)

        for idx, enemy in enumerate(self.enemies):
            direction = self.enemy_directions[idx]
            dx = direction['dx'] * self.enemy_move_speed
            dy = direction['dy'] * self.enemy_move_speed
            if enemy['x'] + dx < self.enem_size or enemy['x'] + dx > self.canvas_width - self.enem_size:
                direction['dx'] *= -1
            if enemy['y'] + dy < self.enem_size or enemy['y'] + dy > self.canvas_height // 2:
                direction['dy'] *= -1
            enemy['x'] += direction['dx'] * self.enemy_move_speed
            enemy['y'] += direction['dy'] * self.enemy_move_speed
            self.canvas.move(enemy['id'], direction['dx'] * self.enemy_move_speed, direction['dy'] * self.enemy_move_speed)
            self.canvas.move(enemy['hp_bar'], direction['dx'] * self.enemy_move_speed, direction['dy'] * self.enemy_move_speed)

        for bullet in self.enemy_bullets[:]:
            self.canvas.move(bullet['id'], 0, self.enemy_bullet_speed)
            bullet['y'] += self.enemy_bullet_speed
            if abs(bullet['x'] - self.Ares_x) < 30 and abs(bullet['y'] - self.Ares_y) < 30:
                self.player_hp -= 1
                hp_ratio = self.player_hp / self.player_max_hp
                self.canvas.coords(self.player_hp_bar, 0, 10, self.canvas_width * hp_ratio, 30)
                self.canvas.delete(bullet['id'])
                self.enemy_bullets.remove(bullet)
                if self.player_hp <= 0:
                    self.game_running = False
                    self.canvas.create_text(
                        self.canvas_width // 2, self.canvas_height // 2,
                        text="游戏失败！", fill="red", font=("Arial", 32)
                    )
                    return
            if bullet['y'] > self.canvas_height:
                self.canvas.delete(bullet['id'])
                self.enemy_bullets.remove(bullet)

        if not self.enemies:
            if self.level == 1:
                self.level = 2
                self.create_enemy()
            else:
                self.game_running = False
                self.canvas.create_text(
                    self.canvas_width // 2, self.canvas_height // 2,
                    text="胜利！", fill="white", font=("Arial", 32)
                )
                return
        if self.game_running:
            self.canvas.after(30, self.game_loop)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    game = PlaneGame()
    game.run()