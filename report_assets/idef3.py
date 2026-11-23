import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, FancyArrowPatch

plt.rcParams["font.family"] = "DejaVu Sans"

FIG_W, FIG_H = 14.2, 15.6
fig, ax = plt.subplots(figsize=(FIG_W/2.54, FIG_H/2.54))
ax.set_xlim(0, 14.2); ax.set_ylim(0, 15.6); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0,0,1,1)

BROWN = "#4E342E"
BLUE = "#1565C0"
GREY = "#333333"

def wrap(s, n):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= n:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    return "\n".join(lines)

def arrow(p1, p2, color=GREY, lw=1.1, style="-|>", ls="-"):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                linestyle=ls, shrinkA=0, shrinkB=0,
                                mutation_scale=11), zorder=2)

def uob(x, y, text, num, w=4.9, h=1.05, fs=8.2):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BROWN, lw=1.2, zorder=3))
    ax.text(x, y, wrap(text, 26), ha="center", va="center", fontsize=fs,
            color="#212121", zorder=4, linespacing=1.1)
    # номер UOB в маленьком квадрате в правом верхнем углу
    ax.add_patch(Rectangle((x+w/2-0.52, y+h/2-0.42), 0.52, 0.42,
                           facecolor=BROWN, edgecolor=BROWN, lw=1.0, zorder=5))
    ax.text(x+w/2-0.26, y+h/2-0.21, str(num), ha="center", va="center",
            fontsize=7.6, color="white", fontweight="bold", zorder=6)

def junction(x, y, sym, label):
    ax.add_patch(Rectangle((x-0.30, y-0.30), 0.60, 0.60, facecolor="white",
                           edgecolor=BROWN, lw=1.2, zorder=3))
    ax.text(x, y, sym, ha="center", va="center", fontsize=12,
            fontweight="bold", color=BROWN, zorder=4)
    ax.text(x, y+0.42, label, ha="center", va="bottom", fontsize=7.8,
            color=BROWN, style="italic", zorder=4)

def terminator(x, y, text):
    ax.add_patch(Ellipse((x, y), 1.7, 0.62, facecolor="#EFE6DC",
                         edgecolor=BROWN, lw=1.2, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=8.2,
            color=BROWN, zorder=4)

# ---------- уровень 0: начало ----------
terminator(7.1, 14.9, "Начало")
arrow((7.1, 14.59), (7.1, 14.25))

# ---------- UOB 1 ----------
uob(7.1, 13.65, "Принять заказ у гостя", 1, w=5.0)
arrow((7.1, 13.12), (7.1, 12.55))

# ---------- J1 ----------
junction(7.1, 11.95, "X", "J1")
ax.text(7.50, 11.62, "Заказ на месте?", ha="left", va="top",
        fontsize=8.0, color=BROWN, style="italic")

# ветка ДА — влево
arrow((6.80, 11.95), (3.85, 11.95))
arrow((3.85, 11.95), (3.85, 11.28))
ax.text(4.05, 12.12, "Да", fontsize=8.2, color=BLUE, style="italic")

# ветка НЕТ — вправо
arrow((7.40, 11.95), (10.35, 11.95))
arrow((10.35, 11.95), (10.35, 11.28))
ax.text(9.55, 12.12, "Нет", fontsize=8.2, color=BLUE, style="italic")

# ---------- UOB 2 и UOB 3 ----------
uob(3.85, 10.75, "Закрепить заказ за столиком", 2, w=5.0)
uob(10.35, 10.75, "Подготовить упаковку", 3, w=4.6)

arrow((3.85, 10.22), (3.85, 9.35))
arrow((10.35, 10.22), (10.35, 9.35))
arrow((3.85, 9.35), (6.80, 9.35))
arrow((10.35, 9.35), (7.40, 9.35))

# ---------- J2 ----------
junction(7.1, 8.75, "&", "J2")
arrow((7.1, 9.05), (7.1, 8.75))
arrow((7.1, 8.45), (7.1, 7.85))

# ---------- UOB 4 ----------
uob(7.1, 7.20, "Рассчитать стоимость заказа", 4, w=5.2, h=1.05)
arrow((7.1, 6.67), (7.1, 6.10))

# ---------- J3 ----------
junction(7.1, 5.55, "X", "J3")
ax.text(7.50, 5.22, "Оплата прошла?", ha="left", va="top",
        fontsize=8.0, color=BROWN, style="italic")

arrow((6.80, 5.55), (3.85, 5.55))
arrow((3.85, 5.55), (3.85, 4.88))
ax.text(4.05, 5.72, "Да", fontsize=8.2, color=BLUE, style="italic")

arrow((7.40, 5.55), (10.35, 5.55))
arrow((10.35, 5.55), (10.35, 4.88))
ax.text(9.55, 5.72, "Нет", fontsize=8.2, color=BLUE, style="italic")

# ---------- UOB 5 и UOB 6 ----------
uob(3.85, 4.35, "Выдать заказ гостю", 5, w=4.6)
uob(10.35, 4.35, "Отменить чек", 6, w=4.6)

arrow((3.85, 3.82), (3.85, 3.25))
arrow((10.35, 3.82), (10.35, 3.25))
terminator(3.85, 2.90, "Конец")
terminator(10.35, 2.90, "Конец")

# ---------- легенда ----------
ax.add_patch(FancyBboxPatch((0.6, 0.35), 13.0, 1.75,
                            boxstyle="round,pad=0,rounding_size=0.10",
                            facecolor="#FAF6F0", edgecolor="#D7CCC8", lw=1.0, zorder=1))
ax.text(0.9, 1.80, "Обозначения:", fontsize=8.6, fontweight="bold", color=BROWN)
ax.text(0.9, 1.38, "UOB — единица работы (Unit of Behavior);   X — исключающее ИЛИ (XOR);", fontsize=8.0, color="#333333")
ax.text(0.9, 0.98, "& — логическое И (AND);   → — связь предшествования;", fontsize=8.0, color="#333333")
ax.text(0.9, 0.58, "J1–J3 — логические переключатели (junctions)", fontsize=8.0, color="#333333")

fig.savefig("/home/user/uchebka/report_assets/idef3.png", dpi=300, facecolor="white")
print("saved")
