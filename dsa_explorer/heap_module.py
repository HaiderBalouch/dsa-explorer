import pygame
import sys
import random

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GREEN  = (144, 238, 144)
RED    = (255, 100, 100)
YELLOW = (255, 220, 80)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)


heap = []   

def heap_insert(h, val):
    h.append(val)
    i = len(h) - 1
    while i > 0:
        parent = (i - 1) // 2
        if h[parent] > h[i]:
            h[parent], h[i] = h[i], h[parent]
            i = parent
        else:
            break
    return h

def heap_extract_min(h):
    if not h:
        return None, h
    if len(h) == 1:
        return h.pop(), h
    root = h[0]
    h[0] = h.pop()
    i = 0
    n = len(h)
    while True:
        smallest = i
        l, r = 2*i+1, 2*i+2
        if l < n and h[l] < h[smallest]:
            smallest = l
        if r < n and h[r] < h[smallest]:
            smallest = r
        if smallest != i:
            h[i], h[smallest] = h[smallest], h[i]
            i = smallest
        else:
            break
    return root, h


def get_positions(n):
    positions = {}
    level = 0
    start = 0
    while start < n:
        count   = min(2**level, n - start)
        level_y = 160 + level * 90
        slots   = 2**level
        for j in range(count):
            idx = start + j
            x   = int(400 - (slots - 1) * 50 + j * 100)
            positions[idx] = (x, level_y)
        start += count
        level += 1
    return positions


def _wait_next_heap(screen, clock, font, label="Next →"):
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


def _draw_heap_tree(screen, font, h):
    if not h: return
    pos = get_positions(len(h))
    for i in range(len(h)):
        l,r = 2*i+1, 2*i+2
        if l < len(h): pygame.draw.line(screen, DKGRAY, pos[i], pos[l], 2)
        if r < len(h): pygame.draw.line(screen, DKGRAY, pos[i], pos[r], 2)
    for i,v in enumerate(h):
        cx,cy = pos[i]
        pygame.draw.circle(screen, YELLOW if i==0 else BLUE, (cx,cy), 26)
        pygame.draw.circle(screen, BLACK, (cx,cy), 26, 2)
        screen.blit(font.render(str(v),True,BLACK), font.render(str(v),True,BLACK).get_rect(center=(cx,cy)))
    screen.blit(pygame.font.SysFont(None,22).render("MIN →",True,RED), (pos[0][0]+30, pos[0][1]-10))


def run_heap_test(screen, clock, font, small):
    tests = [
        ("Heap: root always = minimum after inserts", [40,10,70,5], "root_min"),
        ("Heap: extract min removes smallest value",  [15,3,9],     "extract"),
        ("Heap: extract from empty → returns None",   [],            "empty"),
    ]

    for test_name, values, mode in tests:
        h = []

        if mode == "root_min":
            for v in values:
                h = heap_insert(h, v)
                screen.fill(WHITE)
                pygame.draw.rect(screen, BLUE, (0,0,800,48))
                screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
                screen.blit(small.render("Yellow = root (MIN). Expected: root always = smallest inserted.", True, DKGRAY), (12,56))
                pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
                screen.blit(small.render(f"Inserted {v}   heap array: {h}   root = {h[0]}", True, DKGRAY), (12,82))
                _draw_heap_tree(screen, font, h)
                pygame.display.flip()
                pygame.time.delay(600)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
            screen.blit(small.render("All inserted. Root should be 5 (minimum of [40,10,70,5])", True, DKGRAY), (12,56))
            pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
            screen.blit(small.render(f"Final heap: {h}   root = {h[0]}", True, DKGRAY), (12,82))
            _draw_heap_tree(screen, font, h)
            passed = h[0] == min(h)
            col = (60,200,100) if passed else (220,60,60)
            pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
            screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                        font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))

        elif mode == "extract":
            for v in values: h = heap_insert(h, v)
            before = list(h)

            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
            screen.blit(small.render("Before extract — heap shown below", True, DKGRAY), (12,56))
            pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
            screen.blit(small.render(f"Heap: {before}   root = {before[0]}", True, DKGRAY), (12,82))
            _draw_heap_tree(screen, font, before)
            pygame.display.flip()
            pygame.time.delay(800)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

            extracted, h = heap_extract_min(list(before))
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
            screen.blit(small.render(f"Extracted {extracted}. Heap restructured. New min = {h[0] if h else 'N/A'}", True, DKGRAY), (12,56))
            pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
            screen.blit(small.render(f"Heap after extract: {h}", True, DKGRAY), (12,82))
            _draw_heap_tree(screen, font, h)
            passed = extracted==3 and (h[0]==min(h) if h else True)
            col = (60,200,100) if passed else (220,60,60)
            pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
            screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                        font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))

        else:
            result, _ = heap_extract_min([])
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
            screen.blit(small.render("Extract from empty heap. Expected: returns None, no crash.", True, DKGRAY), (12,56))
            pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
            screen.blit(font.render("Heap is empty!", True, RED), font.render("Heap is empty!",True,RED).get_rect(center=(400,300)))
            screen.blit(small.render(f"heap_extract_min([]) returned: {result}  (None = correct)", True, DKGRAY), (12,82))
            passed = result is None
            col = (60,200,100) if passed else (220,60,60)
            pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
            screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                        font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))

        if not _wait_next_heap(screen, clock, font): return


def draw_button(screen, font, text, x, y, w=130, h=40):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def run_heap(screen, clock, font, small):
    global heap
    heap    = []
    message = "Insert values into the min-heap. The smallest is always at the top!"

    while True:
        screen.fill(WHITE)

        title = font.render("Min-Heap Visualiser", True, BLUE)
        screen.blit(title, (20, 15))

        btn_insert  = draw_button(screen, small, "Insert",      20, 60, w=110)
        btn_extract = draw_button(screen, small, "Extract Min", 140, 60, w=140)
        btn_clear   = draw_button(screen, small, "Clear",       290, 60, w=90)
        btn_back    = draw_button(screen, small, "< Menu",      390, 60, w=100)
        btn_test    = draw_button(screen, small, "Test",        500, 60, w=70)

        if heap:
            positions = get_positions(len(heap))

            for i in range(len(heap)):
                l, r = 2*i+1, 2*i+2
                if l < len(heap):
                    pygame.draw.line(screen, DKGRAY, positions[i], positions[l], 2)
                if r < len(heap):
                    pygame.draw.line(screen, DKGRAY, positions[i], positions[r], 2)

            for i, val in enumerate(heap):
                cx, cy = positions[i]
                color  = YELLOW if i == 0 else BLUE   
                pygame.draw.circle(screen, color, (cx, cy), 26)
                pygame.draw.circle(screen, BLACK, (cx, cy), 26, 2)
                lbl = font.render(str(val), True, BLACK)
                screen.blit(lbl, lbl.get_rect(center=(cx, cy)))

            root_lbl = small.render("MIN", True, RED)
            screen.blit(root_lbl, (positions[0][0] + 30, positions[0][1] - 10))

            arr_lbl = small.render(f"Array: {heap}", True, DKGRAY)
            screen.blit(arr_lbl, (20, 520))
        else:
            empty = font.render("Heap is empty — press Insert!", True, DKGRAY)
            screen.blit(empty, empty.get_rect(center=(400, 350)))

        size_lbl = small.render(f"Size: {len(heap)}", True, DKGRAY)
        screen.blit(size_lbl, (20, 120))

        msg_lbl = small.render(message, True, DKGRAY)
        screen.blit(msg_lbl, (20, 560))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return
                elif btn_test.collidepoint(event.pos):
                    run_heap_test(screen, clock, font, small)
                elif btn_insert.collidepoint(event.pos):
                    v    = random.randint(1, 99)
                    heap = heap_insert(heap, v)
                    message = f"Inserted {v}. Min is {heap[0]}."
                elif btn_extract.collidepoint(event.pos):
                    if heap:
                        v, heap = heap_extract_min(heap)
                        message = f"Extracted min: {v}." + (f" New min: {heap[0]}." if heap else " Heap is now empty.")
                    else:
                        message = "Heap is empty!"
                elif btn_clear.collidepoint(event.pos):
                    heap    = []
                    message = "Heap cleared."

        clock.tick(30)
