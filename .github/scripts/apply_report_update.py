from pathlib import Path

index = Path('index.html')
text = index.read_text(encoding='utf-8')

if 'sum-completed-op-steps' not in text:
    ops_line = '          <div class="sline"><span class="sl">Operations</span><span class="sv" id="sum-ops">—</span></div>'
    report_lines = (
        ops_line + '\n'
        '          <div class="sline"><span class="sl">Completed Op Steps</span><span class="sv g" id="sum-completed-op-steps">—</span></div>\n'
        '          <div class="sline"><span class="sl">Completed by Op</span><span class="sv" id="sum-completed-by-op">—</span></div>'
    )
    text = text.replace(ops_line, report_lines)

if 'function completedOperationStats()' not in text:
    marker = 'function travelerFlowText(w){'
    helper = """function completedOperationStats(){
  const route=routeOps().map(o=>String(o.num));
  const byOp={};
  route.forEach(op=>byOp[op]=0);
  let total=0;
  workOrders.forEach(raw=>{
    const w=normalizeWO(raw);
    const done=new Set(Array.isArray(w.completedOps)?w.completedOps.map(String):[]);
    if(w.status==='Complete'||w.currentOp==='COMPLETE') route.forEach(op=>done.add(op));
    done.forEach(op=>{
      if(!op) return;
      byOp[op]=(byOp[op]||0)+1;
      total++;
    });
  });
  const possible=route.length*workOrders.length;
  const byOpText=route.length
    ? route.map(op=>`OP ${op}: ${byOp[op]||0}`).join(' · ')
    : '—';
  return {total,possible,byOpText};
}
"""
    text = text.replace(marker, helper + marker)

if 'const completedStats=completedOperationStats();' not in text:
    text = text.replace(
        '  const woQty=workOrderQty();\n  let totalOrder=0;',
        '  const woQty=workOrderQty();\n  const completedStats=completedOperationStats();\n  let totalOrder=0;'
    )

if 'sum-completed-op-steps' in text and 'completedStats.possible' not in text:
    text = text.replace(
        "  document.getElementById('sum-ops').textContent=ops.length;\n  document.getElementById('sum-tools').textContent=tools.length;",
        "  document.getElementById('sum-ops').textContent=ops.length;\n  document.getElementById('sum-completed-op-steps').textContent=completedStats.possible?`${completedStats.total}/${completedStats.possible}`:(completedStats.total||'—');\n  document.getElementById('sum-completed-by-op').textContent=completedStats.byOpText;\n  document.getElementById('sum-tools').textContent=tools.length;"
    )

index.write_text(text, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8')
sw_text = sw_text.replace('cnc-cell-planner-v10-inhouse-tooling', 'cnc-cell-planner-v11-report-completed-ops')
sw.write_text(sw_text, encoding='utf-8')

Path('.github/workflows/apply-report-update.yml').unlink(missing_ok=True)
Path('.github/scripts/apply_report_update.py').unlink(missing_ok=True)
try:
    Path('.github/scripts').rmdir()
except OSError:
    pass
