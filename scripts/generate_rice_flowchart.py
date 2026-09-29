#!/usr/bin/env python3
"""Generate an editable SVG flowchart of task handoffs for ООО «ТоргМаркет»."""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import wrap


OUTPUT = Path(__file__).resolve().parents[1] / "artifacts" / "rice_task_flowchart.svg"
WIDTH, HEIGHT = 1920, 1080


# В схеме указаны только роли — персональные имена не используются.
NODES = (
    ("director", 70, 304, 270, 130, "Главный директор", "Утверждает цели, бюджет и приоритеты проекта.", "#1D4F7A"),
    ("commercial", 420, 304, 300, 130, "Коммерческий директор", "Формирует потребность клиента, цену и условия продажи.", "#007D8A"),
    ("supplier", 770, 560, 300, 130, "Менеджер по работе с поставщиками", "Запрашивает наличие, сроки поставки и первичные документы.", "#7C5A9B"),
    ("logistics", 1120, 560, 300, 130, "Логист", "Принимает товар, сверяет документы и коды маркировки.", "#C46A32"),
    ("it", 1480, 304, 300, 130, "ИТ-специалист", "Проверяет остатки и коды; проводит операцию в БД.", "#2B7A52"),
    ("accounting", 1480, 720, 300, 130, "Главный бухгалтер", "Проверяет НДС, оплату и отражает сделку в учёте.", "#9A3E58"),
)


def wrapped(value: str, width: int) -> list[str]:
    return wrap(value, width=width, break_long_words=False, break_on_hyphens=False)


def node_svg(node: tuple[str, int, int, int, int, str, str, str]) -> str:
    _, x, y, width, height, role, action, color = node
    action_lines = wrapped(action, 35)
    role_lines = wrapped(role, 28)
    elements = [
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="16" fill="#fff" stroke="{color}" stroke-width="3"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="42" rx="14" fill="{color}"/>',
        f'<rect x="{x}" y="{y + 28}" width="{width}" height="14" fill="{color}"/>',
    ]
    for index, line in enumerate(role_lines):
        elements.append(f'<text x="{x + 16}" y="{y + 26 + index * 16}" class="role">{escape(line)}</text>')
    for index, line in enumerate(action_lines):
        elements.append(f'<text x="{x + 16}" y="{y + 68 + index * 19}" class="action">{escape(line)}</text>')
    return "\n".join(elements)


def arrow(path: str, label_x: int, label_y: int, label: str, *, dashed: bool = False) -> str:
    dash = ' stroke-dasharray="9 7"' if dashed else ""
    return "\n".join(
        (
            f'<path d="{path}" class="arrow"{dash}/>',
            f'<rect x="{label_x - 7}" y="{label_y - 17}" width="{max(72, len(label) * 8)}" height="24" rx="8" fill="#f6f8fb"/>',
            f'<text x="{label_x}" y="{label_y}" class="arrow-label">{escape(label)}</text>',
        )
    )


def build_svg() -> str:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">',
        '<title id="title">RICE-карта движения задач ООО «ТоргМаркет» в формате блок-схемы</title>',
        '<desc id="desc">Блок-схема передачи задач между ролями компании без использования персональных имён.</desc>',
        '<defs><marker id="arrowhead" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M 0 0 L 10 4 L 0 8 z" fill="#4E6175"/></marker></defs>',
        '<style>.title{font:700 36px Arial,sans-serif;fill:#132238}.subtitle{font:400 18px Arial,sans-serif;fill:#5a6879}.section{font:700 14px Arial,sans-serif;fill:#34516e;letter-spacing:1px}.role{font:700 15px Arial,sans-serif;fill:#fff}.action{font:400 16px Arial,sans-serif;fill:#17283d}.arrow{fill:none;stroke:#4E6175;stroke-width:3;marker-end:url(#arrowhead)}.arrow-label{font:700 13px Arial,sans-serif;fill:#3A5068}.note{font:400 15px Arial,sans-serif;fill:#3D556D}.small{font:400 13px Arial,sans-serif;fill:#526174}</style>',
        '<rect width="1920" height="1080" fill="#f6f8fb"/>',
        '<rect width="1920" height="12" fill="#00A6A6"/>',
        '<text x="70" y="70" class="title">RICE-карта: движение задач в формате блок-схемы</text>',
        '<text x="70" y="104" class="subtitle">Стрелка показывает передачу результата. Текст внутри блока — действие роли в этот момент.</text>',
        '<text x="70" y="154" class="section">ОСНОВНОЙ ПОТОК ЗАДАЧ</text>',
        '<rect x="70" y="174" width="1650" height="50" rx="12" fill="#e5f7f5"/>',
        '<text x="94" y="205" class="note">Цель и бюджет → заказ клиента → поставка → приёмка → операция в системе → учёт и обратный статус</text>',
        '<text x="70" y="266" class="section">РОЛИ И ДЕЙСТВИЯ</text>',
        '<rect x="744" y="488" width="704" height="228" rx="22" fill="#eef4f8" stroke="#cfdee8" stroke-width="2" stroke-dasharray="6 6"/>',
        '<text x="770" y="523" class="section">ПАРАЛЛЕЛЬНЫЙ КОНТУР ПОСТАВКИ И ПРИЁМКИ</text>',
    ]
    parts.extend(node_svg(node) for node in NODES)

    # Основной контур и две связи, которые идут параллельно с работой с поставщиком.
    parts.extend(
        (
            arrow('M 340 369 H 420', 352, 351, 'цели и KPI'),
            arrow('M 720 369 H 1480', 960, 351, 'заказ и требования к операции'),
            arrow('M 570 434 V 490 H 920 V 560', 740, 478, 'потребность в товаре'),
            arrow('M 1070 625 H 1120', 1080, 607, 'поставка и УПД'),
            arrow('M 1420 625 H 1450 V 434 H 1480', 1270, 606, 'остатки и коды'),
            arrow('M 1630 434 V 720', 1642, 579, 'данные сделки'),
            arrow('M 1480 785 H 118 V 434', 680, 770, 'статус проведения', dashed=True),
            arrow('M 720 402 V 886 H 1460 V 785 H 1480', 1035, 873, 'условия оплаты', dashed=True),
        )
    )
    parts.extend(
        (
            '<rect x="70" y="932" width="1780" height="76" rx="14" fill="#fff" stroke="#d6e0e8" stroke-width="2"/>',
            '<circle cx="99" cy="962" r="8" fill="#00A6A6"/><text x="118" y="967" class="small">Сплошная стрелка — обязательная передача результата.</text>',
            '<path d="M 500 962 H 568" class="arrow" stroke-dasharray="9 7"/><text x="582" y="967" class="small">Пунктир — обратная связь или параллельное согласование.</text>',
            '<text x="94" y="994" class="small">Контроль: поставка принимается только после сверки документов и кодов; сделка завершается после проверки оплаты и отражения в учёте.</text>',
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
