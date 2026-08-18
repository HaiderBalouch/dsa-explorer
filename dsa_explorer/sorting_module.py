import pygame
import sys
import random

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
YELLOW = (255, 230, 80)
RED    = (255, 100, 100)
GREEN  = (100, 220, 100)
PURPLE = (180, 100, 220)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)

ARRAY_SIZE = 16


def draw_button(screen, font, text, x, y, w=120, h=40):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def bubble_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            steps.append((list(a), j, j + 1, None))
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                steps.append((list(a), j, j + 1, None))
    steps.append((list(a), -1, -1, None))
    return steps


def selection_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps.append((list(a), min_idx, j, None))
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append((list(a), i, min_idx, None))
    steps.append((list(a), -1, -1, None))
    return steps


def merge_sort_steps(arr):
    a = arr[:]
    steps = []
    n = len(a)
    size = 1
    while size < n:
        for lo in range(0, n, size * 2):
            mid  = min(lo + size,     n)
            hi   = min(lo + size * 2, n)
            left = a[lo:mid]
            rght = a[mid:hi]
            i = j = 0
            k = lo
            while i < len(left) and j < len(rght):
                ci = lo + i
                cj = mid + j
                steps.append((list(a), ci, cj, (lo, hi)))
                if left[i] <= rght[j]:
                    a[k] = left[i]; i += 1
                else:
                    a[k] = rght[j]; j += 1
                k += 1
            while i < len(left):
                a[k] = left[i]; i += 1; k += 1
            while j < len(rght):
                a[k] = rght[j]; j += 1; k += 1
            steps.append((list(a), -1, -1, (lo, hi)))
        size *= 2
    steps.append((list(a), -1, -1, None))
    return steps


def _wait_next_sort(screen, clock, font, label="Next →"):
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


def _draw_bars(screen, small, snap, compare, done, BAR_X=30, BAR_Y=110, BAR_W=740, BAR_H=370):
    max_v = max(snap) if snap else 1
    bar_w = BAR_W // len(snap)
    for i,v in enumerate(snap):
        bh = int(v/max_v*BAR_H)
        x  = BAR_X + i*bar_w
        y  = BAR_Y + BAR_H - bh
        col = (100,220,100) if done else ((255,100,100) if i in compare else (100,149,237))
        pygame.draw.rect(screen, col, (x+2,y,bar_w-4,bh))
        pygame.draw.rect(screen, (0,0,0), (x+2,y,bar_w-4,bh), 1)
    screen.blit(small.render(f"Array: {snap}", True, (100,100,100)), (12,490))


def run_sorting_test(screen, clock, font, small):
    tests = [
        ("Bubble Sort: [5,3,8,1,2] → [1,2,3,5,8]", bubble_sort_steps, [5,3,8,1,2], [1,2,3,5,8]),
        ("Selection Sort: [5,3,8,1,2] → [1,2,3,5,8]", selection_sort_steps, [5,3,8,1,2], [1,2,3,5,8]),
        ("Merge Sort: [5,3,8,1,2] → [1,2,3,5,8]", merge_sort_steps, [5,3,8,1,2], [1,2,3,5,8]),
    ]

    for test_name, sort_fn, arr, expected in tests:
        steps = list(sort_fn(arr))
        sample = steps[::max(1, len(steps)//30)] + [steps[-1]]

        for frame_i, frame in enumerate(sample):
            snap, ci, cj = frame[0], frame[1], frame[2]
            done = (frame_i == len(sample)-1)
            screen.fill((255,255,255))
            pygame.draw.rect(screen, (100,149,237), (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, (255,255,255)), (12,10))
            screen.blit(small.render("Red = comparing   Green = sorted   animating step by step...", True, (100,100,100)), (12,56))
            pygame.draw.line(screen, (200,200,200), (0,76), (800,76), 1)
            _draw_bars(screen, small, snap, (ci,cj), done)

            if not done:
                screen.blit(small.render(f"Comparing indices {ci} and {cj}", True, (100,100,100)), (12,82))
            else:
                passed = snap == expected
                col = (60,200,100) if passed else (220,60,60)
                pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
                screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, (255,255,255)),
                            font.render("RESULT: PASS",True,(255,255,255)).get_rect(center=(400,527)))
                screen.blit(small.render(f"Final array: {snap}  Expected: {expected}", True, (100,100,100)), (12,82))

            pygame.display.flip()
            pygame.time.delay(40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        if not _wait_next_sort(screen, clock, font): return


def run_sorting(screen, clock, font, small):
    arr     = [random.randint(10, 100) for _ in range(ARRAY_SIZE)]
    steps   = []
    step_i  = 0
    playing = False
    done    = False
    algo    = "Bubble"
    message = "Pick an algorithm and press Start."
    compare = (-1, -1)
    merge_range = None
    current_arr = list(arr)
    auto_timer  = 0

    while True:
        screen.fill(WHITE)

        title = font.render(f"Sorting - {algo} Sort", True, BLUE)
        screen.blit(title, (20, 15))

        btn_bubble = draw_button(screen, small, "Bubble",    20,  60, w=100)
        btn_sel    = draw_button(screen, small, "Selection", 128, 60, w=110)
        btn_merge  = draw_button(screen, small, "Merge",     246, 60, w=85)
        btn_start  = draw_button(screen, small, "Start",     339, 60, w=80)
        btn_step   = draw_button(screen, small, "Step",      427, 60, w=75)
        btn_shuf   = draw_button(screen, small, "Shuffle",   510, 60, w=90)
        btn_back   = draw_button(screen, small, "< Menu",    608, 60, w=100)
        btn_test   = draw_button(screen, small, "Test",      716, 60, w=70)

        bar_area_x = 30
        bar_area_y = 120
        bar_area_w = 740
        bar_area_h = 400
        max_val    = max(current_arr) if current_arr else 1
        bar_w      = bar_area_w // len(current_arr)

        for i, v in enumerate(current_arr):
            bar_h = int(v / max_val * bar_area_h)
            x     = bar_area_x + i * bar_w
            y     = bar_area_y + bar_area_h - bar_h

            if done:
                color = GREEN
            elif i in compare:
                color = RED
            elif merge_range and merge_range[0] <= i < merge_range[1]:
                color = PURPLE
            else:
                color = BLUE

            pygame.draw.rect(screen, color, (x + 2, y, bar_w - 4, bar_h))
            pygame.draw.rect(screen, BLACK, (x + 2, y, bar_w - 4, bar_h), 1)

        msg_lbl = small.render(message, True, DKGRAY)
        screen.blit(msg_lbl, (20, 540))

        pygame.draw.rect(screen, RED,    (20,  565, 14, 14))
        screen.blit(small.render("Comparing",    True, DKGRAY), (38,  563))
        pygame.draw.rect(screen, PURPLE, (160, 565, 14, 14))
        screen.blit(small.render("Merge window", True, DKGRAY), (178, 563))
        pygame.draw.rect(screen, GREEN,  (320, 565, 14, 14))
        screen.blit(small.render("Sorted!",      True, DKGRAY), (338, 563))

        pygame.display.flip()

        if playing and not done:
            auto_timer += 1
            if auto_timer >= 3:
                auto_timer = 0
                if step_i < len(steps):
                    current_arr, ci, cj, merge_range = steps[step_i]
                    compare = (ci, cj)
                    step_i += 1
                else:
                    playing = False
                    done    = True
                    compare = (-1, -1)
                    merge_range = None
                    message = "Done! Array is sorted."

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(event.pos):
                    return
                elif btn_test.collidepoint(event.pos):
                    run_sorting_test(screen, clock, font, small)
                elif btn_bubble.collidepoint(event.pos):
                    algo = "Bubble"; playing = False; done = False
                    merge_range = None
                    message = "Bubble Sort selected. Press Start."
                elif btn_sel.collidepoint(event.pos):
                    algo = "Selection"; playing = False; done = False
                    merge_range = None
                    message = "Selection Sort selected. Press Start."
                elif btn_merge.collidepoint(event.pos):
                    algo = "Merge"; playing = False; done = False
                    merge_range = None
                    message = "Merge Sort selected. Press Start."
                elif btn_shuf.collidepoint(event.pos):
                    arr = [random.randint(10, 100) for _ in range(ARRAY_SIZE)]
                    current_arr = list(arr)
                    playing = False; done = False; steps = []
                    compare = (-1, -1); merge_range = None
                    message = "Shuffled! Press Start."
                elif btn_start.collidepoint(event.pos):
                    if algo == "Bubble":
                        steps = bubble_sort_steps(arr)
                    elif algo == "Selection":
                        steps = selection_sort_steps(arr)
                    else:
                        steps = merge_sort_steps(arr)
                    current_arr = list(arr)
                    step_i  = 0
                    playing = True
                    done    = False
                    compare = (-1, -1)
                    merge_range = None
                    message = f"Running {algo} Sort..."
                elif btn_step.collidepoint(event.pos):
                    if not steps:
                        if algo == "Bubble":
                            steps = bubble_sort_steps(arr)
                        elif algo == "Selection":
                            steps = selection_sort_steps(arr)
                        else:
                            steps = merge_sort_steps(arr)
                        current_arr = list(arr)
                        step_i = 0
                    playing = False
                    if step_i < len(steps):
                        current_arr, ci, cj, merge_range = steps[step_i]
                        compare = (ci, cj)
                        step_i += 1
                        message = f"Step {step_i} of {len(steps)}"
                    else:
                        done    = True
                        compare = (-1, -1)
                        merge_range = None
                        message = "Done!"

        clock.tick(60)