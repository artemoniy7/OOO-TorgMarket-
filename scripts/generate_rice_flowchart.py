#!/usr/bin/env python3
"""Generate a swimlane process diagram for ООО «ТоргМаркет» as editable SVG."""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import wrap


OUTPUT = Path(__file__).resolve().parents[1] / "artifacts" / "rice_task_flowchart.svg"
WIDTH, HEIGHT = 1920, 1080
LANE_X, LANE_Y, LANE_WIDTH, LANE_HEIGHT = 70, 270, 1780, 115
LANES = (
    "Коммерческий\nдиректор",
    "Менеджер по работе\nс поставщиками",
    "Логист",
    "Ядро системы /\nИТ-специалист",
    "Главный\nбухгалтер",
)


def lines(value: str, width: int) -> list[str]:
    return wrap(value, width=width, break_long_words=False, break_on_hyphens=False)


def text(x: int, y: int, value: str, css_class: str, width: int, line_height: int = 17) -> str:
    return "\n".join(
        f'<text x="{x}" y="{y + index * line_height}" class="{css_class}">{escape(line)}</text>'
        for index, line in enumerate(lines(value, width))
    )


def task(x: int, y: int, label: str, *, accent: str = "#FFFFFF") -> str:
    return "\n".join(
        (
            f'<rect x="{x}" y="{y}" width="200" height="66" rx="8" fill="{accent}" stroke="#59707C" stroke-width="2"/>',
            text(x + 14, y + 27, label, "task", 24),
        )
    )


def decision(x: int, y: int, label: str) -> str:
    return "\n".join(
        (
            f'<path d="M {x} {y - 42} L {x + 52} {y} L {x} {y + 42} L {x - 52} {y} Z" class="decision"/>',
            text(x - 33, y - 8, label, "decision-text", 11, 14),
        )
    )


def arrow(path: str, label: str = "", x: int = 0, y: int = 0, *, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="8 7"' if dashed else ""
    label_svg = "" if not label else f'<text x="{x}" y="{y}" class="arrow-label">{escape(label)}</text>'
    return f'<path d="{path}" class="arrow"{dash}/>{label_svg}'


def db_marker(x: int, y: int, letter: str, color: str) -> str:
    return f'<circle cx="{x}" cy="{y}" r="15" fill="{color}"/><text x="{x - 4}" y="{y + 5}" class="marker">{letter}</text>'


def build_svg() -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">Сквозной процесс поставки и продажи ООО «ТоргМаркет»</title>',
        '<desc id="desc">Блок-схема со служебными дорожками: от потребности в товаре до проведения сделки в учёте.</desc>',
        '<defs><marker id="arrowhead" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M 0 0 L 10 4 L 0 8 z" fill="#3B5966"/></marker></defs>',
        '<style>.eyebrow{font:700 14px Arial,sans-serif;fill:#1e5965;letter-spacing:3px}.title{font:700 40px Georgia,serif;fill:#193740}.subtitle{font:400 17px Arial,sans-serif;fill:#536873}.lane{font:700 15px Arial,sans-serif;fill:#fff}.task{font:700 14px Arial,sans-serif;fill:#203b45}.decision{fill:#f9fbfc;stroke:#3b5966;stroke-width:2}.decision-text{font:700 12px Arial,sans-serif;fill:#203b45}.arrow{fill:none;stroke:#3b5966;stroke-width:3;marker-end:url(#arrowhead)}.arrow-label{font:700 13px Arial,sans-serif;fill:#3b5966}.marker{font:700 13px Arial,sans-serif;fill:#fff}.legend{font:700 14px Arial,sans-serif;fill:#334e58}.note{font:400 14px Arial,sans-serif;fill:#536873}</style>',
        '<rect width="1920" height="1080" fill="#f8fbf9"/>',
        '<rect x="0" y="0" width="28" height="1080" fill="#1d5a65"/>',
        '<text x="70" y="75" class="eyebrow">СКВОЗНОЙ ПРОЦЕСС</text>',
        '<path d="M 70 92 H 155" stroke="#1d5a65" stroke-width="5"/>',
        '<text x="70" y="145" class="title">Схема процесса: от потребности до продажи товара</text>',
        '<text x="70" y="180" class="subtitle">Роли указаны без персональных данных. Метки C и U показывают создание и изменение записи в БД.</text>',
        '<rect x="70" y="225" width="1780" height="620" rx="10" fill="#fff" stroke="#c7d4d7" stroke-width="2"/>',
    ]
    lane_colors = ("#266675", "#3a7a7a", "#538465", "#496b91", "#7c5c77")
    for index, (label, color) in enumerate(zip(LANES, lane_colors)):
        y = LANE_Y + index * LANE_HEIGHT
        parts.append(f'<rect x="{LANE_X}" y="{y}" width="190" height="{LANE_HEIGHT}" fill="{color}"/>')
        parts.append(f'<rect x="260" y="{y}" width="1590" height="{LANE_HEIGHT}" fill="{"#f5f9f8" if index % 2 == 0 else "#edf4f2"}"/>')
        for line_index, line in enumerate(label.split("\n")):
            parts.append(f'<text x="92" y="{y + 50 + line_index * 19}" class="lane">{line}</text>')

    # Tasks, decisions and the handoffs between responsibility lanes.
    parts.extend(
        (
            '<circle cx="300" cy="327" r="29" fill="#fff" stroke="#1d5a65" stroke-width="4"/>',
            task(355, 294, "Сформировать\nпотребность"),
            db_marker(540, 285, "C", "#3567a6"),
            task(620, 409, "Запросить наличие\nи срок поставки"),
            decision(890, 442, "Товар\nдоступен?"),
            task(1010, 524, "Принять поставку\nи сверить УПД"),
            task(1245, 639, "Проверить остатки\nи коды КМ", accent="#e4efff"),
            decision(1495, 672, "Данные\nкорректны?"),
            task(1595, 294, "Подтвердить товар\nдля продажи"),
            task(1595, 639, "Создать продажу\nи вывести КМ", accent="#e4efff"),
            task(1595, 754, "Провести документы\nи оплату"),
            '<circle cx="1810" cy="812" r="29" fill="#fff" stroke="#1d5a65" stroke-width="4"/>',
            db_marker(1425, 629, "U", "#6a52a3"),
            db_marker(1775, 629, "U", "#6a52a3"),
            db_marker(1775, 744, "U", "#6a52a3"),
            arrow('M 329 327 H 355'),
            arrow('M 555 327 H 590 V 442 H 620'),
            arrow('M 820 442 H 838', 'проверка', 760, 425),
            arrow('M 942 442 H 970 V 557 H 1010', 'да', 953, 495),
            arrow('M 890 484 V 510 H 690 V 475', 'нет', 800, 503),
            arrow('M 1210 557 H 1225 V 672 H 1245', 'приёмка → ядро', 1125, 625),
            arrow('M 1445 672 H 1443', 'проверка', 1360, 655),
            arrow('M 1547 672 H 1575 V 327 H 1595', 'да', 1555, 500),
            arrow('M 1495 714 V 730 H 1110 V 590', 'нет: уточнить расхождения', 1210, 720),
            arrow('M 1695 360 V 606 H 1695 V 639'),
            arrow('M 1695 705 V 754'),
            arrow('M 1795 787 H 1810'),
        )
    )
    parts.extend(
        (
            '<rect x="70" y="875" width="1780" height="130" rx="10" fill="#eef5f3" stroke="#c7d4d7" stroke-width="2"/>',
            db_marker(103, 912, "C", "#3567a6"),
            '<text x="130" y="917" class="legend">Создание записи в БД</text><text x="365" y="917" class="note">— потребность / заказ поставщику</text>',
            db_marker(103, 952, "U", "#6a52a3"),
            '<text x="130" y="957" class="legend">Изменение записи</text><text x="365" y="957" class="note">— остатки, коды маркировки, статус продажи, дата проведения</text>',
            '<circle cx="103" cy="987" r="15" fill="#a65a5a"/><text x="99" y="992" class="marker">D</text>',
            '<text x="130" y="992" class="legend">Удаление</text><text x="220" y="992" class="note">— в процессе не предусмотрено: операции сохраняются в журнале.</text>',
            '</svg>',
        )
    )
    return "\n".join(parts)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Created {OUTPUT.relative_to(OUTPUT.parents[1])}")


if __name__ == "__main__":
    main()
