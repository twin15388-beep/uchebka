import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle, Circle

plt.rcParams["font.family"] = "DejaVu Sans"

FIG_W, FIG_H = 16.5, 11.6
fig, ax = plt.subplots(figsize=(FIG_W/2.54, FIG_H/2.54))
ax.set_xlim(0, 16.5); ax.set_ylim(0, 11.6); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0,0,1,1)

BROWN = "#4E342E"
FILL = "#FDF8F2"
BLUE = "#1565C0"
GREY = "#424242"

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

def usecase(x, y, text, w=4.45, h=1.04):
    ax.add_patch(Ellipse((x, y), w, h, facecolor="white", edgecolor=BROWN,
                         lw=1.3, zorder=3))
    ax.text(x, y, wrap(text, 22), ha="center", va="center", fontsize=8.3,
            color="#212121", zorder=4, linespacing=1.05)

def actor(x, y, name):
    ax.add_patch(Circle((x, y+0.42), 0.16, facecolor="white", edgecolor=BROWN, lw=1.4, zorder=3))
    ax.plot([x, x], [y+0.26, y-0.30], color=BROWN, lw=1.4, zorder=3)
    ax.plot([x-0.30, x+0.30], [y+0.10, y+0.10], color=BROWN, lw=1.4, zorder=3)
    ax.plot([x, x-0.24], [y-0.30, y-0.68], color=BROWN, lw=1.4, zorder=3)
    ax.plot([x, x+0.24], [y-0.30, y-0.68], color=BROWN, lw=1.4, zorder=3)
    ax.text(x, y-1.0, name, ha="center", va="top", fontsize=9.5, color="#212121")

def assoc(p1, p2):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-", color=GREY, lw=0.9, shrinkA=0, shrinkB=0),
                zorder=2)

def include(p1, p2):
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0,
                                linestyle=(0, (4, 3)), shrinkA=0, shrinkB=0,
                                mutation_scale=10), zorder=2)
    ax.text((p1[0]+p2[0])/2 + 0.15, (p1[1]+p2[1])/2, "«include»",
            ha="left", va="center", fontsize=8.2, color=BLUE, style="italic",
            bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none", alpha=0.9), zorder=5)

# ---------- system boundary ----------
ax.add_patch(Rectangle((3.1, 0.75), 10.45, 9.65, facecolor=FILL, edgecolor=BROWN,
                       lw=1.4, zorder=1))
ax.text(8.25, 10.05, "Информационная система «Кофейня»", ha="center", va="center",
        fontsize=11.2, fontweight="bold", color=BROWN)

LX, RX = 5.90, 11.05
uc = {
    "menu":   (LX, 9.05),
    "order":  (LX, 7.55),
    "mod":    (LX, 6.05),
    "auth":   (LX, 4.55),
    "check":  (LX, 3.05),
    "open":   (LX, 1.55),
    "adm_menu":  (RX, 9.05),
    "adm_users": (RX, 7.55),
    "report":    (RX, 6.05),
    "close":     (RX, 4.55),
}
usecase(*uc["menu"], "Просмотреть меню")
usecase(*uc["order"], "Оформить заказ")
usecase(*uc["mod"], "Добавить модификатор")
usecase(*uc["auth"], "Авторизоваться")
usecase(*uc["check"], "Закрыть чек")
usecase(*uc["open"], "Открыть смену")
usecase(*uc["adm_menu"], "Управлять меню")
usecase(*uc["adm_users"], "Управлять сотрудниками")
usecase(*uc["report"], "Сформировать отчёт")
usecase(*uc["close"], "Закрыть смену")

# ---------- actors ----------
actor(1.45, 8.9, "Гость")
actor(1.45, 3.4, "Бариста")
actor(14.55, 4.75, "Администратор")

# ---------- associations ----------
assoc((1.95, 8.95), (uc["menu"][0]-1.95, uc["menu"][1]))
assoc((1.95, 8.65), (uc["order"][0]-1.95, uc["order"][1]+0.20))
assoc((1.95, 3.70), (uc["auth"][0]-1.95, uc["auth"][1]-0.15))
assoc((1.95, 3.50), (uc["order"][0]-1.95, uc["order"][1]-0.35))
assoc((1.95, 3.25), (uc["check"][0]-1.95, uc["check"][1]+0.05))
assoc((1.95, 3.05), (uc["open"][0]-1.95, uc["open"][1]+0.15))
assoc((14.05, 5.25), (uc["adm_menu"][0]+2.22, uc["adm_menu"][1]-0.12))
assoc((14.05, 5.15), (uc["adm_users"][0]+2.22, uc["adm_users"][1]-0.05))
assoc((14.05, 5.05), (uc["report"][0]+2.22, uc["report"][1]+0.05))
assoc((14.05, 4.95), (uc["close"][0]+2.22, uc["close"][1]+0.10))

# ---------- include ----------
include((uc["order"][0], uc["order"][1]-0.51), (uc["mod"][0], uc["mod"][1]+0.51))

fig.savefig("/home/user/uchebka/report_assets/uml_usecase.png", dpi=300,
            facecolor="white")
print("saved")
