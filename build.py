"""services.yaml から AWS サービス一覧の index.html を作る。

使い方:
    uv run --with pyyaml --with diagrams python build.py              # index.html を作る
    uv run --with pyyaml --with diagrams python build.py --list-icons # 使えるアイコン名の一覧

アイコンは icons/<分類>/<名前>.png を優先して使い、無ければ diagrams ライブラリ
同梱の AWS アイコンを icons/ にコピーしてから使う。一度コピーされたアイコンは
diagrams が無くても使える（その場合は `uv run --with pyyaml python build.py` でよい）。
"""

import base64
import html
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).parent
DATA = ROOT / "services.yaml"
ICONS = ROOT / "icons"
OUT = ROOT / "index.html"
TEMPLATE = ROOT / "template.html"

REQUIRED = ("id", "name", "category", "icon", "summary")


def diagrams_resources() -> Path | None:
    try:
        import diagrams
    except ImportError:
        return None
    return Path(diagrams.__file__).parent.parent / "resources" / "aws"


def resolve_icon(key: str) -> Path | None:
    local = ICONS / f"{key}.png"
    if local.exists():
        return local
    res = diagrams_resources()
    if res and (res / f"{key}.png").exists():
        local.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(res / f"{key}.png", local)
        return local
    return None


def list_icons() -> None:
    res = diagrams_resources()
    if not res:
        sys.exit("diagrams が見つかりません。`uv run --with diagrams ...` で実行してください。")
    for p in sorted(res.glob("*/*.png")):
        if not p.stem.endswith("-rounded"):
            print(f"{p.parent.name}/{p.stem}")


def normalize_categories(raw: dict) -> dict:
    """categories の値は「表示名の文字列」でも「label / columns / points の辞書」でもよい。"""
    cats = {}
    for key, v in (raw or {}).items():
        if isinstance(v, str):
            v = {"label": v}
        cats[key] = {
            "label": v.get("label", key),
            "columns": v.get("columns") or [],
            "points": v.get("points") or [],
        }
    return cats


def validate(data: dict, cats: dict) -> list[str]:
    errors, seen = [], set()
    for i, s in enumerate(data.get("services", [])):
        label = s.get("id") or f"#{i + 1}"
        for k in REQUIRED:
            if not s.get(k):
                errors.append(f"{label}: '{k}' がありません")
        if s.get("id") in seen:
            errors.append(f"{label}: id が重複しています")
        seen.add(s.get("id"))
        if s.get("category") and s["category"] not in cats:
            errors.append(f"{label}: category '{s['category']}' が categories にありません")
        elif s.get("attrs"):
            unknown = set(s["attrs"]) - set(cats[s["category"]]["columns"])
            if unknown:
                errors.append(f"{label}: attrs の {sorted(unknown)} がカテゴリの columns にありません")
    return errors


def e(text) -> str:
    return html.escape(str(text), quote=True)


def icon_css(s: dict) -> str:
    icon = resolve_icon(s["icon"])
    if not icon:
        print(f"警告: {s['id']} のアイコン '{s['icon']}' が見つかりません", file=sys.stderr)
        return ""
    b64 = base64.b64encode(icon.read_bytes()).decode()
    return f'.i-{s["id"]}{{background-image:url(data:image/png;base64,{b64})}}'


def icon_el(s: dict, cls: str) -> str:
    return f'<span class="{cls} i-{e(s["id"])}" aria-hidden="true"></span>'


def card(s: dict) -> str:
    img = icon_el(s, "icon")

    keywords = s.get("keywords") or []
    tags = s.get("tags") or []
    search = " ".join(
        [s["name"], s.get("short", ""), s["summary"], s.get("use_when", ""), s.get("compare", ""),
         *(s.get("attrs") or {}).values(), *keywords, *tags]
    ).lower()

    parts = [
        f'<article class="card" id="svc-{e(s["id"])}" data-search="{e(search)}">',
        img,
        '<div class="body">',
        '<header class="head">',
        f'<h3 class="name">{e(s["name"])}</h3>',
    ]
    if s.get("short"):
        parts.append(f'<span class="short">{e(s["short"])}</span>')
    for t in tags:
        parts.append(f'<span class="tag">{e(t)}</span>')
    parts.append("</header>")
    parts.append(f'<p class="summary">{e(s["summary"])}</p>')
    if s.get("use_when"):
        parts.append(f'<p class="use"><b>使う場面</b>{e(s["use_when"])}</p>')
    if keywords:
        chips = "".join(f"<li>{e(k)}</li>" for k in keywords)
        parts.append(f'<ul class="kw" aria-label="試験キーワード">{chips}</ul>')
    if s.get("compare"):
        parts.append(f'<p class="compare"><b>違い</b>{e(s["compare"])}</p>')
    parts.append("</div></article>")
    return "".join(parts)


def compare_block(cat: dict, items: list[dict]) -> str:
    points = "".join(f"<li>{e(p)}</li>" for p in cat["points"])
    head = "".join(f"<th>{e(c)}</th>" for c in cat["columns"])
    rows = []
    for s in items:
        attrs = s.get("attrs") or {}
        cells = "".join(f"<td>{e(attrs.get(c, '—'))}</td>" for c in cat["columns"])
        rows.append(
            f'<tr data-for="svc-{e(s["id"])}">'
            f'<th scope="row"><a class="svc" href="#svc-{e(s["id"])}">{icon_el(s, "mini")}'
            f'<span class="name">{e(s["name"])}</span></a></th>'
            f'{cells}<td class="use-cell">{e(s.get("use_when", "—"))}</td></tr>'
        )
    parts = ['<div class="compare-block">']
    if points:
        parts.append(f'<div class="points"><h3>使い分けのポイント</h3><ul>{points}</ul></div>')
    parts.append(
        '<div class="table-scroll"><table class="cmp">'
        f'<thead><tr><th>サービス</th>{head}<th>どういうときに使うか</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div></div>'
    )
    return "".join(parts)


def build() -> None:
    data = yaml.safe_load(DATA.read_text(encoding="utf-8"))
    cats = normalize_categories(data.get("categories"))
    errors = validate(data, cats)
    if errors:
        sys.exit("services.yaml にエラーがあります:\n  " + "\n  ".join(errors))

    services = data["services"]
    sections, nav = [], []
    for key, cat in cats.items():
        label = cat["label"]
        items = [s for s in services if s["category"] == key]
        if not items:
            continue
        nav.append(
            f'<button type="button" class="chip" data-cat="{e(key)}" aria-pressed="false">'
            f'{e(label)}<span class="n">{len(items)}</span></button>'
        )
        cards = "".join(card(s) for s in items)
        sections.append(
            f'<section class="cat" data-cat="{e(key)}" id="cat-{e(key)}">'
            f'<h2><span>{e(label)}</span><span class="count">{len(items)}</span></h2>'
            f'{compare_block(cat, items)}'
            f'<div class="grid">{cards}</div></section>'
        )
    icon_styles = "\n".join(filter(None, (icon_css(s) for s in services)))

    page = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{TOTAL}}", str(len(services)))
        .replace("{{NAV}}", "".join(nav))
        .replace("{{SECTIONS}}", "".join(sections))
        .replace("/*{{ICON_CSS}}*/", icon_styles)
    )
    OUT.write_text(page, encoding="utf-8")
    print(f"{OUT.name} を作りました（{len(services)} サービス / {len(nav)} カテゴリ）")


if __name__ == "__main__":
    if "--list-icons" in sys.argv:
        list_icons()
    else:
        build()
