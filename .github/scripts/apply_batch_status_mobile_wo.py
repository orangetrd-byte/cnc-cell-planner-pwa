from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
sw_path = ROOT / "sw.js"
script_path = ROOT / ".github" / "scripts" / "apply_batch_status_mobile_wo.py"
workflow_path = ROOT / ".github" / "workflows" / "apply-batch-status-mobile-wo.yml"

html = index_path.read_text(encoding="utf-8")
sw = sw_path.read_text(encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)

html = replace_once(
    html,
    ".wo-bulk-grid{display:grid;grid-template-columns:1.4fr 1fr .75fr .75fr .85fr auto;gap:8px;align-items:end}",
    ".wo-bulk-grid{display:grid;grid-template-columns:1.4fr 1fr .65fr .7fr .8fr .9fr auto;gap:8px;align-items:end}",
    "batch grid columns",
)

html = replace_once(
    html,
    '<div class="field"><label>Qty Each</label><input type="number" id="woQtyEach" min="1" placeholder="10"></div>\n          <button class="btn btn-primary" onclick="createTravelerBatch()">Create Batch</button>',
    '<div class="field"><label>Qty Each</label><input type="number" id="woQtyEach" min="1" placeholder="10"></div>\n          <div class="field"><label>Status</label><select id="woBatchStatus"><option>Not Started</option><option>In Process</option><option>Hold</option><option>Complete</option></select></div>\n          <button class="btn btn-primary" onclick="createTravelerBatch()">Create Batch</button>',
    "batch status field",
)

html = replace_once(
    html,
    '<th>Batch / Part</th><th>WO #</th>',
    '<th>WO #</th><th>Batch / Part</th>',
    "mobile WO first header",
)

html = replace_once(
    html,
    "  const qty=parseInt(document.getElementById('woQtyEach')?.value)||0;\n  if(qty<1){ alert('Enter Qty Each before creating the batch.'); return; }",
    "  const qty=parseInt(document.getElementById('woQtyEach')?.value)||0;\n  const status=document.getElementById('woBatchStatus')?.value||'Not Started';\n  if(qty<1){ alert('Enter Qty Each before creating the batch.'); return; }",
    "batch status read",
)

html = replace_once(
    html,
    "  const width=Math.max(3,String(start+count-1).length);\n  for(let i=0;i<count;i++){",
    "  const width=Math.max(3,String(start+count-1).length);\n  const route=routeOps().map(o=>String(o.num));\n  for(let i=0;i<count;i++){",
    "batch route list",
)

html = replace_once(
    html,
    "    workOrders.push({id:woC,batch,num:`${prefix}${n}`,qty:String(qty),currentOp:firstRouteOp(),status:'Not Started',completedOps:[],opProgress:{}});",
    "    workOrders.push({\n      id:woC,\n      batch,\n      num:`${prefix}${n}`,\n      qty:String(qty),\n      currentOp:status==='Complete'?'COMPLETE':firstRouteOp(),\n      status,\n      completedOps:status==='Complete'?route:[],\n      opProgress:{}\n    });",
    "batch traveler status object",
)

old_cells = '''        <td>
          <input type="text"
                 value="${escHtml(w.batch)}"
                 placeholder="Part / batch"
                 oninput="woCh(${w.id},'batch',this.value)">
        </td>

        <td>
          <input type="text"
                 value="${escHtml(w.num)}"
                 placeholder="WO-001"
                 oninput="woCh(${w.id},'num',this.value)">
        </td>'''

new_cells = '''        <td>
          <input type="text"
                 value="${escHtml(w.num)}"
                 placeholder="WO-001"
                 oninput="woCh(${w.id},'num',this.value)">
        </td>

        <td>
          <input type="text"
                 value="${escHtml(w.batch)}"
                 placeholder="Part / batch"
                 oninput="woCh(${w.id},'batch',this.value)">
        </td>'''

html = replace_once(html, old_cells, new_cells, "WO first row cells")

sw = replace_once(
    sw,
    "cnc-cell-planner-v12-batch-travelers",
    "cnc-cell-planner-v13-batch-status-mobile-wo",
    "service worker cache name",
)

index_path.write_text(html, encoding="utf-8")
sw_path.write_text(sw, encoding="utf-8")

script_path.unlink(missing_ok=True)
workflow_path.unlink(missing_ok=True)
try:
    script_path.parent.rmdir()
except OSError:
    pass
