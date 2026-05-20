import pygame
import random
import math

from utils.json_handler import JSONHandler


class World:
    def __init__(self, tileset_path=JSONHandler.path_join('data', 'tileset', 'tileset.png'),
                 water_path=JSONHandler.path_join('data', 'tileset', 'water.png'),
                 map_size=(70, 70),
                 tile_size=64):
        self.map_size = map_size
        self.tile_size = tile_size
        self.tileset_path = tileset_path
        self.water_path = water_path

        self.current_seed = None
        self.data = []

        self.tiles = self._load_tileset(tileset_path)
        self.water_img = pygame.image.load(water_path).convert_alpha()
        self.scaled_water = pygame.transform.scale(self.water_img, (self.tile_size, self.tile_size))

    def _load_tileset(self, path):
        img = pygame.image.load(path).convert_alpha()
        ts = self.tile_size
        t = {}

        t[(1, 0, 1, 0)] = img.subsurface((0, 0, ts, ts))
        t[(1, 0, 0, 0)] = img.subsurface((ts, 0, ts, ts))
        t[(1, 0, 0, 1)] = img.subsurface((ts * 2, 0, ts, ts))
        t[(0, 0, 1, 0)] = img.subsurface((0, ts, ts, ts))
        t[(0, 0, 0, 0)] = img.subsurface((ts, ts, ts, ts))
        t[(0, 0, 0, 1)] = img.subsurface((ts * 2, ts, ts, ts))
        t[(0, 1, 1, 0)] = img.subsurface((0, ts * 2, ts, ts))
        t[(0, 1, 0, 0)] = img.subsurface((ts, ts * 2, ts, ts))
        t[(0, 1, 0, 1)] = img.subsurface((ts * 2, ts * 2, ts, ts))
        t[(1, 0, 1, 1)] = img.subsurface((ts * 3, 0, ts, ts))
        t[(0, 0, 1, 1)] = img.subsurface((ts * 3, ts, ts, ts))
        t[(0, 1, 1, 1)] = img.subsurface((ts * 3, ts * 2, ts, ts))
        t[(1, 1, 1, 0)] = img.subsurface((0, ts * 3, ts, ts))
        t[(1, 1, 0, 0)] = img.subsurface((ts, ts * 3, ts, ts))
        t[(1, 1, 0, 1)] = img.subsurface((ts * 2, ts * 3, ts, ts))
        t[(1, 1, 1, 1)] = img.subsurface((ts * 3, ts * 3, ts, ts))
        return t

    def generate_new_world(self, seed=None):
        if seed is None:
            seed = random.randint(0, 9999999)
        self.current_seed = seed
        self.data = self._generate_perlin_island(seed)

        self._precalculate_tile_types()

    def _generate_perlin_island(self, seed):
        w, h = self.map_size
        rng = random.Random(seed)
        p = list(range(256))
        rng.shuffle(p)
        p += p

        grid = [[0 for _ in range(h)] for _ in range(w)]
        scale, land_mass, roundness = 25.0, 0.3, 2.2

        for x in range(w):
            for y in range(h):
                nv = self._perlin(x / scale, y / scale, p)
                dx, dy = (x - w / 2) / (w / 2), (y - h / 2) / (h / 2)
                dist = math.sqrt(dx * dx + dy * dy)
                grid[x][y] = 1 if (nv + land_mass) - (dist ** roundness) > 0 else 0
        return self._remove_small_islands(grid)

    def _remove_small_islands(self, grid):
        w, h = self.map_size
        visited = [[False for _ in range(h)] for _ in range(w)]
        cx, cy = w // 2, h // 2

        if grid[cx][cy] == 0:
            found = False
            for r in range(1, w // 2):
                for dx in range(-r, r + 1):
                    for dy in range(-r, r + 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and grid[nx][ny] == 1:
                            cx, cy, found = nx, ny, True
                            break
                    if found: break
                if found: break

        self.spawn_point = (cx, cy)

        main_island = []
        if grid[cx][cy] == 1:
            queue = [(cx, cy)]
            visited[cx][cy] = True
            while queue:
                x, y = queue.pop(0)
                main_island.append((x, y))
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not visited[nx][ny] and grid[nx][ny] == 1:
                        visited[nx][ny] = True
                        queue.append((nx, ny))

        new_grid = [[0 for _ in range(h)] for _ in range(w)]
        for x, y in main_island: new_grid[x][y] = 1
        return new_grid

    def _perlin(self, x, y, p):
        X, Y = int(x) & 255, int(y) & 255
        x -= int(x)
        y -= int(y)
        u, v = self._fade(x), self._fade(y)
        a = p[X] + Y
        aa = p[a]
        ab = p[a + 1]
        b = p[X + 1] + Y
        ba = p[b]
        bb = p[b + 1]
        return self._lerp(v, self._lerp(u, self._grad(p[aa], x, y), self._grad(p[ba], x - 1, y)),
                          self._lerp(u, self._grad(p[ab], x, y - 1), self._grad(p[bb], x - 1, y - 1)))

    def _fade(self, t):
        return t * t * t * (t * (t * 6 - 15) + 10)

    def _lerp(self, t, a, b):
        return a + t * (b - a)

    def _grad(self, h, x, y):
        h &= 3
        return (x if h < 2 else y) if h & 1 else -(x if h < 2 else y) + (
            (y if h < 2 else x) if h & 2 else -(y if h < 2 else x))

    def _precalculate_tile_types(self):
        w, h = self.map_size
        self.tile_grid = [[None for _ in range(h)] for _ in range(w)]

        for x in range(w):
            for y in range(h):
                if self.data[x][y] == 1:
                    u = 1 if y == 0 or self.data[x][y - 1] == 0 else 0
                    d = 1 if y == h - 1 or self.data[x][y + 1] == 0 else 0
                    l = 1 if x == 0 or self.data[x - 1][y] == 0 else 0
                    r = 1 if x == w - 1 or self.data[x + 1][y] == 0 else 0
                    self.tile_grid[x][y] = self.tiles.get((u, d, l, r), self.tiles[(0, 0, 0, 0)])

    def render(self, screen, cam_x=0, cam_y=0):
        ts = self.tile_size
        screen_w, screen_h = screen.get_size()

        off_x = -int(cam_x) % ts
        off_y = -int(cam_y) % ts
        if off_x > 0: off_x -= ts
        if off_y > 0: off_y -= ts

        for x in range(off_x, screen_w + ts, ts):
            for y in range(off_y, screen_h + ts, ts):
                screen.blit(self.scaled_water, (x, y))

        start_x = max(0, int(cam_x // ts))
        start_y = max(0, int(cam_y // ts))

        end_x = min(self.map_size[0], int((cam_x + screen_w) // ts) + 1)
        end_y = min(self.map_size[1], int((cam_y + screen_h) // ts) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile = self.tile_grid[x][y]
                if tile:
                    screen_pos_x = x * ts - int(cam_x)
                    screen_pos_y = y * ts - int(cam_y)
                    screen.blit(tile, (screen_pos_x, screen_pos_y))

    def get_tile_at(self, world_x, world_y):
        grid_x = int(world_x // self.tile_size)
        grid_y = int(world_y // self.tile_size)

        if 0 <= grid_x < self.map_size[0] and 0 <= grid_y < self.map_size[1]:
            return self.data[grid_x][grid_y]
        return 0