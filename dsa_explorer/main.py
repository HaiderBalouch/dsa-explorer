import pygame
import sys

from stack_queue_module import run_stack_queue
from linkedlist_module  import run_linkedlist
from sorting_module     import run_sorting
from bst_module         import run_bst
from graph_module       import run_graph
from heap_module        import run_heap
from puzzles_module     import run_puzzles

pygame.init()

WIDTH  = 800
HEIGHT = 600
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DSA Explorer")
clock  = pygame.time.Clock()
FONT   = pygame.font.SysFont(None, 36)
SMALL  = pygame.font.SysFont(None, 24)


def draw_text(text, x, y, color=BLACK, font=FONT):
    surf = font.render(text, True, color)
    screen.blit(surf, (x, y))


def draw_button(text, x, y, w=200, h=46):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=8)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=8)
    lbl = FONT.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("DSA Explorer", 270, 18, BLUE)
        draw_text("Pick a module:", 295, 60, DKGRAY, SMALL)

        draw_text("-- Phase 1: Data Structures --", 210, 82, DKGRAY, SMALL)
        btn_sq    = draw_button("Stack & Queue", 300, 100)
        btn_ll    = draw_button("Linked List",   300, 152)
        btn_bst   = draw_button("BST",           300, 204)

        draw_text("-- Phase 2: Algorithms --", 225, 256, DKGRAY, SMALL)
        btn_sort  = draw_button("Sorting",       300, 274)
        btn_graph = draw_button("Graph",         300, 326)
        btn_heap  = draw_button("Heap",          300, 378)

        draw_text("-- Phase 3: Puzzles --", 245, 430, DKGRAY, SMALL)
        btn_puzz  = draw_button("Puzzles",       300, 448)


        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_sq.collidepoint(event.pos):
                    run_stack_queue(screen, clock, FONT, SMALL)
                elif btn_ll.collidepoint(event.pos):
                    run_linkedlist(screen, clock, FONT, SMALL)
                elif btn_sort.collidepoint(event.pos):
                    run_sorting(screen, clock, FONT, SMALL)
                elif btn_bst.collidepoint(event.pos):
                    run_bst(screen, clock, FONT, SMALL)
                elif btn_graph.collidepoint(event.pos):
                    run_graph(screen, clock, FONT, SMALL)
                elif btn_heap.collidepoint(event.pos):
                    run_heap(screen, clock, FONT, SMALL)
                elif btn_puzz.collidepoint(event.pos):
                    run_puzzles(screen, clock, FONT, SMALL)

        clock.tick(30)


if __name__ == "__main__":
    main_menu()