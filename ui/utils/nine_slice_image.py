import pygame


class NineSliceImage:
    def __init__(self, image_path):
        full_image = pygame.image.load(image_path).convert_alpha()
        src_w, src_h = full_image.get_size()

        mask = pygame.mask.from_surface(full_image)

        col_active = [False] * src_w
        for x in range(src_w):
            for y in range(src_h):
                if mask.get_at((x, y)):
                    col_active[x] = True
                    break

        row_active = [False] * src_h
        for y in range(src_h):
            for x in range(src_w):
                if mask.get_at((x, y)):
                    row_active[y] = True
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
        rows = get_blocks(row_active)

        if len(cols) == 3 and len(rows) == 3:
            self.cols_info = cols
            self.rows_info = rows
        else:
            w_part = src_w // 3
            h_part = src_h // 3
            self.cols_info = [(0, w_part), (w_part, w_part), (w_part * 2, src_w - w_part * 2)]
            self.rows_info = [(0, h_part), (h_part, h_part), (h_part * 2, src_h - h_part * 2)]

        self.source_subsurfaces = []
        for r_start, r_len in self.rows_info:
            for c_start, c_len in self.cols_info:
                rect = pygame.Rect(c_start, r_start, c_len, r_len)
                self.source_subsurfaces.append(full_image.subsurface(rect))

    def generate_surface(self, width, height):
        src_w_left, src_w_center, src_w_right = [length for _, length in self.cols_info]
        src_h_top, src_h_mid, src_h_bottom = [length for _, length in self.rows_info]

        edge_w_l = min(src_w_left, width // 2)
        edge_w_r = min(src_w_right, width // 2)
        edge_h_t = min(src_h_top, height // 2)
        edge_h_b = min(src_h_bottom, height // 2)

        center_width = max(0, width - edge_w_l - edge_w_r)
        center_height = max(0, height - edge_h_t - edge_h_b)

        left_x = 0
        center_x = edge_w_l
        right_x = width - edge_w_r

        top_y = 0
        mid_y = edge_h_t
        bot_y = height - edge_h_b

        output_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        def blit_segment(index, x, y, w, h):
            if w > 0 and h > 0:
                scaled = pygame.transform.scale(self.source_subsurfaces[index], (w, h))
                output_surface.blit(scaled, (x, y))

        blit_segment(0, left_x, top_y, edge_w_l, edge_h_t)
        blit_segment(1, center_x, top_y, center_width, edge_h_t)
        blit_segment(2, right_x, top_y, edge_w_r, edge_h_t)

        blit_segment(3, left_x, mid_y, edge_w_l, center_height)
        blit_segment(4, center_x, mid_y, center_width, center_height)
        blit_segment(5, right_x, mid_y, edge_w_r, center_height)

        blit_segment(6, left_x, bot_y, edge_w_l, edge_h_b)
        blit_segment(7, center_x, bot_y, center_width, edge_h_b)
        blit_segment(8, right_x, bot_y, edge_w_r, edge_h_b)

        return output_surface