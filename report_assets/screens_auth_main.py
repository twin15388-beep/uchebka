import sys
sys.path.insert(0, "/home/user/uchebka/report_assets")
from ui_lib import *

OUT = "/home/user/uchebka/report_assets/"

# ================= АВТОРИЗАЦИЯ =================
w = Win(480, 460, "Кофейня «Зёрнышко» — авторизация")
w.rect(0, 32, 480, 84, fc=BROWN, ec=BROWN, lw=0)
w.text(240, 66, "Кофейня «Зёрнышко»", size=24, color="#FFFFFF", bold=True, ha="center")
w.text(240, 96, "информационная система автоматизации работы кофейни",
       size=11, color="#F3E9DF", ha="center")

w.rect(32, 144, 416, 292, fc="#FFFFFF", ec=LIGHT, lw=1.2, r=8)
w.text(240, 180, "Авторизация", size=19, color=DARK, bold=True, ha="center")
w.text(60, 204, "Логин", size=13, color=GREY)
w.textbox(60, 212, 360, 36, "", size=14)
w.text(60, 268, "Пароль", size=13, color=GREY)
w.textbox(60, 276, 360, 36, "", size=14)
w.button(60, 324, 360, 42, "Войти", size=15)
w.button(60, 376, 360, 36, "Выход", primary=False, size=14)
w.save(OUT + "shot_auth.png")

# ================= АВТОРИЗАЦИЯ С ОШИБКОЙ =================
w = Win(480, 460, "Кофейня «Зёрнышко» — авторизация")
w.rect(0, 32, 480, 84, fc=BROWN, ec=BROWN, lw=0)
w.text(240, 66, "Кофейня «Зёрнышко»", size=24, color="#FFFFFF", bold=True, ha="center")
w.text(240, 96, "информационная система автоматизации работы кофейни",
       size=11, color="#F3E9DF", ha="center")
w.rect(32, 144, 416, 292, fc="#FFFFFF", ec=LIGHT, lw=1.2, r=8)
w.text(240, 180, "Авторизация", size=19, color=DARK, bold=True, ha="center")
w.text(60, 204, "Логин", size=13, color=GREY)
w.textbox(60, 212, 360, 36, "barista", size=14)
w.text(60, 268, "Пароль", size=13, color=GREY)
w.textbox(60, 276, 360, 36, "••••••", size=14)
w.button(60, 324, 360, 42, "Войти", size=15)
w.button(60, 376, 360, 36, "Выход", primary=False, size=14)

# затемнение + диалог
w.rect(0, 0, 480, 460, fc="#000000", ec="#000000", lw=0, alpha=0.10, z=10)
w.rect(60, 306, 360, 128, fc="#F3F3F3", ec="#BDBDBD", lw=1.2, r=8, z=11)
w.rect(60, 306, 360, 28, fc="#E8E8E8", ec="#E8E8E8", lw=0, z=12)
w.text(74, 320, "Ошибка входа", size=12, color="#1F1F1F", z=15)
w.ax.add_patch(Circle((94, 366), 11, facecolor="#C62828", edgecolor="#C62828", zorder=14))
w.text(94, 366, "!", size=14, color="#FFFFFF", bold=True, ha="center", z=15)
w.text(118, 366, "Неверный логин или пароль.", size=13, color="#212121", z=15)
w.button(346, 392, 64, 30, "OK", size=13, z=14)
w.save(OUT + "shot_auth_error.png")

# ================= ГЛАВНОЕ МЕНЮ =================
w = Win(980, 580, "Кофейня «Зёрнышко» — главное меню")
w.rect(0, 32, 980, 92, fc=BROWN, ec=BROWN, lw=0)
w.text(28, 70, "Кофейня «Зёрнышко»", size=24, color="#FFFFFF", bold=True)
w.text(28, 100, "информационная система автоматизации работы кофейни",
       size=12, color="#F3E9DF")
w.text(952, 68, "Иванова Анна", size=14, color="#FFFFFF", ha="right")
w.text(952, 90, "роль: бариста", size=12, color="#F3E9DF", ha="right")

items = [
    ("Заказы", "оформление и оплата", True),
    ("Меню", "позиции, категории и цены", True),
    ("Столики", "зал и посадка гостей", True),
    ("Смены", "открытие, закрытие, выручка", True),
    ("Отчёты", "выручка и популярные позиции", True),
    ("Выход", "завершить работу", False),
]
for i, (title, sub, primary) in enumerate(items):
    col, row = i % 2, i // 2
    x = 28 + col * 462 + 10
    y = 148 + row * 128 + 21
    w.button(x, y, 442, 86, "", primary=primary)
    w.text(x + 221, y + 34, title, size=18, color=("#FFFFFF" if primary else DARK),
           bold=True, ha="center")
    w.text(x + 221, y + 58, sub, size=11,
           color=("#F3E9DF" if primary else "#5D4037"), ha="center")

w.rect(0, 540, 980, 40, fc="#EFEBE9", ec="#EFEBE9", lw=0)
w.text(28, 560, "Смена не открыта", size=12, color=GREY)
w.text(952, 560, "Кофейня «Зёрнышко» · версия 1.0", size=12, color="#8D6E63", ha="right")
w.save(OUT + "shot_main.png")
print("ok")
