import pygame
import sys

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
GREEN  = (144, 238, 144)
YELLOW = (255, 220, 80)
RED    = (255, 100, 100)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)

class Node:
    def __init__(self, val):
        self.val  = val
        self.next = None

linked_list_head = None
next_val = 1

def ll_insert_head(head, val):
    node = Node(val)
    node.next = head
    return node

def ll_insert_tail(head, val):
    node = Node(val)
    if head is None:
        return node
    cur = head
    while cur.next:
        cur = cur.next
    cur.next = node
    return head

def ll_delete_head(head):
    if head is None:
        return None
    return head.next

def ll_reverse(head):
    prev = None
    cur  = head
    while cur:
        nxt      = cur.next
        cur.next = prev
        prev     = cur
        cur      = nxt
    return prev

def ll_to_list(head):
    result = []
    cur = head
    while cur:
        result.append(cur.val)
        cur = cur.next
    return result


def _wait_next(screen, clock, font, label="Next →"):
    btn = pygame.Rect(630, 548, 160, 36)
    while True:
        pygame.draw.rect(screen, (180,230,180), btn, border_radius=6)
        pygame.draw.rect(screen, BLACK, btn, 2, border_radius=6)
        lbl = font.render(label, True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=btn.center))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: return False
            if event.type == pygame.MOUSEBUTTONDOWN and btn.collidepoint(event.pos): return True
        clock.tick(30)


def _result_bar(screen, font, passed):
    col = (60,200,100) if passed else (220,60,60)
    pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
    screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, (255,255,255)),
                font.render("RESULT: PASS",True,(255,255,255)).get_rect(center=(400,527)))


def _draw_linked_nodes(screen, font, head, highlight=-1, moving_node=None, moving_pos=None):
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    nodes = ll_to_list(head)
    for i, val in enumerate(nodes):
        x = SX + i * (BOX_W + 34)
        color = YELLOW if i == highlight else (GREEN if i == 0 else BLUE)
        pygame.draw.rect(screen, color, (x, CY - BOX_H // 2, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (x, CY - BOX_H // 2, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(val), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(x + BOX_W // 2, CY)))
        if i == 0:
            screen.blit(font.render("HEAD", True, GREEN), (x + 6, CY - BOX_H // 2 - 20))
        if i < len(nodes) - 1:
            ax1 = x + BOX_W
            ax2 = x + BOX_W + 34
            pygame.draw.line(screen, BLACK, (ax1, CY), (ax2, CY), 2)
            pygame.draw.polygon(screen, BLACK, [(ax2, CY), (ax2 - 8, CY - 5), (ax2 - 8, CY + 5)])
        else:
            if nodes:
                screen.blit(font.render("None", True, DKGRAY), (x + BOX_W + 8, CY - 10))
    if moving_node is not None and moving_pos is not None:
        mx, my = moving_pos
        pygame.draw.rect(screen, YELLOW, (mx, my, BOX_W, BOX_H), border_radius=6)
        pygame.draw.rect(screen, BLACK, (mx, my, BOX_W, BOX_H), 2, border_radius=6)
        lbl = font.render(str(moving_node), True, BLACK)
        screen.blit(lbl, lbl.get_rect(center=(mx + BOX_W // 2, my + BOX_H // 2)))


def animate_insert_head(screen, clock, font, small, head, value):
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    start_y = 80
    target_y = CY - BOX_H // 2
    for step in range(18):
        t = (step + 1) / 18
        y = int(start_y + (target_y - start_y) * t)
        screen.fill(WHITE)
        screen.blit(font.render("Linked List", True, BLUE), (20, 15))
        screen.blit(small.render("Animating insert at head...", True, DKGRAY), (20, 120))
        _draw_linked_nodes(screen, font, head)
        _draw_linked_nodes(screen, font, None, moving_node=value, moving_pos=(SX, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return ll_insert_head(head, value)


def animate_insert_tail(screen, clock, font, small, head, value):
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    nodes = ll_to_list(head)
    target_x = SX + len(nodes) * (BOX_W + 34)
    start_y = 80
    for step in range(18):
        t = (step + 1) / 18
        y = int(start_y + (CY - BOX_H // 2 - start_y) * t)
        x = int(target_x + 200 * (1 - t))
        screen.fill(WHITE)
        screen.blit(font.render("Linked List", True, BLUE), (20, 15))
        screen.blit(small.render("Animating insert at tail...", True, DKGRAY), (20, 120))
        _draw_linked_nodes(screen, font, head)
        _draw_linked_nodes(screen, font, None, moving_node=value, moving_pos=(x, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return ll_insert_tail(head, value)


def animate_delete_head(screen, clock, font, small, head):
    if head is None:
        return head, None
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    value = head.val
    for step in range(18):
        t = (step + 1) / 18
        x = int(SX - 260 * t)
        screen.fill(WHITE)
        screen.blit(font.render("Linked List", True, BLUE), (20, 15))
        screen.blit(small.render("Animating delete head...", True, DKGRAY), (20, 120))
        _draw_linked_nodes(screen, font, head.next)
        _draw_linked_nodes(screen, font, None, moving_node=value, moving_pos=(x, CY - BOX_H // 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return ll_delete_head(head), value


def animate_reverse(screen, clock, font, small, head):
    nodes = ll_to_list(head)
    if len(nodes) <= 1:
        return head
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    for i in range(len(nodes)):
        screen.fill(WHITE)
        screen.blit(font.render("Linked List", True, BLUE), (20, 15))
        screen.blit(small.render("Reversing list...", True, DKGRAY), (20, 120))
        _draw_linked_nodes(screen, font, head, highlight=i)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(5)
    head = ll_reverse(head)
    for step in range(18):
        t = (step + 1) / 18
        screen.fill(WHITE)
        screen.blit(font.render("Linked List", True, BLUE), (20, 15))
        screen.blit(small.render("Reversed!", True, DKGRAY), (20, 120))
        _draw_linked_nodes(screen, font, head)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
        clock.tick(60)
    return head


def _render_test_screen(screen, clock, font, small, test_name, test_desc, head, note="", highlight=-1, moving_node=None, moving_pos=None):
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0,0,800,48))
    screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
    screen.blit(small.render(test_desc, True, DKGRAY), (12,56))
    pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
    if note:
        screen.blit(small.render(note, True, DKGRAY), (12, 82))
    _draw_linked_nodes(screen, font, head, highlight=highlight, moving_node=moving_node, moving_pos=moving_pos)
    pygame.display.flip()


def _wait_anim(screen, clock, duration_ms):
    start = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(60)


def _animate_insert_at_position(screen, clock, font, small, head, value, pos_index):
    BOX_W, BOX_H, SX, CY = 70, 48, 30, 300
    target_x = SX + pos_index * (BOX_W + 34)
    start_x = target_x + 220
    y = CY - BOX_H // 2
    for step in range(18):
        t = (step + 1) / 18
        x = int(start_x + (target_x - start_x) * t)
        _render_test_screen(screen, clock, font, small,
                          "Linked List: Insert 10 at position 2",
                          "Animating insertion at index 2.", head,
                          note=f"Moving new node toward index {pos_index}",
                          highlight=pos_index - 1,
                          moving_node=value, moving_pos=(x, y))
        clock.tick(60)
    if pos_index == 0:
        return ll_insert_head(head, value)
    new_node = Node(value)
    cur = head
    for _ in range(pos_index - 1):
        if cur is None:
            break
        cur = cur.next
    if cur is not None:
        new_node.next = cur.next
        cur.next = new_node
    return head


def run_linkedlist_test(screen, clock, font, small):
    tests = [
        ("Linked List: Insert 10 at position 2",
         "Build [1,2,4] then insert 10 at index 2. Expected: [1,2,10,4]"),
        ("Linked List: Reverse [3→2→1] → [1→2→3]",
         "Insert head 1,2,3 (makes [3,2,1]) then reverse. Expected: [1,2,3]"),
    ]

    for test_name, test_desc in tests:
        if "position" in test_name:
            head = None
            for v in [1, 2, 4]:
                head = animate_insert_tail(screen, clock, font, small, head, v)
                _render_test_screen(screen, clock, font, small, test_name, test_desc, head,
                                  note=f"Inserted {v} at tail.")
                _wait_anim(screen, clock, 400)

            for idx in range(2):
                _render_test_screen(screen, clock, font, small, test_name, test_desc, head,
                                  note=f"Traversing node index {idx}", highlight=idx)
                _wait_anim(screen, clock, 400)

            head = _animate_insert_at_position(screen, clock, font, small, head, 10, 2)
            lst = ll_to_list(head)
            _render_test_screen(screen, clock, font, small, test_name, test_desc, head,
                              note=f"Final list: {lst}", highlight=2)
            _result_bar(screen, font, lst == [1, 2, 10, 4])

        else:
            head = None
            for v in [1, 2, 3]:
                head = animate_insert_head(screen, clock, font, small, head, v)
                _render_test_screen(screen, clock, font, small, test_name, test_desc, head,
                                  note=f"Inserted {v} at head.", highlight=0)
                _wait_anim(screen, clock, 400)

            before = ll_to_list(head)
            head = animate_reverse(screen, clock, font, small, head)
            after = ll_to_list(head)
            _render_test_screen(screen, clock, font, small, test_name, test_desc, head,
                              note=f"Reversed list: {after}")
            _result_bar(screen, font, before == [3, 2, 1] and after == [1, 2, 3])

        if not _wait_next(screen, clock, font):
            return


def draw_button(screen, font, text, x, y, w=130, h=40):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect

def run_linkedlist(screen, clock, font, small):
    global linked_list_head, next_val
    linked_list_head = None
    next_val = 1
    message = "Use buttons to build the linked list!"

    while True:
        screen.fill(WHITE)

        title = font.render("Linked List", True, BLUE)
        screen.blit(title, (20, 15))

        btn_head = draw_button(screen, small, "Insert Head",  20, 60, w=130)
        btn_tail = draw_button(screen, small, "Insert Tail", 160, 60, w=120)
        btn_del  = draw_button(screen, small, "Delete Head", 290, 60, w=130)
        btn_rev  = draw_button(screen, small, "Reverse",     430, 60, w=100)
        btn_back = draw_button(screen, small, "< Menu",      560, 60, w=110)
        btn_test = draw_button(screen, small, "Test",        680, 60, w=80)

        nodes = ll_to_list(linked_list_head)
        box_w  = 70
        box_h  = 50
        start_x = 40
        cy = 300

        for i, val in enumerate(nodes):
            x = start_x + i * (box_w + 40)
            color = GREEN if i == 0 else BLUE
            pygame.draw.rect(screen, color, (x, cy - box_h//2, box_w, box_h), border_radius=6)
            pygame.draw.rect(screen, BLACK, (x, cy - box_h//2, box_w, box_h), 2, border_radius=6)
            lbl = font.render(str(val), True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=(x + box_w//2, cy)))

            if i == 0:
                head_lbl = small.render("HEAD", True, GREEN)
                screen.blit(head_lbl, (x + 10, cy - box_h//2 - 22))

            if i < len(nodes) - 1:
                ax1 = x + box_w
                ax2 = x + box_w + 40
                pygame.draw.line(screen, BLACK, (ax1, cy), (ax2, cy), 2)
                pygame.draw.polygon(screen, BLACK, [
                    (ax2, cy),
                    (ax2 - 10, cy - 6),
                    (ax2 - 10, cy + 6)
                ])
            else:
                none_lbl = small.render("None", True, DKGRAY)
                screen.blit(none_lbl, (x + box_w + 8, cy - 10))

        if not nodes:
            empty = font.render("List is empty — press Insert Head or Tail!", True, DKGRAY)
            screen.blit(empty, empty.get_rect(center=(400, 300)))

        size_lbl = small.render(f"Length: {len(nodes)}", True, DKGRAY)
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
                    run_linkedlist_test(screen, clock, font, small)
                elif btn_head.collidepoint(event.pos):
                    linked_list_head = animate_insert_head(screen, clock, font, small, linked_list_head, next_val)
                    message = f"Inserted {next_val} at head."
                    next_val += 1
                elif btn_tail.collidepoint(event.pos):
                    linked_list_head = animate_insert_tail(screen, clock, font, small, linked_list_head, next_val)
                    message = f"Inserted {next_val} at tail."
                    next_val += 1
                elif btn_del.collidepoint(event.pos):
                    if linked_list_head:
                        linked_list_head, v = animate_delete_head(screen, clock, font, small, linked_list_head)
                        message = f"Deleted head ({v})."
                        if linked_list_head is None:
                            next_val = 1
                    else:
                        message = "List is empty!"
                elif btn_rev.collidepoint(event.pos):
                    linked_list_head = animate_reverse(screen, clock, font, small, linked_list_head)
                    message = "List reversed!"

        clock.tick(30)