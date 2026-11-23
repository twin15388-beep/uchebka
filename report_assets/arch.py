import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

plt.rcParams["font.family"] = "DejaVu Sans"

FIG_W, FIG_H = 14.4, 10.4
fig, ax = plt.subplots(figsize=(FIG_W/2.54, FIG_H/2.54))
ax.set_xlim(0, 14.4); ax.set_ylim(0, 10.4); ax.set_aspect("equal"); ax.axis("off")
fig.subplots_adjust(0,0,1,1)

BROWN = "#4E342E"

def band(y, h, title, subtitle=""):
    ax.add_patch(FancyBboxPatch((0.35, y), 13.7, h,
                                boxstyle="round,pad=0,rounding_size=0.12",
                                facecolor="#FAF6F0", edgecolor="#D7CCC8", lw=1.0, zorder=1))
    ax.text(0.65, y+h-0.32, title, fontsize=9.2, fontweight="bold", color=BROWN, va="center")
    if subtitle:
        ax.text(0.65, y+h-0.66, subtitle, fontsize=7.4, color="#6D4C41", va="center")

def box(x, y, w, h, text, fs=8.0, fc="white"):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=fc, edgecolor="#8D6E63", lw=1.0, zorder=3))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color="#212121", zorder=4, linespacing=1.15)

def arrow(x, y1, y2):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=1.1,
                                shrinkA=0, shrinkB=0, mutation_scale=11), zorder=2)

band(7.20, 2.80, "Уровень представления (WPF, XAML)",
     "окна приложения, ввод и отображение данных")
xs = [3.0, 7.2, 11.4]
box(xs[0], 8.35, 2.9, 0.55, "AuthWindow")
box(xs[1], 8.35, 2.9, 0.55, "MainWindow")
box(xs[2], 8.35, 2.9, 0.55, "MenuWindow")
box(xs[0], 7.55, 2.9, 0.55, "OrderWindow")
box(xs[1], 7.55, 2.9, 0.55, "ShiftWindow")
box(xs[2], 7.55, 2.9, 0.55, "ReportWindow")

arrow(7.2, 7.20, 6.40)

band(3.80, 2.60, "Уровень бизнес-логики",
     "аутентификация, расчёт суммы заказа, формирование отчётов")
box(3.0, 4.85, 2.9, 0.62, "AuthService\n(аутентификация)", fs=7.6)
box(7.2, 4.85, 2.9, 0.62, "OrderService\n(расчёт суммы)", fs=7.6)
box(11.4, 4.85, 2.9, 0.62, "ReportService\n(отчёты)", fs=7.6)

arrow(7.2, 3.80, 3.00)

band(0.55, 2.45, "Уровень доступа к данным",
     "SQL-запросы, транзакции, файл базы данных")
box(3.6, 1.60, 3.6, 0.62, "Repositories\n(SQL-запросы)", fs=7.6)
box(10.4, 1.60, 3.6, 0.62, "Database\n(SQLite, coffeeshop.db)", fs=7.6)

fig.savefig("/home/user/uchebka/report_assets/arch.png", dpi=300, facecolor="white")
print("saved")
