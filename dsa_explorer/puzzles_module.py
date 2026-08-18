import pygame
import sys
import heapq
import random

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GREEN  = (80,  200, 100)
RED    = (255, 100, 100)
YELLOW = (255, 220, 60)
ORANGE = (255, 160, 50)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)
WALL   = (60,  60,  80)
PATH   = (255, 200, 50)
VISIT  = (160, 200, 255)
PURPLE = (180, 100, 220)

TABS = ["Pathfinding", "Event Queue", "DP Grid"]

ROWS, COLS = 14, 20
CELL = 32
DP_ROWS, DP_COLS = 5, 8
DP_CELL = 70


def astar(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g = {start: 0}
    visited = set()
    visited.add(start)
    while open_set:
        _, cur = heapq.heappop(open_set)
        if cur == end:
            path = []
            node = end
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return set(path), visited
        r, c = cur
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                nb = (nr, nc)
                if nb not in visited:
                    ng = g[cur] + 1
                    if ng < g.get(nb, 99999):
                        g[nb] = ng
                        came_from[nb] = cur
                        visited.add(nb)
                        heapq.heappush(open_set, (ng + abs(nr-end[0]) + abs(nc-end[1]), nb))
    return None, visited


def dijkstra_animated(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    dist = {start: 0}
    came_from = {}
    pq = [(0, start)]
    visited = set()
    visited.add(start)
    steps = []
    while pq:
        d, cur = heapq.heappop(pq)
        steps.append((set(visited), cur))
        if cur == end:
            path = []
            node = end
            while node in came_from:
                path.append(node)
                node = came_from[node]
            path.append(start)
            return set(path), steps
        r, c = cur
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                nb = (nr, nc)
                if nb not in visited:
                    nd = dist[cur] + 1
                    if nd < dist.get(nb, 99999):
                        dist[nb] = nd
                        came_from[nb] = cur
                        visited.add(nb)
                        heapq.heappush(pq, (nd, nb))
    return None, steps


from collections import deque

def dp_solve(grid):
    R, C = len(grid), len(grid[0])
    dp = [[0]*C for _ in range(R)]
    dist = [[float('inf')]*C for _ in range(R)]
    if grid[0][0] == 1:
        return dp, dist

    q = deque()
    q.append((0, 0))
    dist[0][0] = 0
    dp[0][0] = 1

    while q:
        r, c = q.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0:
                nd = dist[r][c] + 1
                if nd < dist[nr][nc]:
                    dist[nr][nc] = nd
                    dp[nr][nc] = dp[r][c]
                    q.append((nr, nc))
                elif nd == dist[nr][nc]:
                    dp[nr][nc] += dp[r][c]
    return dp, dist


def dp_get_path(dp, dist, grid):
    R, C = len(dp), len(dp[0])
    path = set()
    if dist[R-1][C-1] == float('inf'):
        return path
    r, c = R-1, C-1
    path.add((r, c))
    while (r, c) != (0, 0):
        for dr, dc in [(-1,0),(0,-1),(1,0),(0,1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] == 0 and dist[nr][nc] == dist[r][c] - 1:
                r, c = nr, nc
                path.add((r, c))
                break
    return path


def draw_button(screen, font, text, x, y, w=130, h=36):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def _draw_pf_grid(screen, small, grid, start, end, path, visited, current, ox, oy):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            x = ox + c*CELL; y = oy + r*CELL
            cel = (r,c)
            if   cel == start:    color = GREEN
            elif cel == end:      color = RED
            elif cel in path:     color = PATH
            elif cel == current:  color = YELLOW
            elif cel in visited:  color = VISIT
            elif grid[r][c]==1:   color = WALL
            else:                 color = WHITE
            pygame.draw.rect(screen, color, (x+1,y+1,CELL-2,CELL-2))
            pygame.draw.rect(screen, GRAY,  (x,y,CELL,CELL), 1)


def _wait_next(screen, clock, font, label="Next →"):
    btn = pygame.Rect(630, 548, 160, 36)
    while True:
        pygame.draw.rect(screen, (180,230,180), btn, border_radius=6)
        pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
        screen.blit(font.render(label, True, BLACK), font.render(label,True,BLACK).get_rect(center=btn.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return False
            if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos): return True
        clock.tick(30)


def _render_puzzles_test(screen, clock, font, small, title, desc, grid, start, end, path, vis, current, note=""):
    ox = (800 - COLS*CELL) // 2
    oy = 130
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render(title, True, WHITE), (12,10))
    screen.blit(small.render(desc, True, DKGRAY), (12,56))
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12,82))
    pygame.draw.line(screen, GRAY, (0,100), (800,100), 1)
    _draw_pf_grid(screen, small, grid, start, end, path or set(), vis or set(), current, ox, oy)

    lx, ly = ox + COLS*CELL + 10, oy
    for col, lbl in [(GREEN, "Start"), (RED, "End"), (PATH, "Path"), (VISIT, "Visited")]:
        pygame.draw.rect(screen, col, (lx, ly, 14, 14))
        screen.blit(small.render(lbl, True, DKGRAY), (lx + 18, ly)); ly += 22
    pygame.display.flip()


def _draw_event_queue_test(screen, font, small, queue, sort_by, log, note="", highlight=-1):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render("Event Queue Test", True, WHITE), (12,10))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12,82))

    display_list = sorted(queue, key=lambda x: (x[0], x[1]) if sort_by == "priority" else x[1])
    SX, CY, QBW, QBH = 40, 320, 120, 54
    for i, (pri, t, eid, name) in enumerate(display_list):
        x = SX + i * (QBW + 10)
        color = GREEN if i == 0 else (ORANGE if i == len(display_list) - 1 else BLUE)
        if i == highlight:
            color = YELLOW
        pygame.draw.rect(screen, color, (x, CY - QBH // 2, QBW, QBH))
        pygame.draw.rect(screen, BLACK, (x, CY - QBH // 2, QBW, QBH), 2)
        screen.blit(small.render(name, True, BLACK), (x + 10, CY - 12))
        screen.blit(small.render(f"P{pri} T{t}", True, BLACK), (x + 10, CY + 8))

    header = font.render("Processed log:", True, BLUE)
    screen.blit(header, (520, 110))
    for i, entry in enumerate(log[-8:]):
        screen.blit(small.render(entry, True, DKGRAY), (520, 140 + i * 24))
    pygame.display.flip()


def _draw_dp_grid_test(screen, font, small, grid, dp_vals, dp_path, note=""):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render("DP Grid Test", True, WHITE), (12,10))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12,82))

    ox2 = (800 - DP_COLS * DP_CELL) // 2
    oy2 = 130
    for r in range(DP_ROWS):
        for c in range(DP_COLS):
            x = ox2 + c * DP_CELL
            y = oy2 + r * DP_CELL
            if grid[r][c] == 1:
                color = WALL
            elif (r, c) in dp_path:
                color = PATH
            elif (r, c) == (0, 0):
                color = GREEN
            elif (r, c) == (DP_ROWS - 1, DP_COLS - 1):
                color = RED
            else:
                color = WHITE
            pygame.draw.rect(screen, color, (x + 1, y + 1, DP_CELL - 2, DP_CELL - 2))
            pygame.draw.rect(screen, GRAY, (x, y, DP_CELL, DP_CELL), 1)
            if dp_vals and grid[r][c] == 0:
                vl = small.render(str(dp_vals[r][c]), True, DKGRAY)
                screen.blit(vl, vl.get_rect(center=(x + DP_CELL // 2, y + DP_CELL // 2)))

    pygame.display.flip()


def _animate_dp_path(screen, clock, font, small, grid, dp_vals, dp_path, ox2, oy2):
    path_list = sorted(dp_path)
    animated_path = set()
    for step, cell in enumerate(path_list):
        animated_path.add(cell)
        screen.fill(WHITE)
        pygame.draw.rect(screen, DKGRAY, (0,0,800,100))
        screen.blit(small.render("Revealing path...", True, WHITE), (20,12))
        
        for r in range(DP_ROWS):
            for c in range(DP_COLS):
                x = ox2 + c * DP_CELL
                y = oy2 + r * DP_CELL
                if grid[r][c] == 1:
                    color = WALL
                elif (r, c) in animated_path:
                    color = PATH
                elif (r, c) == (0, 0):
                    color = GREEN
                elif (r, c) == (DP_ROWS - 1, DP_COLS - 1):
                    color = RED
                else:
                    color = WHITE
                pygame.draw.rect(screen, color, (x + 1, y + 1, DP_CELL - 2, DP_CELL - 2))
                pygame.draw.rect(screen, GRAY, (x, y, DP_CELL, DP_CELL), 1)
                if dp_vals and grid[r][c] == 0:
                    vl = small.render(str(dp_vals[r][c]), True, DKGRAY)
                    screen.blit(vl, vl.get_rect(center=(x + DP_CELL // 2, y + DP_CELL // 2)))
        
        pygame.display.flip()
        pygame.time.delay(120)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()


def _wait_anim(screen, clock, duration_ms):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(60)


def run_puzzles_pathfinding_test(screen, clock, font, small):
    tests = [
        ("Dijkstra Test: Empty grid", "Finds path from start to end on an open grid.",
         [[0] * COLS for _ in range(COLS)], True),
        ("Dijkstra Test: Blocked route", "No path exists when column 1 is fully blocked.",
         [[1 if c == 1 else 0 for c in range(COLS)] for _ in range(ROWS)], False),
    ]
    start, end = (0, 0), (ROWS - 1, COLS - 1)

    for title, desc, grid, expected in tests:
        path, steps = dijkstra_animated(grid, start, end)
        path = path or set()

        for vis, current in steps:
            _render_puzzles_test(screen, clock, font, small, f"Test: {title}", desc, grid, start, end, set(), vis, current,
                                note="Exploring nodes...")
            pygame.time.delay(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

        vis = steps[-1][0] if steps else set()
        _render_puzzles_test(screen, clock, font, small, f"Test: {title}", desc, grid, start, end, path, vis, None,
                            note=f"Final path length: {len(path) - 1 if path else 0}")
        passed = bool(path and start in path and end in path) if expected else not bool(path)
        pygame.draw.rect(screen, GREEN if passed else RED, (10, 510, 780, 34), border_radius=6)
        screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                    font.render("RESULT: PASS", True, WHITE).get_rect(center=(400, 527)))
        msg = f"Expected: {'path exists' if expected else 'no path'}; Found: {'path' if path else 'no path'}"
        screen.blit(small.render(msg, True, DKGRAY), (12, 552))
        pygame.display.flip()
        if not _wait_next(screen, clock, font):
            return


def run_event_queue_test(screen, clock, font, small):
    events = [(3, "Email"), (1, "Backup"), (4, "Report"), (2, "Alert")]
    eq_pq = []
    eq_log = []
    sort_by = "priority"
    current_time = 1

    while True:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (0,0,800,48))
        screen.blit(font.render("Event Queue Test", True, WHITE), (12,10))
        pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)

        btn_add     = draw_button(screen, small, "Add Event",      20, 96, w=130)
        btn_proc    = draw_button(screen, small, "Process Next",  160, 96, w=140)
        btn_clr     = draw_button(screen, small, "Clear",         310, 96, w=80)
        btn_by_pri  = draw_button(screen, small, "Sort: Priority",410, 96, w=150)
        btn_by_time = draw_button(screen, small, "Sort: Time",    570, 96, w=120)
        btn_next    = draw_button(screen, small, "Next →",        700, 96, w=80)

        active_btn  = btn_by_pri if sort_by=="priority" else btn_by_time
        pygame.draw.rect(screen, BLUE, active_btn, border_radius=6)
        pygame.draw.rect(screen, BLACK, active_btn, 2, border_radius=6)
        screen.blit(small.render("Sort: Priority" if sort_by=="priority" else "Sort: Time",True,WHITE),
                    small.render("Sort: Priority",True,WHITE).get_rect(center=active_btn.center))

        pygame.draw.rect(screen, DKGRAY, (20,140,560,24))
        screen.blit(small.render("  Priority",True,WHITE),(25,143))
        screen.blit(small.render("Time Added",True,WHITE),(160,143))
        screen.blit(small.render("Event Name",True,WHITE),(310,143))

        display_list = sorted(eq_pq, key=lambda x:(x[0],x[1]) if sort_by=="priority" else x[1])
        for i,(pri,t,eid,name) in enumerate(display_list[:9]):
            row_y=168+i*34; row_color=(min(255,pri*25),max(60,255-pri*20),80)
            row=pygame.Rect(20,row_y,560,28)
            pygame.draw.rect(screen, row_color, row, border_radius=4)
            pygame.draw.rect(screen, BLACK, row, 1, border_radius=4)
            screen.blit(small.render(f"     P{pri}",True,BLACK),(25,row_y+6))
            screen.blit(small.render(f"T={t}",True,BLACK),(160,row_y+6))
            screen.blit(small.render(name,True,BLACK),(310,row_y+6))

        screen.blit(font.render("Processed log:",True,BLUE),(600,140))
        for i,entry in enumerate(eq_log[-10:]):
            screen.blit(small.render(entry,True,DKGRAY),(600,170+i*28))

        pygame.display.flip()

        if current_time <= len(events) and len(eq_pq) < len(events):
            pri, name = events[current_time - 1]
            heapq.heappush(eq_pq, (pri, current_time, len(eq_pq) + 1, name))
            current_time += 1
            pygame.time.delay(800)
            continue
        elif len(eq_log) < 3 and eq_pq:
            if sort_by=="priority":
                pri,t,_,name = heapq.heappop(eq_pq)
            else:
                earliest = min(eq_pq, key=lambda x:x[1])
                eq_pq.remove(earliest)
                heapq.heapify(eq_pq)
                pri,t,_,name = earliest
            eq_log.append(f"P{pri} T{t} {name}")
            pygame.time.delay(800)
            continue
        else:
            processed = [tuple(x.split()) for x in eq_log]
            processed_priorities = [int(p[0][1:]) for p in processed] if processed else []
            passed = processed_priorities == sorted(processed_priorities) and len(eq_pq) == 1
            pygame.draw.rect(screen, GREEN if passed else RED, (10, 510, 780, 34))
            screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                        font.render("RESULT: PASS", True, WHITE).get_rect(center=(400, 527)))
            msg = f"Processed order: {processed_priorities}; remaining size: {len(eq_pq)}"
            screen.blit(small.render(msg, True, DKGRAY), (12, 552))
            pygame.display.flip()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if btn_next.collidepoint(event.pos):
                            waiting = False
            return


def run_dp_grid_test(screen, clock, font, small):
    grid = [[0] * DP_COLS for _ in range(DP_ROWS)]
    for c in range(DP_COLS):
        grid[2][c] = 1
        _draw_dp_grid_test(screen, font, small, grid, None, set(), note=f"Blocking row 2, obstacle {c + 1}/{DP_COLS}")
        _wait_anim(screen, clock, 150)

    dp_vals, dp_dist = dp_solve(grid)
    dp_path = set()
    _draw_dp_grid_test(screen, font, small, grid, dp_vals, dp_path,
                       note="Solved: no path exists between S and G.")
    passed = dp_vals[DP_ROWS - 1][DP_COLS - 1] == 0 and not dp_path
    pygame.draw.rect(screen, GREEN if passed else RED, (10, 510, 780, 34))
    screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                font.render("RESULT: PASS", True, WHITE).get_rect(center=(400, 527)))
    msg = "Expected: no paths; Found: no paths." if passed else "Path count mismatch."
    screen.blit(small.render(msg, True, DKGRAY), (12, 552))
    pygame.display.flip()
    if not _wait_next(screen, clock, font):
        return


def run_puzzles_test(screen, clock, font, small, tab):
    if tab == 0:
        run_puzzles_pathfinding_test(screen, clock, font, small)
    elif tab == 1:
        run_event_queue_test(screen, clock, font, small)
    else:
        run_dp_grid_test(screen, clock, font, small)


def run_puzzles(screen, clock, font, small):
    tab = 0

    pf_grid    = [[0]*COLS for _ in range(ROWS)]
    pf_start   = (0, 0); pf_end = (ROWS-1, COLS-1)
    pf_steps   = []; pf_step_i = 0
    pf_path    = set(); pf_full_path = set(); pf_visited = set(); pf_current = None
    pf_playing = False; pf_done = False; pf_timer = 0
    pf_mode    = "draw"
    pf_message = "Left-click = place walls, Right-click = remove. Then press Run Pathfinding."

    eq_pq=[]; eq_log=[]; eq_id=0; eq_time=1; eq_sort_by="priority"
    eq_message = "Add events then sort/process them by Priority or Time."
    EVENT_NAMES = ["Payment","Alert","Backup","Email","Report","Deploy"]

    dp_grid=[[0]*DP_COLS for _ in range(DP_ROWS)]; dp_vals=None; dp_dist=None; dp_path=set()
    dp_message = "Click cells to add/remove walls, then press Solve."

    ox = (800-COLS*CELL)//2; oy = 165

    while True:
        screen.fill(WHITE)
        screen.blit(font.render("Puzzle Challenges", True, BLUE), (20,15))

        btn_tab0 = draw_button(screen, small, TABS[0], 20,  52, w=160)
        btn_tab1 = draw_button(screen, small, TABS[1], 188, 52, w=145)
        btn_tab2 = draw_button(screen, small, TABS[2], 343, 52, w=110)
        btn_back = draw_button(screen, small, "< Menu", 670, 52, w=110)

        for i, (btn,t) in enumerate([(btn_tab0,TABS[0]),(btn_tab1,TABS[1]),(btn_tab2,TABS[2])]):
            if i == tab:
                pygame.draw.rect(screen, BLUE, btn, border_radius=6)
                pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
                screen.blit(small.render(t,True,WHITE), small.render(t,True,WHITE).get_rect(center=btn.center))

        if tab == 0:
            btn_run   = draw_button(screen, small, "Run Pathfinding", 20,  96, w=130)
            btn_clear = draw_button(screen, small, "Clear Path",     162, 96, w=105)
            btn_reset = draw_button(screen, small, "Reset Grid",     273, 96, w=105)
            btn_setS  = draw_button(screen, small, "Set Start",      384, 96, w=100)
            btn_setE  = draw_button(screen, small, "Set End",        494, 96, w=85)
            btn_test  = draw_button(screen, small, "Test",           589, 96, w=60)
            if pf_playing:
                pf_timer += 1
                if pf_timer % 2 == 0 and pf_step_i < len(pf_steps):
                    pf_visited, pf_current = pf_steps[pf_step_i]
                    pf_step_i += 1
                if pf_step_i >= len(pf_steps):
                    pf_playing = False
                    pf_done = True
                    pf_path = pf_full_path
                    if pf_path:
                        pf_message = f"Path found! {len(pf_path)-1} steps."
                    else:
                        pf_message = "Search complete, no path found."
            _draw_pf_grid(screen, small, pf_grid, pf_start, pf_end, pf_path, pf_visited, pf_current, ox, oy)
            lx, ly = ox+COLS*CELL+10, oy
            for col,lbl in [(GREEN,"Start"),(RED,"End"),(WALL,"Wall"),(PATH,"Path"),(VISIT,"Visited")]:
                pygame.draw.rect(screen, col, (lx,ly,14,14))
                screen.blit(small.render(lbl,True,DKGRAY),(lx+18,ly)); ly+=22
            screen.blit(small.render(pf_message,True,DKGRAY),(20,560))

        elif tab == 1:
            btn_add     = draw_button(screen, small, "Add Event",      20, 96, w=130)
            btn_proc    = draw_button(screen, small, "Process Next",  160, 96, w=140)
            btn_clr     = draw_button(screen, small, "Clear",         310, 96, w=80)
            btn_by_pri  = draw_button(screen, small, "Sort: Priority",410, 96, w=150)
            btn_by_time = draw_button(screen, small, "Sort: Time",    570, 96, w=120)
            btn_test    = draw_button(screen, small, "Test",         690, 96, w=60)
            active_btn  = btn_by_pri if eq_sort_by=="priority" else btn_by_time
            pygame.draw.rect(screen, BLUE, active_btn, border_radius=6)
            pygame.draw.rect(screen, BLACK, active_btn, 2, border_radius=6)
            screen.blit(small.render("Sort: Priority" if eq_sort_by=="priority" else "Sort: Time",True,WHITE),
                        small.render("Sort: Priority",True,WHITE).get_rect(center=active_btn.center))
            pygame.draw.rect(screen, DKGRAY, (20,140,560,24))
            screen.blit(small.render("  Priority",True,WHITE),(25,143))
            screen.blit(small.render("Time Added",True,WHITE),(160,143))
            screen.blit(small.render("Event Name",True,WHITE),(310,143))
            display_list = sorted(eq_pq, key=lambda x:(x[0],x[1]) if eq_sort_by=="priority" else x[1])
            for i,(pri,t,eid,name) in enumerate(display_list[:9]):
                row_y=168+i*34; row_color=(min(255,pri*25),max(60,255-pri*20),80)
                row=pygame.Rect(20,row_y,560,28)
                pygame.draw.rect(screen, row_color, row, border_radius=4)
                pygame.draw.rect(screen, BLACK, row, 1, border_radius=4)
                screen.blit(small.render(f"     P{pri}",True,BLACK),(25,row_y+6))
                screen.blit(small.render(f"T={t}",True,BLACK),(160,row_y+6))
                screen.blit(small.render(name,True,BLACK),(310,row_y+6))
            screen.blit(font.render("Processed log:",True,BLUE),(600,140))
            for i,entry in enumerate(eq_log[-10:]):
                screen.blit(small.render(entry,True,DKGRAY),(600,170+i*28))
            screen.blit(small.render(eq_message,True,DKGRAY),(20,560))

        elif tab == 2:
            btn_solve = draw_button(screen, small, "Solve",     20,96,w=100)
            btn_path  = draw_button(screen, small, "Show Path",130,96,w=120)
            btn_clrdp = draw_button(screen, small, "Clear",    260,96,w=90)
            btn_test  = draw_button(screen, small, "Test",     360,96,w=60)
            ox2=(800-DP_COLS*DP_CELL)//2; oy2=140
            for r in range(DP_ROWS):
                for c in range(DP_COLS):
                    x=ox2+c*DP_CELL; y=oy2+r*DP_CELL
                    if   dp_grid[r][c]==1:              color=WALL
                    elif (r,c) in dp_path:              color=PATH
                    elif (r,c)==(0,0):                  color=GREEN
                    elif (r,c)==(DP_ROWS-1,DP_COLS-1): color=RED
                    else:                               color=WHITE
                    pygame.draw.rect(screen,color,(x+1,y+1,DP_CELL-2,DP_CELL-2),border_radius=4)
                    pygame.draw.rect(screen,GRAY,(x,y,DP_CELL,DP_CELL),1)
                    if dp_vals and dp_grid[r][c]==0:
                        vl=small.render(str(dp_vals[r][c]),True,DKGRAY)
                        screen.blit(vl,vl.get_rect(center=(x+DP_CELL//2,y+DP_CELL//2)))
            screen.blit(small.render("S",True,BLACK),(ox2+DP_CELL//2-5,oy2+DP_CELL//2-8))
            screen.blit(small.render("G",True,BLACK),(ox2+(DP_COLS-1)*DP_CELL+DP_CELL//2-5,oy2+(DP_ROWS-1)*DP_CELL+DP_CELL//2-8))
            screen.blit(small.render(dp_message,True,DKGRAY),(20,560))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: return

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                if btn_back.collidepoint(pos): return
                elif btn_tab0.collidepoint(pos): tab=0
                elif btn_tab1.collidepoint(pos): tab=1
                elif btn_tab2.collidepoint(pos): tab=2

                elif tab==0:
                    if btn_run.collidepoint(pos):
                        pf_full_path, pf_steps = dijkstra_animated(pf_grid, pf_start, pf_end)
                        pf_full_path = pf_full_path or set()
                        pf_path = set()
                        pf_visited = set()
                        pf_current = None
                        pf_step_i = 0
                        pf_timer = 0
                        pf_playing = True
                        pf_done = False
                        pf_message = "Searching..."
                        if not pf_steps:
                            pf_playing = False
                            pf_done = True
                            pf_message = "No path found!"
                    elif btn_clear.collidepoint(pos):
                        pf_path = set(); pf_full_path = set(); pf_visited = set(); pf_current = None
                        pf_playing = False; pf_done = False; pf_message = "Path cleared."
                    elif btn_reset.collidepoint(pos):
                        pf_grid = [[0] * COLS for _ in range(ROWS)]
                        pf_path = set(); pf_full_path = set(); pf_visited = set(); pf_current = None
                        pf_playing = False; pf_done = False; pf_message = "Grid reset."
                    elif btn_setS.collidepoint(pos): pf_mode="start"; pf_message="Click a cell to set START."
                    elif btn_setE.collidepoint(pos): pf_mode="end";   pf_message="Click a cell to set END."
                    elif btn_test.collidepoint(pos): run_puzzles_test(screen, clock, font, small, tab)
                    else:
                        c=(pos[0]-ox)//CELL; r=(pos[1]-oy)//CELL
                        if 0<=r<ROWS and 0<=c<COLS:
                            cell=(r,c)
                            if pf_mode=="start":
                                pf_start=cell; pf_mode="draw"; pf_message=f"Start={cell}."
                                pf_playing=False; pf_current=None; pf_path=set(); pf_full_path=set(); pf_visited=set()
                            elif pf_mode=="end":
                                pf_end=cell; pf_mode="draw"; pf_message=f"End={cell}."
                                pf_playing=False; pf_current=None; pf_path=set(); pf_full_path=set(); pf_visited=set()
                            elif cell!=pf_start and cell!=pf_end:
                                if event.button == 1:
                                    pf_grid[r][c]=1
                                elif event.button == 3:
                                    pf_grid[r][c]=0
                                pf_playing=False; pf_current=None; pf_path=set(); pf_full_path=set(); pf_visited=set()

                elif tab==1:
                    if btn_add.collidepoint(pos):
                        pri=random.randint(1,10); name=random.choice(EVENT_NAMES)
                        eq_id+=1; heapq.heappush(eq_pq,(pri,eq_time,eq_id,name))
                        eq_message=f"Added '{name}' P={pri} T={eq_time}"; eq_time+=1
                    elif btn_proc.collidepoint(pos):
                        if eq_pq:
                            if eq_sort_by=="priority": pri,t,_,name=heapq.heappop(eq_pq)
                            else:
                                earliest=min(eq_pq,key=lambda x:x[1]); eq_pq.remove(earliest)
                                heapq.heapify(eq_pq); pri,t,_,name=earliest
                            eq_log.append(f"P{pri} T{t} {name}")
                            eq_message=f"Processed '{name}' P={pri} T={t}"
                        else: eq_message="Queue is empty!"
                    elif btn_clr.collidepoint(pos): eq_pq=[]; eq_log=[]; eq_time=1; eq_message="Cleared."
                    elif btn_by_pri.collidepoint(pos): eq_sort_by="priority"; eq_message="Sorting by Priority."
                    elif btn_by_time.collidepoint(pos): eq_sort_by="time"; eq_message="Sorting by Time."
                    elif btn_test.collidepoint(pos): run_puzzles_test(screen, clock, font, small, tab)

                elif tab==2:
                    if btn_solve.collidepoint(pos):
                        dp_vals, dp_dist = dp_solve(dp_grid)
                        dp_path = set()
                        dp_message = f"Total shortest paths S→G: {dp_vals[DP_ROWS-1][DP_COLS-1]}  Click 'Show Path' to visualize."
                    elif btn_path.collidepoint(pos):
                        if dp_vals is None:
                            dp_vals, dp_dist = dp_solve(dp_grid)
                        if dp_vals[DP_ROWS-1][DP_COLS-1]:
                            dp_path = dp_get_path(dp_vals, dp_dist, dp_grid)
                            ox2 = (800-DP_COLS*DP_CELL)//2
                            oy2 = 140
                            _animate_dp_path(screen, clock, font, small, dp_grid, dp_vals, dp_path, ox2, oy2)
                            dp_message = "One shortest path shown in yellow."
                        else:
                            dp_path = set()
                            dp_message = "No path exists."
                    elif btn_clrdp.collidepoint(pos):
                        dp_grid=[[0]*DP_COLS for _ in range(DP_ROWS)]; dp_vals=None; dp_dist=None; dp_path=set()
                        dp_message="Grid cleared."
                    elif btn_test.collidepoint(pos):
                        run_puzzles_test(screen, clock, font, small, tab)
                    else:
                        ox2=(800-DP_COLS*DP_CELL)//2; oy2=140
                        c=(pos[0]-ox2)//DP_CELL; r=(pos[1]-oy2)//DP_CELL
                        if 0<=r<DP_ROWS and 0<=c<DP_COLS and (r,c) not in [(0,0),(DP_ROWS-1,DP_COLS-1)]:
                            dp_grid[r][c]^=1; dp_vals=None; dp_path=set()

            if event.type==pygame.MOUSEMOTION:
                if tab==0 and pygame.mouse.get_pressed()[0] and pf_mode=="draw":
                    c=(event.pos[0]-ox)//CELL; r=(event.pos[1]-oy)//CELL
                    if 0<=r<ROWS and 0<=c<COLS:
                        cell=(r,c)
                        if cell!=pf_start and cell!=pf_end: pf_grid[r][c]=1

        clock.tick(30)
