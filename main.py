import pygame
import numpy as np
import random
import math
from constants import *
from cube import *

# --- Sticker and 3D Rendering Class ---
class Sticker:
    def __init__(self, face_idx, r, c, size):
        self.face_idx, self.r, self.c = face_idx, r, c
        
        # --- ENHANCEMENT: Increased border for a more solid, realistic look ---
        self.sticker_size = size * 0.88 
        
        coord_map, dist = [-1, 0, 1], 1.5
        if   face_idx == U: self.center=np.array([coord_map[c],dist,-coord_map[r]]); self.normal=np.array([0,1,0])
        elif face_idx == D: self.center=np.array([coord_map[c],-dist,coord_map[r]]); self.normal=np.array([0,-1,0])
        elif face_idx == R: self.center=np.array([dist,-coord_map[r],coord_map[c]]); self.normal=np.array([1,0,0])
        elif face_idx == L: self.center=np.array([-dist,-coord_map[r],-coord_map[c]]); self.normal=np.array([-1,0,0])
        elif face_idx == F: self.center=np.array([coord_map[c],-coord_map[r],dist]); self.normal=np.array([0,0,1])
        elif face_idx == B: self.center=np.array([-coord_map[c],-coord_map[r],-dist]); self.normal=np.array([0,0,-1])
        
        self.center_orig = self.center * size
        self.base_points_orig = self.get_corners(self.center_orig, size)
        self.sticker_points_orig = self.get_corners(self.center_orig, self.sticker_size)
        self.normal_orig = self.normal.copy()

    def get_corners(self, center, size):
        corners, d = [], size / 2
        if self.face_idx in [U,D]: u,v = np.array([d,0,0]), np.array([0,0,d])
        elif self.face_idx in [R,L]: u,v = np.array([0,0,d]), np.array([0,d,0])
        else: u,v = np.array([d,0,0]), np.array([0,d,0])
        corners.extend([center-u+v, center+u+v, center+u-v, center-u-v])
        return corners

    def draw(self, screen, cube_state, rot_matrix, light_vec, cube_center, anim_matrix=None):
        base_points = [anim_matrix @ p for p in self.base_points_orig] if anim_matrix is not None else self.base_points_orig
        sticker_points = [anim_matrix @ p for p in self.sticker_points_orig] if anim_matrix is not None else self.sticker_points_orig
        normal = anim_matrix @ self.normal_orig if anim_matrix is not None else self.normal_orig

        projected_base_points = [((rot_matrix @ p)[0] + cube_center[0], (rot_matrix @ p)[1] + cube_center[1]) for p in base_points]
        pygame.draw.polygon(screen, C_BG, projected_base_points)

        self.color = COLORS[cube_state[self.face_idx, self.r, self.c]]
        rotated_normal = rot_matrix @ normal
        lum = max(0.3, min(1, 0.7 + 0.3 * np.dot(rotated_normal, light_vec)))
        view_vec = np.array([0, 0, -1])
        reflect_vec = 2 * np.dot(rotated_normal, light_vec) * rotated_normal - light_vec
        specular = max(0, np.dot(view_vec, -reflect_vec)) ** 16
        shaded_color = tuple(min(255, c * lum + specular * 100) for c in self.color)
        projected_sticker_points = [((rot_matrix @ p)[0] + cube_center[0], (rot_matrix @ p)[1] + cube_center[1]) for p in sticker_points]
        pygame.draw.polygon(screen, shaded_color, projected_sticker_points)


# --- Main Application Class ---
class CubeGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("3D Rubik's Cube Simulator")
        self.font_sm = pygame.font.SysFont("Segoe UI", 18)
        self.font_md = pygame.font.SysFont("Segoe UI", 22, bold=True)
        self.font_lg = pygame.font.SysFont("Segoe UI", 32, bold=True)
        self.font_moves = pygame.font.SysFont("Roboto Mono", 24, bold=True)
        self.clock = pygame.time.Clock()
        self.cube_state = create_solved_cube()
        self.stickers = [Sticker(f, r, c, 70) for f in range(6) for r in range(3) for c in range(3)]
        self.angle_x, self.angle_y = math.radians(25), math.radians(-35)
        self.light = np.array([-0.6, -1, -0.3]) / np.linalg.norm(np.array([-0.6, -1, -0.3]))
        self.scramble_history = []
        
        self.anim_queue = []
        self.current_anim = None
        self.anim_angle = 0
        self.solve_speeds = {"Slow": 4, "Normal": 8, "Fast": 16}
        self.solve_speed = "Normal"
        
        self.display_moves = []
        self.moves_title = "Welcome!"
        self.current_move_index = -1
        self.buttons = {}
        self.create_controls()

    def create_controls(self):
        panel_x = 920
        # --- REFINED LAYOUT & SPACING ---
        self.buttons["Scramble"] = {"rect": pygame.Rect(panel_x, 620, 280, 50), "icon": "⟳"}
        self.buttons["Solve"] = {"rect": pygame.Rect(panel_x, 680, 280, 50), "icon": "▶"}
        self.buttons["Reset"] = {"rect": pygame.Rect(panel_x, 740, 280, 50), "icon": "⌫"}
        
        moves = ['U','D','L','R','F','B']
        for i, move in enumerate(moves):
            self.buttons[move] = {"rect": pygame.Rect(panel_x, 100 + i * 65, 85, 45)}
            self.buttons[move + "'"] = {"rect": pygame.Rect(panel_x + 95, 100 + i * 65, 85, 45)}
            
        self.buttons["Slow"] = {"rect": pygame.Rect(panel_x, 525, 85, 45)}
        self.buttons["Normal"] = {"rect": pygame.Rect(panel_x + 95, 525, 90, 45)}
        self.buttons["Fast"] = {"rect": pygame.Rect(panel_x + 195, 525, 85, 45)}

    def draw_panel(self, rect, title, title_font, title_color):
        pygame.draw.rect(self.screen, C_PANEL, rect, border_radius=15)
        pygame.draw.rect(self.screen, C_BORDER, rect, 2, border_radius=15)
        title_surf = title_font.render(title, True, title_color)
        self.screen.blit(title_surf, (rect.x + 25, rect.y + 15))

    def draw_moves_panel(self):
        panel_rect = pygame.Rect(25, 25, 400, WINDOW_SIZE[1] - 50)
        self.draw_panel(panel_rect, self.moves_title, self.font_lg, C_TEXT)
        
        y = 110
        x_start = panel_rect.x + 30
        x = x_start
        line_spacing = 10
        font_height = self.font_moves.get_height()

        for i, move in enumerate(self.display_moves):
            is_current_move = (i == self.current_move_index)
            word_surf = self.font_moves.render(move, True, C_ACCENT_TEXT if is_current_move else C_TEXT_DARK)
            word_width, word_height = word_surf.get_size()
            
            if x + word_width + 15 > panel_rect.right:
                x = x_start
                y += font_height + line_spacing

            if is_current_move:
                pygame.draw.rect(self.screen, C_ACCENT, (x, y, word_width + 10, font_height), border_radius=5)
            
            self.screen.blit(word_surf, (x + 5, y))
            x += word_width + 20


    def draw_button(self, text, data, base_color, hover_color, text_color, is_active=False, is_disabled=False):
        rect = data["rect"]
        mouse_pos = pygame.mouse.get_pos()
        color = base_color
        
        if is_disabled: color = C_BORDER; text_color = C_TEXT_DARK
        elif is_active: color = C_ACCENT; text_color = C_ACCENT_TEXT
        elif rect.collidepoint(mouse_pos): color = hover_color
        
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        
        icon = data.get("icon")
        if icon: text = f"{icon}  {text}"
        
        text_surf = self.font_md.render(text, True, text_color)
        self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(C_BG)
        self.draw_moves_panel()
        
        # --- REVISED PANEL LAYOUT AND SIZES ---
        self.draw_panel(pygame.Rect(890, 25, 360, 455), "Manual Control", self.font_lg, C_TEXT)
        self.draw_panel(pygame.Rect(890, 490, 360, 95), "Solve Speed", self.font_md, C_TEXT)
        self.draw_panel(pygame.Rect(890, 595, 360, 195), "Actions", self.font_md, C_TEXT)

        for label, data in self.buttons.items():
            is_disabled = (label == "Solve" and (not self.scramble_history or self.current_anim is not None))
            is_active = (label == self.solve_speed)
            base, hover = (C_BTN, C_BTN_HOVER)
            text_c = C_TEXT
            self.draw_button(label, data, base, hover, text_c, is_active, is_disabled)

        anim_matrices = {}
        if self.current_anim:
            move, direction = self.current_anim
            progress = min(1.0, self.anim_angle / (math.pi / 2))
            eased_progress = 0.5 * (1 - math.cos(progress * math.pi))
            render_angle = eased_progress * (math.pi / 2)
            angle = render_angle * direction
            c, s = math.cos(angle), math.sin(angle)
            
            axis_map = {'U':(1,1), 'D':(1,-1), 'R':(0,1), 'L':(0,-1), 'F':(2,1), 'B':(2,-1)}
            axis, layer_dir = axis_map[move]
            
            if axis == 0: rot = np.array([[1,0,0], [0,c,-s], [0,s,c]])
            elif axis == 1: rot = np.array([[c,0,s], [0,1,0], [-s,0,c]])
            else: rot = np.array([[c,-s,0], [s,c,0], [0,0,1]])
            
            for sticker in self.stickers:
                sticker_axis_val = sticker.center_orig[axis]
                if abs(sticker_axis_val - 70 * 1.5 * layer_dir) < 1:
                   anim_matrices[(sticker.face_idx, sticker.r, sticker.c)] = rot

        rx = np.array([[1,0,0],[0,math.cos(self.angle_x),-math.sin(self.angle_x)],[0,math.sin(self.angle_x),math.cos(self.angle_x)]])
        ry = np.array([[math.cos(self.angle_y),0,math.sin(self.angle_y)],[0,1,0],[-math.sin(self.angle_y),0,math.cos(self.angle_y)]])
        rot_matrix = ry @ rx
        
        self.stickers.sort(key=lambda s: (rot_matrix @ (anim_matrices.get((s.face_idx, s.r, s.c), np.identity(3)) @ s.center_orig))[2])
        cube_center = (640, WINDOW_SIZE[1]/2)
        for sticker in self.stickers:
            anim_mat = anim_matrices.get((sticker.face_idx, sticker.r, sticker.c))
            sticker.draw(self.screen, self.cube_state, rot_matrix, self.light, cube_center, anim_mat)

        pygame.display.flip()

    def run(self):
        dragging_cube = False
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    clicked_on_button = False
                    for label, data in self.buttons.items():
                        if data["rect"].collidepoint(mouse_pos):
                            clicked_on_button = True
                            if self.current_anim: continue
                            
                            if label in self.solve_speeds: self.solve_speed = label
                            elif label == "Reset":
                                self.cube_state = create_solved_cube(); self.scramble_history = []; self.display_moves = []; self.moves_title = "Welcome!"; self.current_move_index = -1
                            elif label == "Scramble":
                                new_scramble = random.choices(['U','D','L','R','F','B',"U'","D'","L'","R'","F'","B'"], k=25)
                                self.scramble_history.extend(new_scramble)
                                self.anim_queue.extend([(m[0], -1 if "'" in m else 1) for m in new_scramble])
                                self.display_moves = self.scramble_history.copy(); self.moves_title = "Scramble"; self.current_move_index = 0
                            elif label == "Solve" and self.scramble_history:
                                solution = [get_inverse_move(m) for m in reversed(self.scramble_history)]
                                self.anim_queue.extend([(m[0], -1 if "'" in m else 1) for m in solution])
                                self.scramble_history = []
                                self.display_moves = solution; self.moves_title = "Solution Steps"; self.current_move_index = 0
                            elif "icon" not in data: # It's a move button
                                self.anim_queue.append((label[0], -1 if "'" in label else 1))
                                self.display_moves = [label]; self.moves_title = "Manual Move"; self.current_move_index = 0
                            break
                    if not clicked_on_button and mouse_pos[0] > 430 and mouse_pos[0] < 880:
                        dragging_cube = True

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1: dragging_cube = False
                elif event.type == pygame.MOUSEMOTION and dragging_cube:
                    dx, dy = event.rel
                    self.angle_y += dx * 0.01; self.angle_x -= dy * 0.01

            if not self.current_anim and self.anim_queue:
                self.current_anim = self.anim_queue.pop(0)
                self.anim_angle = 0
            
            if self.current_anim:
                self.anim_angle += math.radians(self.solve_speeds[self.solve_speed])
                if self.anim_angle >= math.pi / 2:
                    move, direction = self.current_anim
                    full_move = move if direction == 1 else move + "'"
                    self.cube_state = apply_move(self.cube_state, full_move)
                    self.current_anim = None
                    if self.anim_queue:
                        self.current_move_index += 1
                    else:
                        if self.moves_title == "Solving...": self.moves_title = "Solved!"
                        elif self.moves_title == "Scramble": self.moves_title = "Scrambled"
                        self.current_move_index = -1

            self.draw()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    app = CubeGUI()
    app.run()
