import pygame


class ThreeSliceImage:
    def __init__(self, image_path, color_index=0):
        full_image = pygame.image.load(image_path).convert_alpha()
        src_w, src_h = full_image.get_size()

        if src_h < 128:
            row_height = src_h
            y_start = 0
        else:
            row_height = 128
            color_index = color_index % 5
            y_start = color_index * row_height

            if y_start + row_height > src_h:
                row_height = src_h
                y_start = 0

        row_surface = full_image.subsurface(pygame.Rect(0, y_start, src_w, row_height))
        mask = pygame.mask.from_surface(row_surface)

        col_active = [False] * src_w
        for x in range(src_w):
            for y in range(row_height):
                if mask.get_at((x, y)):
                    col_active[x] = True
                    break

        def get_blocks(activity_list):
            blocks = []
            start = None
            for i, active in enumerate(activity_list):
                if active and start is None:
                    start = i
                elif not active and start is not None:
                    blocks.append((start, i - start))
                    start = None
            if start is not None:
                blocks.append((start, len(activity_list) - start))
            return blocks

        cols = get_blocks(col_active)

        if len(cols) == 3:
            self.cols_info = cols
        else:
            w_part = src_w // 3
            self.cols_info = [(0, w_part), (w_part, w_part), (w_part * 2, src_w - w_part * 2)]

        self.source_subsurfaces = []
        for c_start, c_len in self.cols_info:
            rect = pygame.Rect(c_start, 0, c_len, row_height)
            self.source_subsurfaces.append(row_surface.subsurface(rect))

    def generate_surface(self, width, height=128):
        src_w_left, src_w_center, src_w_right = [length for _, length in self.cols_info]

        edge_w_l = min(src_w_left, width // 2)
        edge_w_r = min(src_w_right, width // 2)

        center_width = max(0, width - edge_w_l - edge_w_r)

        left_x = 0
        center_x = edge_w_l
        right_x = width - edge_w_r

        output_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        def blit_segment(index, x, w):
            if w > 0 and height > 0:
                scaled = pygame.transform.scale(self.source_subsurfaces[index], (w, height))
                output_surface.blit(scaled, (x, 0))

        blit_segment(0, left_x, edge_w_l)
        blit_segment(1, center_x, center_width)
        blit_segment(2, right_x, edge_w_r)

        return output_surface