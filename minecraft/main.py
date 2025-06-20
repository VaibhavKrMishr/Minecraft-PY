from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from pathlib import Path
import random
import math

app = Ursina()
window.title = "Voxel Builder"
window.borderless = False
window.color = color.rgb(135, 206, 235)

# ===== Constants ===== #
WORLD_WIDTH = 60
WORLD_DEPTH = 60
MAX_HEIGHT = 20
BLOCK_PATH = Path('assets/images')
BLOCK_KEYS = {1: 'grass.png', 2: 'stone.png', 3: 'soil.png'}
boxes = {}
selected_block = 1

# ===== Load Textures ===== #
block_textures = {
    k: load_texture(str(BLOCK_PATH / v)) for k, v in BLOCK_KEYS.items()
}

# ===== Environment ===== #
Sky(texture=load_texture('sky_sunset'))

# ===== Player ===== #
player = FirstPersonController()
player.gravity = 0.5
player.jump_height = 1.5
player.cursor.visible = True

# ===== Voxel Block ===== #
class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=block_textures[2]):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0,
            texture=texture,
            color=color.white,
            scale=1
        )
        boxes[tuple(position)] = self

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                new_pos = self.position + mouse.normal
                if tuple(new_pos) not in boxes:
                    Voxel(position=new_pos, texture=block_textures[selected_block])
            elif key == 'right mouse down':
                pos = tuple(self.position)
                destroy(self)
                boxes.pop(pos, None)

# ===== Terrain Generation ===== #
def generate_terrain():
    for x in range(WORLD_WIDTH):
        for z in range(WORLD_DEPTH):
            height = int(2 + random.uniform(-1, 1) + 3 * (math.sin(x * 0.1) + math.cos(z * 0.1)))
            for y in range(height):
                pos = (x, y, z)
                texture = block_textures[1] if y == height - 1 else block_textures[3]
                Voxel(position=pos, texture=texture)

# ===== Input Handling ===== #
def input(key):
    global selected_block
    if key in map(str, BLOCK_KEYS.keys()):
        selected_block = int(key)
        hotbar_highlight.x = -0.33 + (selected_block - 1) * 0.33

# ===== Hotbar UI ===== #
hotbar = Entity(parent=camera.ui, y=-0.45, scale=(1, 0.1), model='quad', color=color.black66)

for i, texture in block_textures.items():
    Entity(
        parent=camera.ui,
        model='quad',
        texture=texture,
        x=-0.33 + (i - 1) * 0.33,
        y=-0.45,
        scale=0.09
    )

hotbar_highlight = Entity(
    parent=camera.ui,
    model='quad',
    scale=0.1,
    color=color.azure,
    y=-0.45,
    x=-0.33,
    z=-1
)

generate_terrain()
app.run()
