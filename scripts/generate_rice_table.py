#!/usr/bin/env python3
"""Generate an editable SVG RICE task-flow table for ООО «ТоргМаркет»."""

from __future__ import annotations

from html import escape
from pathlib import Path
from textwrap import wrap


OUTPUT = Path(__file__).resolve().parents[1] / "artifacts" / "rice_process_table.svg"

WIDTH, HEIGHT = 1920, 1080
MARGIN = 70
TABLE_Y = 254
HEADER_HEIGHT = 62
ROW_HEIGHT = 108
COLUMNS = (
    (310, "Роль"),
    (390, "Инициирует задачу"),
    (355, "Передаёт результат"),
    (455, "Что происходит параллельно"),
    (270, "Контрольная точка"),
)

# В таблицу намеренно внесены только должности — без имён сотрудников.
ROWS = (
    (
        "Главный директор",
        "Утверждает цели, бюджет и приоритеты проекта.",
        "Коммерческому директору: план продаж и KPI.",
        "Получает статусы продаж, поставок, финансов и ИТ; снимает блокеры.",
        "Решение принято, ресурсы распределены.",
    ),
    (
        "Коммерческий директор",
        "Формирует спрос, предложение для клиента и условия продажи.",
        "Менеджеру по поставщикам: потребность. Бухгалтеру: условия оплаты. ИТ: требования к операции.",
        "Ведёт переговоры с клиентом и уточняет номенклатуру, цену, количество.",
        "Заказ согласован с клиентом.",
    ),
    (
        "Менеджер по работе с поставщиками",
        "Запрашивает наличие, цену, сроки и документы у поставщиков.",
        "Логисту: график и состав поставки. Бухгалтеру: УПД/счёт.",
        "Подтверждает сроки поставки и отслеживает изменения у поставщика.",
        "Поставка подтверждена.",
    ),
    (
        "Логист",
        "Принимает товар, сверяет количество, документы и коды маркировки.",
        "ИТ: данные о товаре и кодах. Коммерческому директору: доступный остаток.",
        "Размещает товар на складе, фиксирует расхождения и готовит отгрузку.",
        "Товар доступен для продажи.",
    ),
    (
        "ИТ-специалист",
        "Настраивает БД и интеграцию с «Честным знаком»; проверяет статусы кодов.",
        "Коммерческому директору и бухгалтеру: подтверждение корректной операции.",
        "Система резервирует остаток, создаёт документ и ведёт журнал изменений.",
        "Данные и коды валидны.",
    ),
    (
        "Главный бухгалтер",
        "Проверяет первичные документы, НДС, оплату и итоговую сумму сделки.",
        "Всем участникам: статус проведения и замечания по документам.",
        "Отражает операцию в учёте, сверяет оплату и хранит комплект документов.",
        "Сделка проведена в учёте.",
    ),
)


def lines(text: str, width: int) -> list[str]:
    """Wrap a cell to a predictable number of SVG text lines."""
    return wrap(text, width=width, break_long_words=False, break_on_hyphens=False)


def text_block(x: int, y: int, value: str, width: int, *, bold: bool = False) -> str:
    font_weight = "700" if bold else "400"
    content = []
    for index, line in enumerate(lines(value, width)):
        content.append(
            f'<text x="{x}" y="{y + index * 19}" class="cell" font-weight="{font_weight}">{escape(line)}</text>'
        )
    return "\n".join(content)


def build_svg() -> str:
    table_width = sum(width for width, _ in COLUMNS)
    stage_labels = ("Планирование", "Заказ", "Поставка", "Учёт в системе", "Продажа и контроль")
    stage_width = 356
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title description">',
        "<title id=\"title\">RICE-карта движения задач ООО «ТоргМаркет»</title>",
        "<desc id=\"description\">Таблица ролей и передачи задач между сотрудниками без указания имён.</desc>",
        "<style>.title{font:700 36px Arial,sans-serif;fill:#132238}.subtitle{font:400 18px Arial,sans-serif;fill:#5a6879}.stage{font:700 15px Arial,sans-serif;fill:#28517a}.head{font:700 16px Arial,sans-serif;fill:#fff}.cell{font:400 15px Arial,sans-serif;fill:#17283d}.note{font:400 14px Arial,sans-serif;fill:#526174}.legend{font:700 14px Arial,sans-serif;fill:#28517a}</style>",
        '<rect width="1920" height="1080" fill="#f6f8fb"/>',
        '<rect x="0" y="0" width="1920" height="12" fill="#00a6a6"/>',
        '<text x="70" y="70" class="title">RICE-карта: движение задач в ООО «ТоргМаркет»</text>',
        '<text x="70" y="103" class="subtitle">Схема показывает, кто запускает работу, кому передаёт результат и какие процессы идут одновременно.</text>',
        '<text x="70" y="133" class="subtitle">Роли указаны без персональных данных. Контрольные точки формируют единый цикл: от цели до отражения сделки.</text>',
        '<text x="70" y="181" class="legend">ЦЕПОЧКА ПРОЦЕССА</text>',
    ]

    for index, label in enumerate(stage_labels):
        x = MARGIN + index * stage_width
        parts.append(f'<rect x="{x}" y="198" width="{stage_width - 14}" height="34" rx="17" fill="#e1edf6"/>')
        parts.append(f'<text x="{x + 18}" y="220" class="stage">{label}</text>')
        if index < len(stage_labels) - 1:
            parts.append(f'<path d="M {x + stage_width - 4} 215 H {x + stage_width + 8}" stroke="#00a6a6" stroke-width="3"/>')
            parts.append(f'<path d="M {x + stage_width + 3} 210 L {x + stage_width + 10} 215 L {x + stage_width + 3} 220" fill="none" stroke="#00a6a6" stroke-width="3"/>')

    parts.append(f'<rect x="{MARGIN}" y="{TABLE_Y}" width="{table_width}" height="{HEADER_HEIGHT}" rx="10" fill="#1d4f7a"/>')
    x = MARGIN
    for width, label in COLUMNS:
        parts.append(f'<text x="{x + 16}" y="{TABLE_Y + 38}" class="head">{label}</text>')
        x += width

    for row_index, row in enumerate(ROWS):
        y = TABLE_Y + HEADER_HEIGHT + row_index * ROW_HEIGHT
        fill = "#ffffff" if row_index % 2 == 0 else "#eef4f8"
        parts.append(f'<rect x="{MARGIN}" y="{y}" width="{table_width}" height="{ROW_HEIGHT}" fill="{fill}"/>')
        parts.append(f'<rect x="{MARGIN}" y="{y}" width="7" height="{ROW_HEIGHT}" fill="#00a6a6"/>')
        x = MARGIN
        wrap_widths = (25, 35, 37, 46, 29)
        for cell_index, ((width, _), value, wrap_width) in enumerate(zip(COLUMNS, row, wrap_widths)):
            parts.append(text_block(x + 16, y + 29, value, wrap_width, bold=cell_index == 0))
            x += width
        for boundary in range(1, len(COLUMNS)):
            line_x = MARGIN + sum(width for width, _ in COLUMNS[:boundary])
            parts.append(f'<path d="M {line_x} {y} V {y + ROW_HEIGHT}" stroke="#d6e0e8" stroke-width="1"/>')
        parts.append(f'<path d="M {MARGIN} {y + ROW_HEIGHT} H {MARGIN + table_width}" stroke="#d6e0e8" stroke-width="1"/>')

    parts.extend(
        (
            '<rect x="70" y="986" width="1780" height="46" rx="10" fill="#e5f7f5"/>',
            '<text x="92" y="1015" class="note">Правило работы: каждая передача фиксируется в системе или документе; при ошибке задача возвращается исполнителю на уточнение.</text>',
            "</svg>",
        )
    )
    return "\n".join(parts)


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(build_svg(), encoding="utf-8")
    print(f"Created {OUTPUT.relative_to(OUTPUT.parents[1])}")


if __name__ == "__main__":
    main()
