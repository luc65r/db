from typing import Optional, Tuple

import drawSvg as draw
import arrow

from cybot.celcat import Calendar


class CalendarTheme:
    def __init__(self) -> None:
        self.text = "#dcddde"
        self.background = "#36393f"
        self.secondary = "#72767d"
        self.primary = "#9ba1aa"
        self.td = "#4A4AFF"
        self.cm = "#FF0000"
        self.tp = "#FE8BAD"
        self.exam = "#00FFFF"
        self.tiers = "#6FFFFF"

    pass


class Override:
    def __init__(self, height: float) -> None:
        self.height = height

    def Text(
        self,
        text: str,
        fontSize: int,
        x: float,
        y: float,
        col: str,
        anch: Optional[str] = None,
    ) -> draw.Text:
        return draw.Text(
            text, fontSize, x, self.height - y - fontSize, text_anchor=anch, fill=col
        )

    def Line(
        self, sx: float, sy: float, ex: float, ey: float, width: int, color: str
    ) -> draw.Line:
        return draw.Line(
            sx, self.height - sy, ex, self.height - ey, stroke_width=width, stroke=color
        )

    def Rectangle(
        self, x: float, y: float, w: float, h: float, color: str
    ) -> draw.Rectangle:
        return draw.Rectangle(x, self.height - y, w, -h, fill=color)


class SvgCalendar:
    def __init__(
        self,
        date: arrow,
        group: int,
        lines: int,
        spacing: float,
        dayHeight: float,
        dayLength: float,
        margin: float,
        theme: CalendarTheme,
    ) -> None:
        self.days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        self.lines = lines
        self.spacing = spacing
        self.dayHeight = dayHeight
        self.dayLength = dayLength
        self.margin = margin
        self.theme = theme
        self.width = margin + 3.5 * 16 + dayLength * self.days.__len__() + margin
        self.height = (lines - 1) * spacing + 2 * margin + dayHeight
        self.d = draw.Drawing(self.width, self.height, origin=(0, 0))
        self.o = Override(self.height)

        self.draw_table()

        d = date.format("W", locale="fr")
        start = arrow.get(d[:-1] + "1", "W")
        end = arrow.get(d[:-1] + "5", "W")
        c = Calendar(start, end)
        c.fetch(group)
        for e in c.courses:
            # if e.start.date() == date.date():
            # print(str(e.start.date())+"\n")
            self.draw_course(
                e.name,
                e.start.format("dddd", locale="fr").capitalize(),
                e.start,
                e.end,
                e.prof,
                self.colorEvent(e.category),
            )

        # self.d.setPixelScale(1)
        self.d.savePng("edt.png")
        self.d.saveSvg("edt.svg")

    def colorChannelMixer(
        self, colorChannelA: float, colorChannelB: float, amountToMix: float
    ) -> int:
        channelA = colorChannelA * amountToMix
        channelB = colorChannelB * (1 - amountToMix)
        return int(channelA + channelB)

    def colorMixer(
        self, rgbA: Tuple[int, ...], rgbB: Tuple[int, ...], amountToMix: float
    ) -> str:
        r = self.colorChannelMixer(rgbA[0], rgbB[0], amountToMix)
        g = self.colorChannelMixer(rgbA[1], rgbB[1], amountToMix)
        b = self.colorChannelMixer(rgbA[2], rgbB[2], amountToMix)
        return "rgb(" + str(r) + "," + str(g) + "," + str(b) + ")"

    def colorEvent(self, event: str) -> str:
        if event == "TD":
            return self.theme.td
        elif event == "TP":
            return self.theme.tp
        elif event == "CM":
            return self.theme.cm
        elif event == "Examens":
            return self.theme.exam
        elif event == "Tiers temps":
            return self.theme.tiers
        else:
            return "#1e7b91"

    def draw_table(self) -> None:
        self.d.draw(
            self.o.Rectangle(0, 0, self.width, self.height, self.theme.background)
        )
        self.d.draw(
            self.o.Line(
                self.margin,
                self.margin,
                self.margin + 3.5 * 16 + self.dayLength * self.days.__len__(),
                self.margin,
                1,
                self.theme.primary,
            )
        )
        for i in range(self.days.__len__()):
            self.d.draw(
                self.o.Text(
                    self.days[i],
                    16,
                    self.margin + 3.5 * 16 + self.dayLength * i + self.dayLength / 2,
                    self.margin + 16 - 1,
                    self.theme.text,
                    "middle",
                )
            )
            self.d.draw(
                self.o.Line(
                    self.margin + 3.5 * 16 + self.dayLength * (i + 1),
                    self.margin,
                    self.margin + 3.5 * 16 + self.dayLength * (i + 1),
                    (self.lines - 1) * self.spacing + self.margin + self.dayHeight,
                    1,
                    self.theme.primary,
                )
            )
        time = arrow.get("08:00", "HH:mm")
        for i in range(self.lines - 1):
            self.d.draw(
                self.o.Line(
                    self.margin,
                    i * self.spacing + self.margin + self.dayHeight,
                    self.width - 2 * self.margin,
                    i * self.spacing + self.margin + self.dayHeight,
                    1,
                    (self.theme.primary if not (i % 3) else self.theme.secondary),
                )
            )
            self.d.draw(
                self.o.Text(
                    time.format("H:mm", locale="fr"),
                    16,
                    self.margin + 3,
                    i * self.spacing + self.margin + 16 / 2 - 1 + self.dayHeight,
                    self.theme.text,
                )
            )
            time = time.shift(minutes=30)
        self.d.draw(
            self.o.Line(
                self.margin,
                (self.lines - 1) * self.spacing + self.margin + self.dayHeight,
                self.margin + 3.5 * 16 + self.dayLength * self.days.__len__(),
                (self.lines - 1) * self.spacing + self.margin + self.dayHeight,
                1,
                self.theme.primary,
            )
        )
        self.d.draw(
            self.o.Line(
                self.margin,
                self.margin,
                self.margin,
                (self.lines - 1) * self.spacing + self.margin + self.dayHeight,
                1,
                self.theme.primary,
            )
        )
        self.d.draw(
            self.o.Line(
                3.5 * 16,
                self.margin,
                3.5 * 16,
                (self.lines - 1) * self.spacing + self.margin + self.dayHeight,
                1,
                self.theme.primary,
            )
        )

    def draw_course(
        self, name: str, day: str, start: arrow, end: arrow, teacher: str, color: str
    ) -> None:
        i = self.days.index(day)
        x1 = self.margin + 3.5 * 16 + self.dayLength * i
        x2 = self.margin + 3.5 * 16 + self.dayLength * (i + 1) - 1
        timeStart = (start.datetime.hour - 8) * 2 + start.datetime.minute / 30
        timeEnd = (end.datetime.hour - 8) * 2 + end.datetime.minute / 30
        y1 = timeStart * self.spacing + self.margin + self.dayHeight
        y2 = timeEnd * self.spacing + self.margin + self.dayHeight
        self.d.draw(
            self.o.Rectangle(
                x1 + 0.1,
                y1,
                x2 - x1,
                y2 - y1,
                self.colorMixer(
                    tuple(int(color.lstrip("#")[i : i + 2], 16) for i in (0, 2, 4)),
                    tuple(
                        int(self.theme.background.lstrip("#")[i : i + 2], 16)
                        for i in (0, 2, 4)
                    ),
                    0.2,
                ),
            )
        )
        self.d.draw(self.o.Line(x1, y1, x2, y1, 2, color))
        self.d.draw(self.o.Line(x1, y1, x1, y2, 2, color))
        self.d.draw(self.o.Line(x2, y1, x2, y2, 2, color))
        self.d.draw(self.o.Line(x1, y2, x2, y2, 2, color))
        self.d.draw(
            self.o.Text(
                start.format("H:mm", locale="fr"), 13, x1 + 3, y1 + 3, self.theme.text
            )
        )
        if timeEnd - timeStart > 1:
            self.d.draw(
                self.o.Text(
                    end.format("H:mm", locale="fr"),
                    13,
                    x1 + 3,
                    y2 - 1 - 16,
                    self.theme.text,
                )
            )
            self.d.draw(
                self.o.Text(
                    teacher.replace(", ", "\n") if teacher is not None else "",
                    14,
                    x1 + 3,
                    y1 + 4 + 16,
                    "#00db6b",
                )
            )
        self.d.draw(self.o.Text(name, 14, x1 + 6 * 7, y1 + 3, self.theme.text))
