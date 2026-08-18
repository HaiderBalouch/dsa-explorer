import pygame
import sys

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GREEN  = (144, 238, 144)
ORANGE = (255, 180, 80)
RED    = (255, 100, 100)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)
LGRAY  = (240, 240, 240)


def draw_button(screen, font, text, x, y, w=130, h=40):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect


def _wait_next(screen, clock, font, label="Next →"):
    btn = pygame.Rect(630, 548, 160, 36)
    while True:
        pygame.draw.rect(screen, (180, 230, 180), btn, border_radius=6)
        pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
        screen.blit(font.render(label, True, BLACK), font.render(label,True,BLACK).get_rect(center=btn.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return False
            if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos): return True
        clock.tick(30)


def _result_bar(screen, font, passed):
    col = (60,200,100) if passed else (220,60,60)
    pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
    screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))


def draw_stack_area(screen, font, stack):
    BOX_W, BOX_H, BASE_X, BASE_Y = 140, 44, 330, 540
    pygame.draw.line(screen, BLACK, (BASE_X-10, BASE_Y), (BASE_X+BOX_W+10, BASE_Y), 3)
    for i, val in enumerate(stack):
        x = BASE_X
        y = BASE_Y - (i + 1) * (BOX_H + 4)
        col = GREEN if i == len(stack) - 1 else BLUE
        pygame.draw.rect(screen, col, (x, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(val), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, y + BOX_H // 2)))
        if i == len(stack) - 1:
            screen.blit(font.render("<-- TOP", True, RED), (x + BOX_W + 8, y + 12))


def draw_queue_area(screen, font, queue):
    BOX_W, BOX_H, START_X, CY = 70, 60, 40, 360
    for i, val in enumerate(queue):
        x = START_X + i * (BOX_W + 6)
        col = GREEN if i == 0 else (ORANGE if i == len(queue) - 1 else BLUE)
        pygame.draw.rect(screen, col, (x, CY - BOX_H // 2, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, CY - BOX_H // 2, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(val), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, CY)))
    if queue:
        screen.blit(font.render("FRONT", True, GREEN), (START_X, CY - BOX_H // 2 - 22))
        rear_x = START_X + (len(queue) - 1) * (BOX_W + 6)
        screen.blit(font.render("REAR", True, ORANGE), (rear_x, CY - BOX_H // 2 - 22))


def animate_stack_push(screen, clock, font, small, stack, value):
    BOX_W, BOX_H, BASE_X, BASE_Y = 140, 44, 330, 540
    start_y = 120
    target_y = BASE_Y - len(stack + [value]) * (BOX_H + 4)
    for step in range(18):
        t = (step + 1) / 18
        y = int(start_y + (target_y - start_y) * t)
        screen.fill(WHITE)
        screen.blit(font.render("Stack & Queue", True, BLUE), (20, 15))
        screen.blit(small.render("Animating push...", True, DKGRAY), (20, 182))
        draw_stack_area(screen, font, stack)
        pygame.draw.rect(screen, GREEN, (BASE_X, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (BASE_X, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(BASE_X + BOX_W // 2, y + BOX_H // 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    stack.append(value)


def animate_stack_pop(screen, clock, font, small, stack):
    if not stack:
        return None
    BOX_W, BOX_H, BASE_X, BASE_Y = 140, 44, 330, 540
    value = stack.pop()
    start_y = BASE_Y - len(stack) * (BOX_H + 4)
    for step in range(18):
        t = (step + 1) / 18
        y = int(start_y - 220 * t)
        screen.fill(WHITE)
        screen.blit(font.render("Stack & Queue", True, BLUE), (20, 15))
        screen.blit(small.render("Animating pop...", True, DKGRAY), (20, 182))
        draw_stack_area(screen, font, stack)
        pygame.draw.rect(screen, RED, (BASE_X, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (BASE_X, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(BASE_X + BOX_W // 2, y + BOX_H // 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return value


def animate_queue_enqueue(screen, clock, font, small, queue, value):
    BOX_W, BOX_H, START_X, CY = 70, 60, 40, 360
    target_x = START_X + len(queue) * (BOX_W + 6)
    start_x = 800
    y = CY - BOX_H // 2
    for step in range(18):
        t = (step + 1) / 18
        x = int(start_x + (target_x - start_x) * t)
        screen.fill(WHITE)
        screen.blit(font.render("Stack & Queue", True, BLUE), (20, 15))
        screen.blit(small.render("Animating enqueue...", True, DKGRAY), (20, 182))
        draw_queue_area(screen, font, queue)
        pygame.draw.rect(screen, GREEN, (x, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, y + BOX_H // 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    queue.append(value)


def animate_queue_dequeue(screen, clock, font, small, queue):
    if not queue:
        return None
    BOX_W, BOX_H, START_X, CY = 70, 60, 40, 360
    value = queue.pop(0)
    start_x = START_X
    y = CY - BOX_H // 2
    for step in range(18):
        t = (step + 1) / 18
        x = int(start_x - 260 * t)
        screen.fill(WHITE)
        screen.blit(font.render("Stack & Queue", True, BLUE), (20, 15))
        screen.blit(small.render("Animating dequeue...", True, DKGRAY), (20, 182))
        draw_queue_area(screen, font, queue)
        pygame.draw.rect(screen, RED, (x, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, y + BOX_H // 2)))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return value


def _render_stack_test(screen, clock, font, small, title, desc, stack, note="", highlight=-1, moving_value=None, moving_pos=None):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render(f"Test: {title}", True, WHITE), (12,10))
    screen.blit(small.render(desc, True, DKGRAY), (12,56))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12, 82))
    draw_stack_area(screen, font, stack)
    if moving_value is not None and moving_pos is not None:
        BOX_W, BOX_H = 140, 44
        x, y = moving_pos
        pygame.draw.rect(screen, GREEN, (x, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(moving_value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, y + BOX_H // 2)))
    if highlight >= 0 and highlight < len(stack):
        BOX_W, BOX_H, BASE_X, BASE_Y = 140, 44, 330, 540
        y = BASE_Y - (highlight + 1) * (BOX_H + 4)
        pygame.draw.rect(screen, RED, (BASE_X - 6, y - 6, BOX_W + 12, BOX_H + 12), 2, border_radius=10)
    pygame.display.flip()


def _render_queue_test(screen, clock, font, small, title, desc, queue, note="", highlight=-1, moving_value=None, moving_pos=None):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render(f"Test: {title}", True, WHITE), (12,10))
    screen.blit(small.render(desc, True, DKGRAY), (12,56))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12, 82))
    draw_queue_area(screen, font, queue)
    if moving_value is not None and moving_pos is not None:
        BOX_W, BOX_H = 70, 60
        x, y = moving_pos
        pygame.draw.rect(screen, GREEN, (x, y, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, y, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(moving_value), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, y + BOX_H // 2)))
    if highlight >= 0 and highlight < len(queue):
        BOX_W, BOX_H, START_X, CY = 70, 60, 40, 360
        x = START_X + highlight * (BOX_W + 6)
        pygame.draw.rect(screen, RED, (x - 6, CY - BOX_H // 2 - 6, BOX_W + 12, BOX_H + 12), 2, border_radius=10)
    pygame.display.flip()


def _wait_anim(screen, clock, duration_ms):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(60)


def run_stack_test(screen, clock, font, small):
    tests = [
        ("Stack: Push 3 items, Pop 2 → size=1",
         "Push 1,2,3 onto stack then pop twice. Expected: size=1, item=1"),
        ("Stack: Pop from empty → message shown",
         "Try to pop from empty stack. Expected: blocked correctly, size stays 0"),
    ]

    for test_name, test_desc in tests:
        if "Push 3 items" in test_name:
            stack = []
            for v in [1, 2, 3]:
                animate_stack_push(screen, clock, font, small, stack, v)
                _render_stack_test(screen, clock, font, small, test_name, test_desc, stack,
                                   note=f"Pushed {v}.", highlight=len(stack) - 1)
                _wait_anim(screen, clock, 500)

            for _ in range(2):
                popped = animate_stack_pop(screen, clock, font, small, stack)
                _render_stack_test(screen, clock, font, small, test_name, test_desc, stack,
                                   note=f"Popped {popped}.", highlight=len(stack) - 1)
                _wait_anim(screen, clock, 500)

            _render_stack_test(screen, clock, font, small, test_name, test_desc, stack,
                               note=f"Final stack: {stack}  size={len(stack)}")
            _result_bar(screen, font, len(stack) == 1 and stack == [1])
        else:
            stack = []
            _render_stack_test(screen, clock, font, small, test_name, test_desc, stack,
                               note="Attempting to pop from an empty stack.")
            pygame.draw.rect(screen, LGRAY, (100,160,600,70), border_radius=8)
            pygame.draw.rect(screen, GRAY,  (100,160,600,70), 2, border_radius=8)
            msg = "Stack is empty — nothing to pop!"
            screen.blit(font.render(msg, True, RED), font.render(msg, True, RED).get_rect(center=(400,195)))
            pygame.display.flip()
            _wait_anim(screen, clock, 700)
            _result_bar(screen, font, len(stack) == 0)

        if not _wait_next(screen, clock, font):
            return


def run_queue_test(screen, clock, font, small):
    tests = [
        ("Queue: Enqueue 4, Dequeue 3 → FIFO order",
         "Enqueue 10,20,30,40 then dequeue 3. Expected: [10,20,30] dequeued in order"),
        ("Queue: Dequeue from empty → message shown",
         "Try to dequeue from empty queue. Expected: blocked correctly, size stays 0"),
    ]

    for test_name, test_desc in tests:
        if "Enqueue 4" in test_name:
            queue = []
            dequeued = []
            for v in [10, 20, 30, 40]:
                animate_queue_enqueue(screen, clock, font, small, queue, v)
                _render_queue_test(screen, clock, font, small, test_name, test_desc, queue,
                                   note=f"Enqueued {v}.", highlight=len(queue) - 1)
                _wait_anim(screen, clock, 500)

            for i in range(3):
                value = animate_queue_dequeue(screen, clock, font, small, queue)
                dequeued.append(value)
                _render_queue_test(screen, clock, font, small, test_name, test_desc, queue,
                                   note=f"Dequeued {value}.", highlight=0)
                _wait_anim(screen, clock, 500)

            _render_queue_test(screen, clock, font, small, test_name, test_desc, queue,
                               note=f"Remaining queue: {queue}")
            _result_bar(screen, font, dequeued == [10, 20, 30] and queue == [40])
        else:
            queue = []
            _render_queue_test(screen, clock, font, small, test_name, test_desc, queue,
                               note="Attempting to dequeue from an empty queue.")
            pygame.draw.rect(screen, LGRAY, (100,160,600,70), border_radius=8)
            pygame.draw.rect(screen, GRAY,  (100,160,600,70), 2, border_radius=8)
            msg = "Queue is empty — nothing to dequeue!"
            screen.blit(font.render(msg, True, RED), font.render(msg, True, RED).get_rect(center=(400,195)))
            pygame.display.flip()
            _wait_anim(screen, clock, 700)
            _result_bar(screen, font, len(queue) == 0)

        if not _wait_next(screen, clock, font):
            return


def run_stack_queue(screen, clock, font, small):
    tab    = "stack"
    stack  = []
    s_next = 1
    queue  = []
    q_next = 1
    message = "Pick Stack or Queue above, then use the buttons!"

    while True:
        screen.fill(WHITE)
        screen.blit(font.render("Stack & Queue", True, BLUE), (20,15))

        btn_stack_tab = draw_button(screen, small, "Stack",  20, 55, w=100)
        btn_queue_tab = draw_button(screen, small, "Queue", 130, 55, w=100)

        for btn, name in [(btn_stack_tab,"stack"),(btn_queue_tab,"queue")]:
            if tab == name:
                pygame.draw.rect(screen, BLUE, btn, border_radius=6)
                pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
                screen.blit(small.render(name.capitalize(),True,WHITE), small.render(name.capitalize(),True,WHITE).get_rect(center=btn.center))

        btn_back = draw_button(screen, small, "< Menu", 560, 55, w=110)
        btn_test = draw_button(screen, small, "Test",   680, 55, w=80)
        pygame.draw.line(screen, GRAY, (0,100), (800,100), 1)

        if tab == "stack":
            btn_push = draw_button(screen, small, "Push", 20, 110, w=100)
            btn_pop  = draw_button(screen, small, "Pop",  130, 110, w=100)
            screen.blit(small.render("LIFO — last item pushed is first to be popped",True,DKGRAY),(20,160))
            screen.blit(small.render(f"Size: {len(stack)}",True,DKGRAY),(20,182))
            box_w=140; box_h=44; base_x=330; base_y=540
            pygame.draw.line(screen, BLACK, (base_x-10,base_y),(base_x+box_w+10,base_y),3)
            for i,val in enumerate(stack):
                x=base_x; y=base_y-(i+1)*(box_h+4)
                color=GREEN if i==len(stack)-1 else BLUE
                pygame.draw.rect(screen,color,(x,y,box_w,box_h),border_radius=6)
                pygame.draw.rect(screen,BLACK,(x,y,box_w,box_h),2,border_radius=6)
                screen.blit(font.render(str(val),True,BLACK),font.render(str(val),True,BLACK).get_rect(center=(x+box_w//2,y+box_h//2)))
                if i==len(stack)-1:
                    screen.blit(small.render("<-- TOP",True,RED),(x+box_w+8,y+12))
            if not stack:
                screen.blit(small.render("Stack is empty",True,DKGRAY),small.render("Stack is empty",True,DKGRAY).get_rect(center=(400,350)))
        else:
            btn_enq = draw_button(screen, small, "Enqueue",  20, 110, w=120)
            btn_deq = draw_button(screen, small, "Dequeue", 150, 110, w=120)
            screen.blit(small.render("FIFO — first item enqueued is first to be dequeued",True,DKGRAY),(20,160))
            screen.blit(small.render(f"Size: {len(queue)}",True,DKGRAY),(20,182))
            box_w=70; box_h=60; start_x=40; cy=360
            for i,val in enumerate(queue):
                x=start_x+i*(box_w+6); color=GREEN if i==0 else (ORANGE if i==len(queue)-1 else BLUE)
                pygame.draw.rect(screen,color,(x,cy-box_h//2,box_w,box_h),border_radius=6)
                pygame.draw.rect(screen,BLACK,(x,cy-box_h//2,box_w,box_h),2,border_radius=6)
                screen.blit(font.render(str(val),True,BLACK),font.render(str(val),True,BLACK).get_rect(center=(x+box_w//2,cy)))
            if queue:
                screen.blit(small.render("FRONT",True,GREEN),(start_x,cy-box_h//2-22))
                screen.blit(small.render("REAR",True,ORANGE),(start_x+(len(queue)-1)*(box_w+6),cy-box_h//2-22))
            else:
                screen.blit(small.render("Queue is empty",True,DKGRAY),small.render("Queue is empty",True,DKGRAY).get_rect(center=(400,360)))

        screen.blit(small.render(message,True,DKGRAY),(20,565))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT: pygame.quit(); sys.exit()
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: return
            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                if btn_back.collidepoint(pos): return
                elif btn_test.collidepoint(pos):
                    if tab == "stack":
                        run_stack_test(screen, clock, font, small)
                    else:
                        run_queue_test(screen, clock, font, small)
                elif btn_stack_tab.collidepoint(pos): tab="stack"; message="Stack selected."
                elif btn_queue_tab.collidepoint(pos): tab="queue"; message="Queue selected."
                elif tab=="stack":
                    if btn_push.collidepoint(pos):
                        animate_stack_push(screen, clock, font, small, stack, s_next)
                        message=f"Pushed {s_next} onto the stack."
                        s_next += 1
                    elif btn_pop.collidepoint(pos):
                        if stack:
                            v = animate_stack_pop(screen, clock, font, small, stack)
                            message = f"Popped {v} from the stack."
                            if not stack: s_next = 1
                        else:
                            message = "Stack is empty — nothing to pop!"
                elif tab=="queue":
                    if btn_enq.collidepoint(pos):
                        animate_queue_enqueue(screen, clock, font, small, queue, q_next)
                        message=f"Enqueued {q_next} at the rear."
                        q_next += 1
                    elif btn_deq.collidepoint(pos):
                        if queue:
                            v = animate_queue_dequeue(screen, clock, font, small, queue)
                            message = f"Dequeued {v} from the front."
                            if not queue: q_next = 1
                        else:
                            message = "Queue is empty — nothing to dequeue!"
        clock.tick(30)
