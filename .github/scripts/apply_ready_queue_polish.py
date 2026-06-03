from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
sw_path = ROOT / "sw.js"
script_path = ROOT / ".github" / "scripts" / "apply_ready_queue_polish.py"
workflow_path = ROOT / ".github" / "workflows" / "apply-ready-queue-polish.yml"

html = index_path.read_text(encoding="utf-8")
sw = sw_path.read_text(encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)

html = replace_once(
    html,
    ".cv{color:var(--green);font-weight:600;font-family:var(--mono)}\n.cv-alert{color:var(--red);font-weight:600;font-family:var(--mono)}",
    ".cv{color:var(--green);font-weight:600;font-family:var(--mono)}\n.cv-alert{color:var(--red);font-weight:600;font-family:var(--mono)}\n.ready-row{background:var(--green-light)}\n.ready-row:hover{background:#dff0e3}\n.hold-row{background:var(--yellow-light)}\n.release-panel{display:none;margin-bottom:11px;background:var(--green-light);border:1px solid rgba(40,167,69,.24);border-radius:var(--radius-sm);padding:11px}\n.release-panel.show{display:block}\n.release-title{font-size:10px;font-weight:700;color:var(--green);text-transform:uppercase;letter-spacing:.5px;margin-bottom:7px}\n.release-list{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}\n.release-card{background:#fff;border:1px solid rgba(40,167,69,.22);border-radius:var(--radius-sm);padding:9px 10px;font-size:12px;line-height:1.45}\n.release-card b{font-family:var(--mono);color:var(--text)}\n.release-meta{display:block;color:var(--text-dim);font-size:11px;margin-top:2px}\n.ready-pill{display:inline-block;background:var(--green);color:#fff;border-radius:6px;padding:2px 7px;font-family:var(--mono);font-size:10px;font-weight:600;white-space:nowrap}",
    "ready queue styles",
)

html = replace_once(
    html,
    ".wo-bulk-grid{grid-template-columns:1fr}}",
    ".wo-bulk-grid{grid-template-columns:1fr}.release-list{grid-template-columns:1fr}}",
    "mobile ready queue styles",
)

html = replace_once(
    html,
    '      <div class="hchips" id="woSummary" style="margin-bottom:11px"></div>',
    '      <div class="release-panel" id="readyQueue"></div>\n      <div class="hchips" id="woSummary" style="margin-bottom:11px"></div>',
    "ready queue panel",
)

html = replace_once(
    html,
    "function completedOpsText(w){",
    "function woCanAdvance(w){\n  const cur=w.currentOp || (w.status==='Complete' ? 'COMPLETE' : firstRouteOp());\n  return !!cur&&cur!=='COMPLETE'&&w.status!=='Hold'&&w.status!=='Complete'&&woReleaseReady(w);\n}\nfunction completedOpsText(w){",
    "woCanAdvance helper",
)

html = replace_once(
    html,
    "  const release=w.currentOp==='COMPLETE'?'Complete':(woReleaseReady(w)?'Next ready':`Needs ${Math.max(0,move-done)} more`);\n  return `Completed: ${completedOpsText(w)}<br>Current: ${cur}<br>Next: ${nextText}<br><span style=\"color:${woReleaseReady(w)||w.currentOp==='COMPLETE'?'var(--green)':'var(--text-dim)'}\">${release}${w.currentOp!=='COMPLETE'?` (${done}/${move})`:''}</span>`;\n}",
    "  const release=w.currentOp==='COMPLETE'?'Complete':(woCanAdvance(w)?'<span class=\"ready-pill\">Ready</span>':`Needs ${Math.max(0,move-done)} more`);\n  return `Completed: ${completedOpsText(w)}<br>Current: ${cur}<br>Next: ${nextText}<br><span style=\"color:${woCanAdvance(w)||w.currentOp==='COMPLETE'?'var(--green)':'var(--text-dim)'}\">${release}${w.currentOp!=='COMPLETE'?` (${done}/${move})`:''}</span>`;\n}\nfunction renderReadyQueue(){\n  const el=document.getElementById('readyQueue');\n  if(!el) return;\n  const ready=workOrders.map(normalizeWO).filter(woCanAdvance);\n  if(!ready.length){\n    el.classList.remove('show');\n    el.innerHTML='';\n    return;\n  }\n  const cards=ready.map(w=>{\n    const next=nextRouteOp(w.currentOp);\n    const nextText=next==='COMPLETE'?'COMPLETE':`OP ${next}`;\n    const op=ops.find(o=>String(o.num)===String(w.currentOp));\n    const machine=(op?.machine||'Unassigned').trim()||'Unassigned';\n    return `<div class=\"release-card\"><b>${escHtml(w.num||'WO')}</b> ${escHtml(w.batch||'Unbatched')}<span class=\"release-meta\">OP ${escHtml(w.currentOp)} ready for ${escHtml(nextText)} &middot; ${escHtml(machine)}</span></div>`;\n  }).join('');\n  el.innerHTML=`<div class=\"release-title\">${ready.length} ready for next operation</div><div class=\"release-list\">${cards}</div>`;\n  el.classList.add('show');\n}",
    "traveler flow and ready queue",
)

html = replace_once(
    html,
    "  route.forEach(o=>chips.push(`<div class=\"chip\">OP ${o.num}: ${counts['OP '+o.num]||0}</div>`));\n  chips.push(`<div class=\"chip\">Complete: ${counts.Complete||0}</div>`);",
    "  route.forEach(o=>chips.push(`<div class=\"chip\">OP ${o.num}: ${counts['OP '+o.num]||0}</div>`));\n  chips.push(`<div class=\"chip\">Ready: ${workOrders.map(normalizeWO).filter(woCanAdvance).length}</div>`);\n  chips.push(`<div class=\"chip\">Complete: ${counts.Complete||0}</div>`);",
    "ready summary chip",
)

html = replace_once(
    html,
    "  workOrders=workOrders.map(normalizeWO);\n  renderWOSummary();",
    "  workOrders=workOrders.map(normalizeWO);\n  renderReadyQueue();\n  renderWOSummary();",
    "render ready queue call",
)

html = replace_once(
    html,
    "    const canAdvance=!!cur&&cur!=='COMPLETE'&&w.status!=='Hold'&&w.status!=='Complete'&&woReleaseReady(w);\n    const doneAtOp=woCurrentDone(w);\n    const releaseTitle=cur==='COMPLETE'?'Complete':`Move Qty ${opMoveQty(cur)}`;\n\n    return `\n      <tr>",
    "    const canAdvance=woCanAdvance(w);\n    const doneAtOp=woCurrentDone(w);\n    const releaseTitle=cur==='COMPLETE'?'Complete':`Move Qty ${opMoveQty(cur)}`;\n    const rowClass=canAdvance?' class=\"ready-row\"':(w.status==='Hold'?' class=\"hold-row\"':'');\n\n    return `\n      <tr${rowClass}>",
    "ready row class",
)

sw = replace_once(
    sw,
    "cnc-cell-planner-v13-batch-status-mobile-wo",
    "cnc-cell-planner-v14-ready-queue-polish",
    "service worker v14 cache",
)

index_path.write_text(html, encoding="utf-8")
sw_path.write_text(sw, encoding="utf-8")

script_path.unlink(missing_ok=True)
workflow_path.unlink(missing_ok=True)
try:
    script_path.parent.rmdir()
except OSError:
    pass
