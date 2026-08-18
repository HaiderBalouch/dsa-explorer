import pygame
import sys

WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
BLUE   = (100, 149, 237)
YELLOW = (255, 220, 80)
GRAY   = (200, 200, 200)
DKGRAY = (100, 100, 100)

class Node:
    def __init__(self, val):
        self.val   = val
        self.left  = None
        self.right = None


def insert(root, val):
    if root is None:
        return Node(val)
    if val < root.val:
        root.left  = insert(root.left,  val)
    elif val > root.val:
        root.right = insert(root.right, val)
    return root


def inorder(root):
    if root is None: return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root):
    if root is None: return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root):
    if root is None: return []
    return postorder(root.left) + postorder(root.right) + [root.val]


def get_positions(root, depth=0, lo=0.0, hi=1.0, positions=None):
    if positions is None:
        positions = {}
    if root is None:
        return positions
    mid = (lo + hi) / 2
    x   = int(80 + mid * 640)
    y   = 160 + depth * 80
    positions[root.val] = (x, y)
    get_positions(root.left,  depth + 1, lo,  mid, positions)
    get_positions(root.right, depth + 1, mid, hi,  positions)
    return positions


def _wait_next_bst(screen, clock, font, label="Next →"):
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


def run_bst_test(screen, clock, font, small):
    tests = [
        ("BST: Insert [50,30,70] → Inorder = [30,50,70]",
         "Insert values one by one, then check inorder traversal order."),
        ("BST: Duplicate 50 inserted twice → only one node",
         "Insert 50 twice. Expected: inorder = [50], duplicate silently ignored."),
    ]

    for test_name, test_desc in tests:
        root = None
        values = [50,30,70] if "Inorder" in test_name else [50,50]

        for step_val in values:
            root = insert(root, step_val)
            positions = get_positions(root)
            screen.fill(WHITE)
            pygame.draw.rect(screen, BLUE, (0,0,800,48))
            screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
            screen.blit(small.render(test_desc, True, DKGRAY), (12,56))
            pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
            screen.blit(small.render(f"Inserted {step_val}", True, DKGRAY), (12,82))

            def draw_edges(node):
                if node is None: return
                if node.left:
                    pygame.draw.line(screen, DKGRAY, positions[node.val], positions[node.left.val], 2)
                    draw_edges(node.left)
                if node.right:
                    pygame.draw.line(screen, DKGRAY, positions[node.val], positions[node.right.val], 2)
                    draw_edges(node.right)

            draw_edges(root)
            for val,(x,y) in positions.items():
                pygame.draw.circle(screen, BLUE, (x,y), 26)
                pygame.draw.circle(screen, BLACK, (x,y), 26, 2)
                screen.blit(font.render(str(val),True,WHITE), font.render(str(val),True,WHITE).get_rect(center=(x,y)))

            pygame.display.flip()
            pygame.time.delay(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

        traversal = inorder(root)
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (0,0,800,48))
        screen.blit(font.render(f"Test: {test_name}", True, WHITE), (12,10))
        screen.blit(small.render(test_desc, True, DKGRAY), (12,56))
        pygame.draw.line(screen, GRAY, (0,76), (800,76), 1)
        screen.blit(small.render(f"Final inorder traversal: {traversal}", True, DKGRAY), (12,82))
        positions = get_positions(root)

        def draw_edges2(node):
            if node is None: return
            if node.left:
                pygame.draw.line(screen, DKGRAY, positions[node.val], positions[node.left.val], 2)
                draw_edges2(node.left)
            if node.right:
                pygame.draw.line(screen, DKGRAY, positions[node.val], positions[node.right.val], 2)
                draw_edges2(node.right)

        draw_edges2(root)
        for val,(x,y) in positions.items():
            pygame.draw.circle(screen, BLUE, (x,y), 26)
            pygame.draw.circle(screen, BLACK, (x,y), 26, 2)
            screen.blit(font.render(str(val),True,WHITE), font.render(str(val),True,WHITE).get_rect(center=(x,y)))

        passed = (traversal == [30,50,70]) if "Inorder" in test_name else (traversal == [50])
        col = (60,200,100) if passed else (220,60,60)
        pygame.draw.rect(screen, col, (10,510,780,34), border_radius=6)
        screen.blit(font.render("RESULT: PASS" if passed else "RESULT: FAIL", True, WHITE),
                    font.render("RESULT: PASS",True,WHITE).get_rect(center=(400,527)))
        if not _wait_next_bst(screen, clock, font): return

def draw_button(screen, font, text, x, y, w=120, h=38):
    rect = pygame.Rect(x, y, w, h)
    mx, my = pygame.mouse.get_pos()
    col = DKGRAY if rect.collidepoint(mx, my) else GRAY
    pygame.draw.rect(screen, col, rect, border_radius=6)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=6)
    lbl = font.render(text, True, BLACK)
    screen.blit(lbl, lbl.get_rect(center=rect.center))
    return rect

def run_bst(screen, clock, font, small):
    root    = None
    message = "Insert numbers to build the BST."
    import random
    vals_to_insert = [50, 30, 70, 20, 40, 60, 80]

    while True:
        screen.fill(WHITE)

        title = font.render("Binary Search Tree", True, BLUE)
        screen.blit(title, (20, 15))

        btn_insert   = draw_button(screen, small, "Insert",    20,  60, w=100)
        btn_inorder  = draw_button(screen, small, "Inorder",  130,  60, w=110)
        btn_pre      = draw_button(screen, small, "Preorder", 250,  60, w=110)
        btn_post     = draw_button(screen, small, "Postorder",370,  60, w=120)
        btn_clear    = draw_button(screen, small, "Clear",    500,  60, w=80)
        btn_back     = draw_button(screen, small, "< Menu",   590,  60, w=100)
        btn_test     = draw_button(screen, small, "Test",     700,  60, w=70)

        if root:
            positions = get_positions(root)

            def draw_edges(node):
                if node is None:
                    return
                if node.left and node.left.val in positions:
                    pygame.draw.line(screen, DKGRAY,
                                     positions[node.val], positions[node.left.val], 2)
                    draw_edges(node.left)
                if node.right and node.right.val in positions:
                    pygame.draw.line(screen, DKGRAY,
                                     positions[node.val], positions[node.right.val], 2)
                    draw_edges(node.right)

            draw_edges(root)

            for val, (x, y) in positions.items():
                pygame.draw.circle(screen, BLUE,   (x, y), 24)
                pygame.draw.circle(screen, BLACK,  (x, y), 24, 2)
                lbl = font.render(str(val), True, WHITE)
                screen.blit(lbl, lbl.get_rect(center=(x, y)))
        else:
            empty = font.render("Tree is empty — press Insert!", True, DKGRAY)
            screen.blit(empty, empty.get_rect(center=(400, 350)))

        msg = small.render(message, True, DKGRAY)
        screen.blit(msg, (20, 560))

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
                    run_bst_test(screen, clock, font, small)
                elif btn_insert.collidepoint(event.pos):
                    v    = random.randint(1, 99)
                    root = insert(root, v)
                    layout_mode = "tree"
                    current_order = []
                    message = f"Inserted {v}"
                elif btn_inorder.collidepoint(event.pos):
                    message = f"Inorder: {inorder(root)}"
                elif btn_pre.collidepoint(event.pos):
                    message = f"Preorder: {preorder(root)}"
                elif btn_post.collidepoint(event.pos):
                    message = f"Postorder: {postorder(root)}"
                elif btn_clear.collidepoint(event.pos):
                    root = None
                    message = "Tree cleared."

        clock.tick(30)
