import pygame
import sys
from collections import deque

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GREEN  = (80,  200, 100)
YELLOW = (255, 220, 60)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)

NODES = {
    'A': (200, 180),
    'B': (370, 130),
    'C': (540, 180),
    'D': (290, 310),
    'E': (450, 310),
    'F': (370, 440),
}

EDGES = [
    ('A', 'B'), ('A', 'D'),
    ('B', 'C'), ('B', 'E'),
    ('C', 'E'),
    ('D', 'E'), ('D', 'F'),
    ('E', 'F'),
]

def build_adj():
    adj = {n: [] for n in NODES}
    for u, v in EDGES:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def bfs_order(adj, start):
    visited = []
    seen    = set()
    queue   = deque([start])
    seen.add(start)
    while queue:
        node = queue.popleft()
        visited.append(node)
        for nb in sorted(adj[node]):
            if nb not in seen:
                seen.add(nb)
                queue.append(nb)
    return visited


def dfs_order(adj, start):
    visited = []
    seen    = set()
    stack   = [start]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        visited.append(node)
        for nb in sorted(adj[node], reverse=True):
            if nb not in seen:
                stack.append(nb)
    return visited


def draw_button(screen, font, text, x, y, w=120, h=38):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def _wait_next_graph(screen, clock, font, label="Next →"):
    btn = pygame.Rect(630, 548, 160, 36)
    while True:
        pygame.draw.rect(screen, (180,230,180), btn, border_radius=6)
        pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
        screen.blit(font.render(label,True,BLACK), font.render(label,True,BLACK).get_rect(center=btn.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return False
            if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos): return True
        clock.tick(30)


def _draw_graph_state(screen, font, small, visited, current=None, start=None, title="", desc=""):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render(title, True, WHITE), (12,10))
    screen.blit(small.render(desc, True, DKGRAY), (12,56))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    for u,v in EDGES:
        pygame.draw.line(screen, DKGRAY, NODES[u], NODES[v], 2)
    for name,(x,y) in NODES.items():
        if name == current:       col = YELLOW
        elif name in visited:     col = GREEN
        elif name == start:       col = BLUE
        else:                     col = (100,149,237)
        pygame.draw.circle(screen, col, (x,y), 28)
        pygame.draw.circle(screen, BLACK, (x,y), 28, 2)
        screen.blit(font.render(name,True,BLACK), font.render(name,True,BLACK).get_rect(center=(x,y)))


def run_graph_test(screen, clock, font, small):
    adj = build_adj()

    tests = [
        ("BFS", "BFS from A: visit all nodes in level order. Expected: A first, all 6 visited.", "A"),
        ("DFS", "DFS from C: depth-first traversal. Expected: C first, all 6 visited.", "C"),
        ("BFS_restart", "BFS restart from B: should start at B, visit all nodes.", "B"),
    ]

    for algo, desc, start in tests:
        if algo == "BFS" or algo == "BFS_restart":
            order = bfs_order(adj, start)
            algo_label = "BFS"
        else:
            order = dfs_order(adj, start)
            algo_label = "DFS"

        title = f"Test: {algo_label} from '{start}'"
        visited_so_far = []

        for node in order:
            visited_so_far.append(node)
            _draw_graph_state(screen, font, small, visited_so_far, current=node, start=start,
                              title=title, desc=desc)
            screen.blit(small.render(f"Order so far: {' → '.join(visited_so_far)}", True, DKGRAY), (12,82))
            pygame.display.flip()
            pygame.time.delay(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        _draw_graph_state(screen, font, small, visited_so_far, start=start, title=title, desc=desc)
        screen.blit(small.render(f"Final order: {' → '.join(order)}", True, DKGRAY), (12,82))
        passed = set(order)=={'A','B','C','D','E','F'} and order[0]==start
        col = (60,200,100) if passed else (220,60,60)
        pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
        screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                    font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))
        if not _wait_next_graph(screen, clock, font): return


def run_graph(screen, clock, font, small):
    adj          = build_adj()
    visited      = []
    order        = []
    show_index   = 0
    start_node   = 'A'
    algo         = "BFS"
    message      = "Click a node to set start, then press Run."
    timer        = 0

    while True:
        screen.fill(WHITE)

        title = font.render(f"Graph Traversal - {algo}", True, BLUE)
        screen.blit(title, (20, 15))

        btn_bfs  = draw_button(screen, small, "BFS",      20,  60, w=80)
        btn_dfs  = draw_button(screen, small, "DFS",     110,  60, w=80)
        btn_run  = draw_button(screen, small, "Run",     210,  60, w=80)
        btn_reset= draw_button(screen, small, "Reset",   300,  60, w=90)
        btn_back = draw_button(screen, small, "< Menu",  500,  60, w=100)
        btn_test = draw_button(screen, small, "Test",    610,  60, w=70)

        for u, v in EDGES:
            pygame.draw.line(screen, DKGRAY, NODES[u], NODES[v], 2)

        for name, (x, y) in NODES.items():
            if name in visited:
                color = GREEN
            elif name == start_node:
                color = YELLOW
            else:
                color = BLUE
            pygame.draw.circle(screen, color,  (x, y), 28)
            pygame.draw.circle(screen, BLACK,  (x, y), 28, 2)
            lbl = font.render(name, True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=(x, y)))

        if order:
            order_str = " → ".join(order[:show_index])
            olbl = small.render(f"Order: {order_str}", True, DKGRAY)
            screen.blit(olbl, (20, 510))

        msg = small.render(message, True, DKGRAY)
        screen.blit(msg, (20, 560))

        pygame.display.flip()

        if show_index < len(order):
            timer += 1
            if timer >= 30:
                timer = 0
                visited.append(order[show_index])
                show_index += 1
                if show_index == len(order):
                    message = f"{algo} complete! Visited: {' → '.join(order)}"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return
                elif btn_test.collidepoint(event.pos):
                    run_graph_test(screen, clock, font, small)
                elif btn_bfs.collidepoint(event.pos):
                    algo = "BFS"; message = "BFS selected."
                elif btn_dfs.collidepoint(event.pos):
                    algo = "DFS"; message = "DFS selected."
                elif btn_run.collidepoint(event.pos):
                    if algo == "BFS":
                        order = bfs_order(adj, start_node)
                    else:
                        order = dfs_order(adj, start_node)
                    visited    = []
                    show_index = 0
                    timer      = 0
                    message    = f"Running {algo} from {start_node}..."
                elif btn_reset.collidepoint(event.pos):
                    visited = []; order = []; show_index = 0
                    message = "Reset. Click a node to pick start."
                else:
                    for name, (nx, ny) in NODES.items():
                        dx, dy = event.pos[0]-nx, event.pos[1]-ny
                        if dx*dx + dy*dy <= 28*28:
                            start_node = name
                            visited = []; order = []; show_index = 0
                            message = f"Start set to '{name}'. Press Run."

        clock.tick(30)
