# Erzeugt eigene, lizenzfreie Lernillustrationen (entre, réponse, un/une, des).
from PIL import Image, ImageDraw, ImageFont
import os
OUT = os.path.join(os.path.dirname(__file__), "..", "media")
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(s): return ImageFont.truetype(F, s)
def canvas(): 
    im = Image.new("RGB", (500, 300), "#fdf6e3"); return im, ImageDraw.Draw(im)
def center(d, xy, text, f, fill):
    x0, y0, x1, y1 = xy; w = d.textlength(text, font=f)
    d.text(((x0+x1)/2 - w/2, (y0+y1)/2 - f.size/2 - 3), text, font=f, fill=fill)

# entre
im, d = canvas()
d.rounded_rectangle((20, 70, 150, 230), 12, fill="#4a90d9"); center(d, (20,70,150,230), "A", font(60), "white")
d.rounded_rectangle((350, 70, 480, 230), 12, fill="#4a90d9"); center(d, (350,70,480,230), "B", font(60), "white")
d.ellipse((205, 120, 295, 210), fill="#e85d4a"); center(d, (205,120,295,210), "X", font(46), "white")
d.line((155, 150, 200, 150), fill="#555", width=4); d.polygon([(200,142),(200,158),(212,150)], fill="#555")
d.line((345, 150, 300, 150), fill="#555", width=4); d.polygon([(300,142),(300,158),(288,150)], fill="#555")
center(d, (0, 245, 500, 295), "X est ENTRE A et B", font(26), "#333")
im.save(f"{OUT}/fr_entre.jpg", quality=92)

# réponse
im, d = canvas()
d.rounded_rectangle((20, 40, 250, 140), 24, fill="#4a90d9"); d.polygon([(60,138),(50,175),(95,138)], fill="#4a90d9")
center(d, (20,40,250,140), "?", font(70), "white")
d.rounded_rectangle((250, 150, 480, 250), 24, fill="#5cb85c"); d.polygon([(440,248),(455,285),(405,248)], fill="#5cb85c")
center(d, (250,150,480,250), "!", font(70), "white")
d.text((30, 5), "la question", font=font(22), fill="#333"); d.text((290, 255), "la réponse", font=font(22), fill="#333")
im.save(f"{OUT}/fr_reponse.jpg", quality=92)

# un / une und des
def stars(n, color, name, label):
    im, d = canvas(); w = 500 // max(n, 1)
    for i in range(n):
        cx = (i + 0.5) * (500 / n) if n > 1 else 250
        d.rounded_rectangle((cx-45, 70, cx+45, 160), 14, fill=color)
    center(d, (0, 210, 500, 285), label, font(34), "#333")
    im.save(f"{OUT}/{name}.jpg", quality=92)
stars(1, "#e85d4a", "fr_un_une", "un / une  =  1")
stars(4, "#4a90d9", "fr_des", "des  =  mehrere")
