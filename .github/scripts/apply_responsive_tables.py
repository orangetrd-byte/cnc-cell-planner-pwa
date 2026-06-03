from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
sw_path = ROOT / "sw.js"
script_path = ROOT / ".github" / "scripts" / "apply_responsive_tables.py"
workflow_path = ROOT / ".github" / "workflows" / "apply-responsive-tables.yml"

html = index_path.read_text(encoding="utf-8")
sw = sw_path.read_text(encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)

html = replace_once(
    html,
    "tbody td input:focus,tbody td select:focus{border-bottom-color:var(--accent)}\n.op-badge",
    "tbody td input:focus,tbody td select:focus{border-bottom-color:var(--accent)}\n.stack-table td::before{display:none}\n.op-badge",
    "stack table base style",
)

html = replace_once(
    html,
    "@media(max-width:900px){.two-col{grid-template-columns:1fr}.stat-grid{grid-template-columns:1fr 1fr}.sum-grid{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr 1fr}.app-nav{top:66px}}\n@media(max-width:1100px)",
    "@media(max-width:900px){.two-col{grid-template-columns:1fr}.stat-grid{grid-template-columns:1fr 1fr}.sum-grid{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr 1fr}.app-nav{top:66px}}\n@media(min-width:701px) and (max-width:1100px){.stack-table th:first-child,.stack-table td:first-child{position:sticky;left:0;background:var(--surface);z-index:2}.stack-table thead th:first-child{background:var(--surface2);z-index:3}.stack-table th:nth-child(2),.stack-table td:nth-child(2){position:sticky;left:76px;background:var(--surface);z-index:2}.stack-table thead th:nth-child(2){background:var(--surface2);z-index:3}}\n@media(max-width:1100px)",
    "tablet sticky stack table style",
)

html = replace_once(
    html,
    "@media(max-width:600px){body{padding-bottom:70px}header{padding:11px 12px}.htitles h1{font-size:15px}.hright{gap:5px}.app-nav{position:fixed;top:auto;bottom:0;left:0;right:0;z-index:300;padding:8px 10px calc(8px + env(safe-area-inset-bottom));border-top:1px solid var(--border);border-bottom:none;background:rgba(255,255,255,.96);box-shadow:0 -2px 12px rgba(0,0,0,.08)}.nav-btn{padding:9px 10px;min-width:82px}.main{padding-bottom:20px}.stat-grid{grid-template-columns:1fr 1fr}.frow{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr}.wo-bulk-grid{grid-template-columns:1fr}.release-list{grid-template-columns:1fr}}",
    "@media(max-width:600px){body{padding-bottom:70px}header{padding:11px 12px}.htitles h1{font-size:15px}.hright{gap:5px}.app-nav{position:fixed;top:auto;bottom:0;left:0;right:0;z-index:300;padding:8px 10px calc(8px + env(safe-area-inset-bottom));border-top:1px solid var(--border);border-bottom:none;background:rgba(255,255,255,.96);box-shadow:0 -2px 12px rgba(0,0,0,.08)}.nav-btn{padding:9px 10px;min-width:82px}.main{padding-bottom:20px}.stat-grid{grid-template-columns:1fr 1fr}.frow{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr}.wo-bulk-grid{grid-template-columns:1fr}.release-list{grid-template-columns:1fr}}\n@media(max-width:700px){.tbl-wrap{overflow:visible;border:none}.stack-table{border-collapse:separate;border-spacing:0 10px}.stack-table thead{display:none}.stack-table tbody,.stack-table tr,.stack-table td{display:block;width:100%}.stack-table tbody tr{background:#fff;border:1px solid var(--border);border-radius:var(--radius-sm);box-shadow:var(--shadow-sm);padding:9px 10px;margin-bottom:10px}.stack-table tbody tr.ready-row{background:var(--green-light);border-color:rgba(40,167,69,.25)}.stack-table tbody tr.hold-row{background:var(--yellow-light);border-color:rgba(245,158,11,.28)}.stack-table tbody tr.empty-row{box-shadow:none;padding:0}.stack-table tbody tr.empty-row td{display:block;text-align:center}.stack-table tbody td{display:grid;grid-template-columns:94px minmax(0,1fr);gap:9px;align-items:center;border-bottom:1px solid rgba(0,0,0,.05);padding:8px 2px}.stack-table tbody td:last-child{border-bottom:none}.stack-table td::before{content:attr(data-label);display:block;color:var(--text-dim);font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.4px}.stack-table td input,.stack-table td select{background:var(--surface2);border:1px solid var(--border2);border-radius:var(--radius-sm);padding:8px 9px}.stack-table td .cv{font-size:11px;line-height:1.55}.stack-table td .btn{width:100%;justify-content:center}}",
    "phone stack table cards",
)

html = replace_once(html, '<table><thead><tr><th>WO #</th>', '<table class="stack-table"><thead><tr><th>WO #</th>', "WO stack table class")
html = replace_once(html, '<table><thead><tr><th>Op #</th>', '<table class="stack-table"><thead><tr><th>Op #</th>', "op stack table class")

wo_replacements = [
    ("        <td>\n          <input type=\"text\"\n                 value=\"${escHtml(w.num)}\"", "        <td data-label=\"WO #\">\n          <input type=\"text\"\n                 value=\"${escHtml(w.num)}\"", "WO label"),
    ("        <td>\n          <input type=\"text\"\n                 value=\"${escHtml(w.batch)}\"", "        <td data-label=\"Batch / Part\">\n          <input type=\"text\"\n                 value=\"${escHtml(w.batch)}\"", "batch label"),
    ("        <td>\n          <input type=\"number\"\n                 value=\"${escHtml(w.qty)}\"", "        <td data-label=\"Qty\">\n          <input type=\"number\"\n                 value=\"${escHtml(w.qty)}\"", "qty label"),
    ("        <td>\n          <select onchange=\"woCh(${w.id},'currentOp',this.value)\">", "        <td data-label=\"Current Op\">\n          <select onchange=\"woCh(${w.id},'currentOp',this.value)\">", "current op label"),
    ("        <td>\n          <input type=\"number\"\n                 value=\"${doneAtOp}\"", "        <td data-label=\"Done @ Op\">\n          <input type=\"number\"\n                 value=\"${doneAtOp}\"", "done label"),
    ("        <td><span class=\"cv\">${travelerFlowText(w)}</span></td>", "        <td data-label=\"Flow\"><span class=\"cv\">${travelerFlowText(w)}</span></td>", "flow label"),
    ("        <td>\n          <select onchange=\"woCh(${w.id},'status',this.value)\">", "        <td data-label=\"Status\">\n          <select onchange=\"woCh(${w.id},'status',this.value)\">", "status label"),
    ("        <td>\n          <button class=\"btn btn-primary btn-sm\"", "        <td data-label=\"Advance\">\n          <button class=\"btn btn-primary btn-sm\"", "advance label"),
    ("        <td>\n          <button class=\"btn btn-red btn-sm\"", "        <td data-label=\"Remove\">\n          <button class=\"btn btn-red btn-sm\"", "remove label"),
]
for old, new, label in wo_replacements:
    html = replace_once(html, old, new, label)

op_pairs = [
    ('<td><span class="op-badge">OP ${o.num}</span></td>', '<td data-label="Op #"><span class="op-badge">OP ${o.num}</span></td>', 'op num label'),
    ('<td><input type="text" value="${escHtml(o.desc)}"', '<td data-label="Description"><input type="text" value="${escHtml(o.desc)}"', 'op desc label'),
    ('<td><input type="text" value="${escHtml(o.machine)}"', '<td data-label="Machine"><input type="text" value="${escHtml(o.machine)}"', 'op machine label'),
    ('<td><input type="number" value="${escHtml(o.cycle)}"', '<td data-label="Cycle Time"><input type="number" value="${escHtml(o.cycle)}"', 'op cycle label'),
    ('<td><select onchange="opCh(${o.id},\'cycleUnit\',this.value)"', '<td data-label="Cycle Unit"><select onchange="opCh(${o.id},\'cycleUnit\',this.value)"', 'op cycle unit label'),
    ('<td><input type="number" value="${escHtml(o.setup)}"', '<td data-label="Setup Time"><input type="number" value="${escHtml(o.setup)}"', 'op setup label'),
    ('<td><select onchange="opCh(${o.id},\'setupUnit\',this.value)"', '<td data-label="Setup Unit"><select onchange="opCh(${o.id},\'setupUnit\',this.value)"', 'op setup unit label'),
    ('<td><input type="number" value="${escHtml(o.moveQty||1)}"', '<td data-label="Move Qty"><input type="number" value="${escHtml(o.moveQty||1)}"', 'op move label'),
    ('<td><select onchange="opCh(${o.id},\'shiftCount\',this.value)"', '<td data-label="Shifts"><select onchange="opCh(${o.id},\'shiftCount\',this.value)"', 'op shifts label'),
    ('<td><select onchange="opCh(${o.id},\'type\',this.value)"', '<td data-label="Type"><select onchange="opCh(${o.id},\'type\',this.value)"', 'op type label'),
    ('<td><button class="btn btn-red btn-sm" onclick="removeOp(${o.id})">', '<td data-label="Remove"><button class="btn btn-red btn-sm" onclick="removeOp(${o.id})">', 'op remove label'),
]
for old, new, label in op_pairs:
    html = replace_once(html, old, new, label)

sw = replace_once(sw, "cnc-cell-planner-v15-operation-shifts", "cnc-cell-planner-v16-responsive-tables", "service worker v16")

index_path.write_text(html, encoding="utf-8")
sw_path.write_text(sw, encoding="utf-8")

script_path.unlink(missing_ok=True)
workflow_path.unlink(missing_ok=True)
try:
    script_path.parent.rmdir()
except OSError:
    pass
