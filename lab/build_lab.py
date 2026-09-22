# -*- coding: utf-8 -*-
"""Сборка оформления упражнений 2 и 3 лабораторной работы №1."""
import math
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, CondPageBreak)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DJ", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DJ-B", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFontFamily("DJ", normal="DJ", bold="DJ-B")

# ---------- исходные данные (упражнение 1) ----------
h = [40.0, 40.0, 39.8, 40.1, 40.0]     # мм
d = [15.0, 15.0, 15.0, 15.0, 15.0]     # мм
m = 19.07                               # г
n = 5
theta = 0.1        # цена деления нониуса штангенциркуля, мм
ds_m = 0.01        # систематическая погрешность весов, г
t = 2.78           # коэффициент Стьюдента, P=0.95, n=5

hm = sum(h) / n
dm = sum(d) / n
dh = [hm - x for x in h]
dd = [dm - x for x in d]
sum_dh2 = sum(x * x for x in dh)
sum_dd2 = sum(x * x for x in dd)
sig_h = math.sqrt(sum_dh2 / (n * (n - 1)))
sig_d = math.sqrt(sum_dd2 / (n * (n - 1)))
dh_sl = sig_h * t
dd_sl = sig_d * t

ratio_h = theta / sig_h            # 2.04 -> 0.8 <= r <= 8
k_h = 0.71                         # по таблице k для Δs/σ = 2
D_h = k_h * (theta + sig_h * t)
D_d = theta                        # σ(d)=0 -> отношение > 8 -> Δ = Δs(d)
delta_h = D_h / hm * 100
delta_d = D_d / dm * 100
delta_m = ds_m / m * 100

PI = 3.14
rho = 4 * m / (PI * hm * dm ** 2) * 1e6          # кг/м³
sig_rho = rho * math.sqrt((sig_h / hm) ** 2 + 4 * (sig_d / dm) ** 2)
d_rho_sl = sig_rho * t
Ds_rho = 1.1 * rho * math.sqrt((ds_m / m) ** 2 + (theta / hm) ** 2
                               + 4 * (theta / dm) ** 2)
ratio_rho = Ds_rho / sig_rho                      # > 8 -> Δ(ρ) = Δs(ρ)
D_rho = Ds_rho
delta_rho = D_rho / rho * 100

# ---------- стили ----------
body = ParagraphStyle("body", fontName="DJ", fontSize=10, leading=14.5,
                      alignment=TA_JUSTIFY, spaceAfter=3)
h1 = ParagraphStyle("h1", parent=body, fontName="DJ-B", fontSize=13,
                    leading=17, alignment=TA_CENTER, spaceBefore=8, spaceAfter=6)
h2 = ParagraphStyle("h2", parent=body, fontName="DJ-B", fontSize=10.5,
                    leading=15, spaceBefore=8, spaceAfter=3)
cap = ParagraphStyle("cap", parent=body, fontSize=9.5, alignment=TA_CENTER,
                     spaceBefore=4, spaceAfter=4)
fml = ParagraphStyle("fml", parent=body, fontSize=10.5, leading=17,
                     alignment=TA_CENTER, spaceBefore=3, spaceAfter=3)
cell = ParagraphStyle("cell", fontName="DJ", fontSize=7.6, leading=9.5,
                      alignment=TA_CENTER)
cellL = ParagraphStyle("cellL", parent=cell, alignment=0, fontSize=8)

P = lambda s, st=body: Paragraph(s, st)
C = lambda s: Paragraph(s, cell)
CL = lambda s: Paragraph(s, cellL)
f = lambda v, p=2: ("%%.%df" % p % v).replace(".", ",")

story = []
story.append(P("Лабораторная работа № 1. Определение линейных размеров, "
               "массы и плотности твёрдого тела", h1))
story.append(P("Образец — алюминиевый цилиндр. Исходные данные (упражнение 1): "
               "h<sub>i</sub> = 40,0; 40,0; 39,8; 40,1; 40,0 мм; "
               "d<sub>i</sub> = 15,0 мм (5 измерений); m = 19,07 г; "
               "n = 5; θ = 0,1 мм; Δ<sub>s</sub>(m) = 0,01 г; P = 0,95; "
               "t(P, n) = 2,78.", body))

# ===================== УПРАЖНЕНИЕ 2 =====================
story.append(P("Упражнение 2. Расчёт погрешностей прямых измерений "
               "диаметра, высоты и массы цилиндра", h1))

story.append(P("1. Средние значения (из упражнения 1)", h2))
story.append(P("h̄ = (1/n)·Σh<sub>i</sub> = (40,0 + 40,0 + 39,8 + 40,1 + 40,0)/5 = "
               "<b>39,98 мм</b>", fml))
story.append(P("d̄ = (1/n)·Σd<sub>i</sub> = (15,0·5)/5 = <b>15,00 мм</b>", fml))

story.append(P("2. Неисключённые систематические погрешности", h2))
story.append(P("Δ<sub>s</sub>(d) = Δ<sub>s</sub>(h) = θ = <b>0,1 мм</b>; "
               "Δ<sub>s</sub>(m) = <b>0,01 г</b>, поэтому Δ(m) = 0,01 г.", body))

story.append(P("3. Абсолютные погрешности отдельных измерений и их квадраты", h2))
tbl1 = [[C("i"), C("h<sub>i</sub>, мм"), C("Δh<sub>i</sub> = h̄ − h<sub>i</sub>, мм"),
         C("(Δh<sub>i</sub>)², мм²"), C("d<sub>i</sub>, мм"),
         C("Δd<sub>i</sub> = d̄ − d<sub>i</sub>, мм"), C("(Δd<sub>i</sub>)², мм²")]]
for i in range(n):
    tbl1.append([C(str(i + 1)), C(f(h[i], 1)), C(f(dh[i])), C(f(dh[i] ** 2, 4)),
                 C(f(d[i], 1)), C(f(dd[i])), C(f(dd[i] ** 2, 4))])
tbl1.append([C("Σ"), C("—"), C("0,00"), C(f(sum_dh2, 4)), C("—"), C("0,00"),
             C(f(sum_dd2, 4))])
T1 = Table(tbl1, colWidths=[10*mm, 20*mm, 29*mm, 25*mm, 20*mm, 29*mm, 25*mm],
           hAlign="CENTER")
T1.setStyle(TableStyle([
    ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
    ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f4f6f9")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
]))
story.append(T1)

story.append(P("4. СКО серии измерений", h2))
story.append(P("σ(h̄) = √(Σ(Δh<sub>i</sub>)² / (n(n−1))) = √(0,0480 / 20) = "
               "<b>0,049 мм</b>", fml))
story.append(P("σ(d̄) = √(Σ(Δd<sub>i</sub>)² / (n(n−1))) = √(0 / 20) = "
               "<b>0 мм</b>", fml))

story.append(P("5. Случайные погрешности при P = 0,95, t(0,95; 5) = 2,78", h2))
story.append(P("Δh<sub>сл</sub> = σ(h̄)·t = 0,049·2,78 = <b>0,136 мм</b>;&nbsp;&nbsp;"
               "Δd<sub>сл</sub> = σ(d̄)·t = <b>0 мм</b>", fml))

story.append(P("6. Отношение систематической погрешности к СКО и результирующая "
               "погрешность", h2))
story.append(P("Δ<sub>s</sub>(h)/σ(h̄) = 0,1 / 0,049 = <b>2,04</b> — попадает в "
               "интервал 0,8 ≤ Δ<sub>s</sub>/σ ≤ 8, значит суммарная погрешность "
               "берётся по формуле с коэффициентом k (для Δ<sub>s</sub>/σ = 2 → "
               "k = 0,71):", body))
story.append(P("Δ(h̄) = k·[Δ<sub>s</sub>(h) + σ(h̄)·t(P,n)] = "
               "0,71·(0,1 + 0,136) = <b>0,17 мм</b>", fml))
story.append(P("Δ<sub>s</sub>(d)/σ(d̄) = 0,1 / 0 → ∞ &gt; 8 — результирующая "
               "погрешность определяется только систематической:", body))
story.append(P("Δ(d̄) = Δ<sub>s</sub>(d) = θ = <b>0,10 мм</b>", fml))

story.append(P("7. Относительные погрешности", h2))
story.append(P("δ(h̄) = Δ(h̄)/h̄ ·100 % = 0,17/39,98 ·100 % = <b>0,42 %</b>", fml))
story.append(P("δ(d̄) = Δ(d̄)/d̄ ·100 % = 0,10/15,00 ·100 % = <b>0,67 %</b>", fml))
story.append(P("δ(m) = Δ(m)/m ·100 % = 0,01/19,07 ·100 % = <b>0,05 %</b>", fml))

# ===================== УПРАЖНЕНИЕ 3 =====================
story.append(CondPageBreak(60*mm))
story.append(P("Упражнение 3. Расчёт погрешностей косвенных измерений "
               "плотности цилиндра", h1))

story.append(P("1. Среднее значение плотности (упражнение 1)", h2))
story.append(P("ρ̄ = 4m / (π·h̄·d̄²) = 4·19,07 / (3,14·39,98·15,0²) = "
               "0,0027 г/мм³ = <b>2701 кг/м³</b>", fml))

story.append(P("2. СКО косвенного измерения плотности", h2))
story.append(P("σ(ρ̄) = ρ̄·√[(σ(h̄)/h̄)² + 4·(σ(d̄)/d̄)²] = "
               "2701·√[(0,049/39,98)² + 0] = <b>3,3 кг/м³</b>", fml))

story.append(P("3. Абсолютная случайная погрешность плотности", h2))
story.append(P("Δρ<sub>сл</sub> = σ(ρ̄)·t(P,n) = 3,3·2,78 = <b>9,2 кг/м³</b>", fml))

story.append(P("4. Неисключённая систематическая погрешность плотности", h2))
story.append(P("Δ<sub>s</sub>(ρ̄) = 1,1·ρ̄·√[(Δ<sub>s</sub>(m)/m)² + "
               "(Δ<sub>s</sub>(h)/h̄)² + 4·(Δ<sub>s</sub>(d)/d̄)²]", fml))
story.append(P("Δ<sub>s</sub>(ρ̄) = 1,1·2701·√[(0,01/19,07)² + (0,1/39,98)² + "
               "4·(0,1/15,0)²] = <b>40,3 кг/м³</b>", fml))

story.append(P("5. Отношение и результирующая погрешность", h2))
story.append(P("Δ<sub>s</sub>(ρ̄)/σ(ρ̄) = 40,3 / 3,3 = <b>12,2 &gt; 8</b> → "
               "погрешность определяется систематической составляющей:", body))
story.append(P("Δ(ρ̄) = Δ<sub>s</sub>(ρ̄) = <b>40 кг/м³</b>", fml))
story.append(P("δ(ρ̄) = Δ(ρ̄)/ρ̄ ·100 % = 40/2701 ·100 % = <b>1,5 %</b>", fml))

# ===================== ТАБЛИЦА 2 =====================
story.append(P("Таблица 2. Результаты расчёта погрешностей прямых и косвенных "
               "измерений", cap))
hdr = [C("n"), C("Δh<sub>i</sub>, мм"), C("Δd<sub>i</sub>, мм"), C("σ(h̄)"),
       C("σ(d̄)"), C("Δ<sub>s</sub>(d)/σ(d̄)"), C("Δ<sub>s</sub>(h)/σ(h̄)"),
       C("Δh<sub>сл</sub>, мм"), C("Δd<sub>сл</sub>, мм")]
rows = [hdr]
for i in range(n):
    rows.append([C(str(i + 1)), C(f(dh[i])), C(f(dd[i])),
                 C(f(sig_h, 3) if i == 0 else ""),
                 C(f(sig_d, 3) if i == 0 else ""),
                 C("∞ (&gt;8)" if i == 0 else ""),
                 C(f(ratio_h) if i == 0 else ""),
                 C(f(dh_sl, 3) if i == 0 else ""),
                 C(f(dd_sl, 3) if i == 0 else "")])
res = [("h = h̄ ± Δ(h̄) = <b>39,98 ± 0,17</b> мм", "δ(h̄) % = <b>0,42</b>"),
       ("d = d̄ ± Δ(d̄) = <b>15,00 ± 0,10</b> мм", "δ(d̄) % = <b>0,67</b>"),
       ("ρ = ρ̄ ± Δ(ρ̄) = <b>2701 ± 40</b> кг/м³", "δ(ρ̄) % = <b>1,5</b>"),
       ("m = m ± Δ(m) = <b>19,07 ± 0,01</b> г", "δ(m) % = <b>0,05</b>")]
for left, right in res:
    rows.append([CL(left), "", "", "", "", CL(right), "", "", ""])

T2 = Table(rows, colWidths=[8*mm, 19*mm, 19*mm, 16*mm, 16*mm, 24*mm, 24*mm,
                            20*mm, 20*mm], hAlign="CENTER")
st = [("GRID", (0, 0), (-1, 5), 0.5, colors.black),
      ("BOX", (0, 0), (-1, -1), 0.8, colors.black),
      ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8edf3")),
      ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
      ("TOPPADDING", (0, 0), (-1, -1), 3.5),
      ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
      # объединённые ячейки столбцов с едиными для серии значениями
      ("SPAN", (3, 1), (3, 5)), ("SPAN", (4, 1), (4, 5)), ("SPAN", (5, 1), (5, 5)),
      ("SPAN", (6, 1), (6, 5)), ("SPAN", (7, 1), (7, 5)), ("SPAN", (8, 1), (8, 5))]
for r in range(6, 10):
    st += [("SPAN", (0, r), (4, r)), ("SPAN", (5, r), (8, r)),
           ("GRID", (0, r), (-1, r), 0.5, colors.black)]
T2.setStyle(TableStyle(st))
story.append(T2)

story.append(Spacer(1, 6))
story.append(P("Вывод: плотность образца ρ = (2,70 ± 0,04)·10³ кг/м³ при "
               "относительной погрешности 1,5 %, что соответствует табличному "
               "значению плотности алюминия 2700 кг/м³. Основной вклад в "
               "погрешность вносит систематическая погрешность штангенциркуля "
               "(θ = 0,1 мм), прежде всего через диаметр, входящий в формулу "
               "в квадрате.", body))


def deco(canvas, doc_):
    canvas.saveState()
    canvas.setFont("DJ", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawRightString(A4[0] - 18*mm, 10*mm, "стр. %d" % doc_.page)
    canvas.restoreState()


doc = SimpleDocTemplate("/tmp/hoplite/workspace/lab/lab1_ex2_ex3.pdf",
                        pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                        topMargin=15*mm, bottomMargin=15*mm,
                        title="Лабораторная работа №1 — упражнения 2 и 3")
doc.build(story, onFirstPage=deco, onLaterPages=deco)
print("ok")
