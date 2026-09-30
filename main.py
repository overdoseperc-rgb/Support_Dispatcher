"""Диспетчер заявок службы поддержки. Python 3.10+, без зависимостей."""
from dataclasses import dataclass
from collections import deque


@dataclass(frozen=True)
class Request:
    id: int
    title: str
    priority: int


@dataclass
class TreeNode:
    request: Request
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None


# Исходные данные документа, строго в порядке вставки.
INITIAL_REQUESTS = (
    Request(50, "Ошибка оплаты", 9),
    Request(30, "Сброс пароля", 4),
    Request(70, "Интеграция API", 13),
    Request(20, "Изменение профиля", 2),
    Request(40, "Ошибка отчёта", 7),
    Request(60, "Настройка уведомлений", 11),
    Request(80, "Сбой сервера", 15),
    Request(10, "Удаление аккаунта", 1),
    Request(25, "Проблема входа", 3),
    Request(35, "Экспорт данных", 5),
    Request(45, "Возврат платежа", 8),
    Request(55, "Подключение тарифа", 10),
    Request(65, "Ошибка синхронизации", 12),
    Request(75, "Недоступна база данных", 14),
    Request(90, "Обновление реквизитов", 6),
)


def insert(root, request):
    """O(h) времени и O(h) стека; дубликат оставляет прежнюю заявку."""
    if root is None:
        return TreeNode(request)
    if request.id < root.request.id:
        root.left = insert(root.left, request)
    elif request.id > root.request.id:
        root.right = insert(root.right, request)
    return root


def _traverse(root, order, result):
    if root is None:
        return
    if order == "pre":
        result.append(root.request)
    _traverse(root.left, order, result)
    if order == "in":
        result.append(root.request)
    _traverse(root.right, order, result)
    if order == "post":
        result.append(root.request)


def preorder(root):
    result = []
    _traverse(root, "pre", result)
    return result


def inorder(root):
    result = []
    _traverse(root, "in", result)
    return result


def postorder(root):
    result = []
    _traverse(root, "post", result)
    return result


def levelorder(root):
    result = []
    queue = deque([root]) if root else deque()
    while queue:
        node = queue.popleft()
        result.append(node.request)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result


def search(root, request_id):
    path = []
    while root:
        path.append(root.request.id)
        if request_id == root.request.id:
            return root.request, path
        root = root.left if request_id < root.request.id else root.right
    return None, path


def find_min(root):
    if root is None:
        return None
    while root.left:
        root = root.left
    return root.request


def find_max(root):
    if root is None:
        return None
    while root.right:
        root = root.right
    return root.request


def count_nodes(root):
    return 0 if root is None else 1 + count_nodes(root.left) + count_nodes(root.right)


def count_leaves(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return count_leaves(root.left) + count_leaves(root.right)


def height(root):
    return 0 if root is None else 1 + max(height(root.left), height(root.right))


def get_depth(root, request_id):
    """Корень имеет глубину 0; отсутствующий узел — None."""
    depth = 0
    while root:
        if root.request.id == request_id:
            return depth
        root = root.left if request_id < root.request.id else root.right
        depth += 1
    return None


def validate_bst(root):
    def check(node, lower, upper):
        if node is None:
            return True
        key = node.request.id
        if lower is not None and key <= lower:
            return False
        if upper is not None and key >= upper:
            return False
        return check(node.left, lower, key) and check(node.right, key, upper)
    return check(root, None, None)


def delete(root, request_id):
    if root is None:
        return None
    if request_id < root.request.id:
        root.left = delete(root.left, request_id)
    elif request_id > root.request.id:
        root.right = delete(root.right, request_id)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        # Симметричный преемник: минимум правого поддерева.
        # Переносим всю заявку (id, title, priority).
        successor = find_min(root.right)
        root.request = successor
        root.right = delete(root.right, successor.id)
    return root


def request_key(request):
    return request.priority, request.id


def sift_down(data, heap_size, index):
    """Итеративное просеивание: O(log n) времени, O(1) памяти."""
    while 2 * index + 1 < heap_size:
        child = 2 * index + 1
        if child + 1 < heap_size and request_key(data[child + 1]) > request_key(data[child]):
            child += 1
        if request_key(data[index]) >= request_key(data[child]):
            break
        data[index], data[child] = data[child], data[index]
        index = child


def build_max_heap(data):
    for index in range(len(data) // 2 - 1, -1, -1):
        sift_down(data, len(data), index)


def is_max_heap(data):
    for child in range(1, len(data)):
        if request_key(data[(child - 1) // 2]) < request_key(data[child]):
            return False
    return True


def heap_sort(data):
    """По возрастанию (priority, id), in-place, O(n log n)/O(1)."""
    build_max_heap(data)
    for end in range(len(data) - 1, 0, -1):
        data[0], data[end] = data[end], data[0]
        sift_down(data, end, 0)


def make_initial_tree():
    root = None
    for request in INITIAL_REQUESTS:
        root = insert(root, request)
    return root


def ids(data):
    return [request.id for request in data]


def format_requests(data):
    return ", ".join(f"{r.id}({r.priority})" for r in data)


def print_tree_levels(root):
    queue = deque([root]) if root else deque()
    level = 0
    while queue:
        row = []
        for _ in range(len(queue)):
            node = queue.popleft()
            row.append(node.request)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        print(f"Уровень {level}: {format_requests(row)}")
        level += 1


def main():
    root = make_initial_tree()
    print("Этап 1. Исходное дерево")
    print_tree_levels(root)
    print("\nЭтап 2. Обходы")
    controls = [
        ("Прямой", preorder, [50,30,20,10,25,40,35,45,70,60,55,65,80,75,90]),
        ("Симметричный", inorder, [10,20,25,30,35,40,45,50,55,60,65,70,75,80,90]),
        ("Обратный", postorder, [10,25,20,35,45,40,30,55,65,60,75,90,80,70,50]),
        ("Уровневый", levelorder, [50,30,70,20,40,60,80,10,25,35,45,55,65,75,90]),
    ]
    for label, traversal, expected in controls:
        actual = ids(traversal(root))
        assert actual == expected
        print(f"{label}: {actual}")
    print("\nЭтап 3. Поиск и характеристики")
    for key in (65, 99):
        found, path = search(root, key)
        print(f"Поиск {key}: {found}; путь: {path}")
    assert search(root, 65) == (INITIAL_REQUESTS[12], [50,70,60,65])
    assert search(root, 99) == (None, [50,70,80,90])
    actual = (count_nodes(root), count_leaves(root), height(root),
              find_min(root).id, find_max(root).id, get_depth(root,65))
    assert actual == (15,8,4,10,90,3)
    assert validate_bst(root)
    print("Узлы, листья, высота, min, max, глубина 65:", actual)
    print("validate_bst:", validate_bst(root))
    print("\nЭтап 4. Изменения")
    operations = [
        ("Добавить 37", "insert", Request(37,"Утечка данных",16), 16, 5),
        ("Добавить дубликат 50 — отклонён", "insert", Request(50,"Дубликат",99),16,5),
        ("Удалить лист 10", "delete", 10,15,5),
        ("Удалить узел 35 с одним потомком", "delete",35,14,4),
        ("Удалить узел 70 с двумя потомками", "delete",70,13,4),
        ("Удалить отсутствующий 999", "delete",999,13,4),
    ]
    for label, operation, value, size, tree_height in operations:
        root = insert(root,value) if operation == "insert" else delete(root,value)
        assert count_nodes(root) == size and height(root) == tree_height
        assert validate_bst(root)
        print(label)
        print("Симметричный обход:", ids(inorder(root)))
        print(f"Узлы: {size}; высота: {tree_height}; validate_bst: {validate_bst(root)}")
    assert search(root,50)[0] == INITIAL_REQUESTS[0]
    assert ids(inorder(root)) == [20,25,30,37,40,45,50,55,60,65,75,80,90]
    print("\nЭтап 5. Максимальная куча")
    data = inorder(root)
    print("Исходный массив:", format_requests(data))
    build_max_heap(data)
    assert ids(data) == [37,75,80,60,65,45,50,55,25,20,40,30,90]
    assert is_max_heap(data)
    print("Массив кучи:", format_requests(data))
    start, width, level = 0, 1, 0
    while start < len(data):
        print(f"Уровень {level}: {format_requests(data[start:start+width])}")
        start += width
        width *= 2
        level += 1
    print("is_max_heap:", is_max_heap(data))
    print("\nЭтап 6. Сортировка кучей")
    heap_sort(data)
    assert ids(data) == [20,25,30,90,40,45,50,55,60,65,75,80,37]
    print("По возрастанию (priority, id):", format_requests(data))
    for request in data:
        print(f"{request.id}: {request.title}; приоритет {request.priority}")
    print("\nВсе контрольные результаты документа совпали.")


if __name__ == "__main__":
    main()
