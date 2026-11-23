import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False

BROWN = "#6F4E37"
DARK = "#3E2723"
LIGHT = "#E7D9C6"
BORDER = "#D7CCC8"
GREY = "#5D4037"


class Win:
    def __init__(self, w, h, title):
        self.W, self.H = w, h
        self.fig = plt.figure(figsize=(w / 100, h / 100), dpi=200)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(h, 0)
        self.ax.axis("off")
        self.fig.patch.set_facecolor("white")
        self._chrome(title)

    # ---------- primitives ----------
    def rect(self, x, y, w, h, fc="#FFFFFF", ec=None, lw=1.0, r=0, alpha=1.0, z=2):
        if r:
            p = FancyBboxPatch((x, y), w, h,
                               boxstyle=f"round,pad=0,rounding_size={r}",
                               facecolor=fc, edgecolor=(ec if ec else fc),
                               linewidth=lw, alpha=alpha, zorder=z,
                               mutation_aspect=1)
        else:
            p = Rectangle((x, y), w, h, facecolor=fc,
                          edgecolor=(ec if ec else fc), linewidth=lw,
                          alpha=alpha, zorder=z)
        self.ax.add_patch(p)
        return p

    def text(self, x, y, s, size=14, color="#212121", bold=False, italic=False,
             ha="left", va="center", z=6, alpha=1.0):
        self.ax.text(x, y, s, fontsize=size * 0.72, color=color,
                     fontweight=("bold" if bold else "normal"),
                     style=("italic" if italic else "normal"),
                     ha=ha, va=va, zorder=z, alpha=alpha)

    def line(self, x1, y1, x2, y2, color="#BDBDBD", lw=1.0, z=5):
        self.ax.plot([x1, x2], [y1, y2], color=color, lw=lw, zorder=z,
                     solid_capstyle="butt")

    def _chrome(self, title):
        self.rect(0, 0, self.W, self.H, fc="#FFFFFF", ec="#C9C9C9", lw=1.2, r=9)
        bar = self.rect(0, 0, self.W, 34, fc="#F3F3F3", ec="#F3F3F3", lw=0)
        bar.set_clip_path(self.ax.patches[0])
        self.text(14, 17, title, size=12, color="#1F1F1F")
        # window buttons
        self.line(self.W - 54, 17, self.W - 42, 17, color="#3A3A3A", lw=1.3)
        self.rect(self.W - 34, 12, 10, 10, fc="none", ec="#3A3A3A", lw=1.1)
        self.line(self.W - 18, 13, self.W - 8, 23, color="#3A3A3A", lw=1.3)
        self.line(self.W - 8, 13, self.W - 18, 23, color="#3A3A3A", lw=1.3)

    def header(self, title, subtitle="", h=60, right=""):
        y = 32
        self.rect(0, y, self.W, h, fc=BROWN, ec=BROWN, lw=0)
        self.text(24, y + h / 2 - (7 if subtitle else 0), title, size=20,
                  color="#FFFFFF", bold=True)
        if subtitle:
            self.text(24, y + h / 2 + 13, subtitle, size=11, color="#F3E9DF")
        if right:
            self.text(self.W - 24, y + h / 2, right, size=12,
                      color="#F3E9DF", ha="right")

    # ---------- controls ----------
    def button(self, x, y, w, h, label, primary=True, size=14, bold=False,
               enabled=True, z=2):
        fc = BROWN if primary else LIGHT
        tc = "#FFFFFF" if primary else DARK
        alpha = 1.0 if enabled else 0.45
        self.rect(x, y, w, h, fc=fc, ec=fc, r=6, alpha=alpha, z=z)
        self.text(x + w / 2, y + h / 2 + 0.5, label, size=size, color=tc,
                  bold=bold, ha="center", alpha=alpha, z=z + 3)

    def textbox(self, x, y, w, h, value="", size=14, color="#212121"):
        self.rect(x, y, w, h, fc="#FFFFFF", ec=BORDER, lw=1.0, r=2)
        self.text(x + 10, y + h / 2 + 0.5, value, size=size, color=color)

    def combobox(self, x, y, w, h, value="", size=14):
        self.rect(x, y, w, h, fc="#FFFFFF", ec=BORDER, lw=1.0, r=2)
        self.text(x + 10, y + h / 2 + 0.5, value, size=size)
        cx, cy = x + w - 18, y + h / 2
        self.ax.plot([cx - 5, cx, cx + 5], [cy - 2, cy + 3, cy - 2],
                     color="#555555", lw=1.4, zorder=7, solid_capstyle="round")

    def checkbox(self, x, y, label, checked=True, size=13):
        s = 16
        if checked:
            self.rect(x, y, s, s, fc=BROWN, ec=BROWN, lw=1.0, r=2)
            self.ax.plot([x + 4, x + 7, x + 12.5], [y + 8, y + 12, y + 3.5],
                         color="white", lw=1.8, zorder=8,
                         solid_capstyle="round", solid_joinstyle="round")
        else:
            self.rect(x, y, s, s, fc="#FFFFFF", ec="#8D6E63", lw=1.2, r=2)
        self.text(x + s + 8, y + s / 2, label, size=size)

    def radio(self, x, y, label, checked=False, size=14):
        self.ax.add_patch(Circle((x + 8, y + 8), 7.2, facecolor="#FFFFFF",
                                 edgecolor="#8D6E63", lw=1.2, zorder=6))
        if checked:
            self.ax.add_patch(Circle((x + 8, y + 8), 3.6, facecolor=BROWN,
                                     edgecolor=BROWN, lw=1, zorder=7))
        self.text(x + 22, y + 8, label, size=size)

    def panel(self, x, y, w, h, title=None, pad=10):
        self.rect(x, y, w, h, fc="#FFFFFF", ec=LIGHT, lw=1.2, r=8)
        if title:
            self.text(x + pad, y + 20, title, size=14, color=DARK, bold=True)

    def listview(self, x, y, w, h, columns, rows, selected=None,
                 row_h=34, head_h=34, size=13, header=True):
        self.rect(x, y, w, h, fc="#FFFFFF", ec="#E3E3E3", lw=1.0)
        if header:
            self.rect(x, y, w, head_h, fc="#F7F7F7", ec="#E3E3E3", lw=0.8)
            cx = x
            for title, cw in columns:
                self.text(cx + 10, y + head_h / 2, title, size=size, color="#3F3F3F")
                cx += cw
            cx = x
            for title, cw in columns[:-1]:
                cx += cw
                self.line(cx, y + 6, cx, y + head_h - 6, color="#DDDDDD", lw=0.9)
        for i, row in enumerate(rows):
            ry = y + head_h + i * row_h
            if selected is not None and i == selected:
                self.rect(x, ry, w, row_h, fc="#EDEDED", ec="#EDEDED", lw=0)
            self.line(x, ry + row_h, x + w, ry + row_h, color="#EFEFEF", lw=0.8)
            cx = x
            for val, (_, cw) in zip(row, columns):
                self.text(cx + 10, ry + row_h / 2, val, size=size)
                cx += cw

    def save(self, path):
        self.fig.savefig(path, dpi=200, facecolor="white")
        plt.close(self.fig)
