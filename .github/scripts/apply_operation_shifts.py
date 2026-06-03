from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
index_path = ROOT / "index.html"
sw_path = ROOT / "sw.js"
script_path = ROOT / ".github" / "scripts" / "apply_operation_shifts.py"
workflow_path = ROOT / ".github" / "workflows" / "apply-operation-shifts.yml"

html = index_path.read_text(encoding="utf-8")
sw = sw_path.read_text(encoding="utf-8")


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f"Missing expected block: {label}")
    return text.replace(old, new, 1)

html = replace_once(
    html,
    "<th>Move Qty</th><th>Type</th><th></th>",
    "<th>Move Qty</th><th>Shifts</th><th>Type</th><th></th>",
    "operation shifts header",
)
html = html.replace('colspan="10">No operations', 'colspan="11">No operations')

html = replace_once(
    html,
    '<div class="sline"><span class="sl">Machine Hours by Machine</span><span class="sv" id="sum-machine-hours">—</span></div>\n          <div class="sline"><span class="sl">Operations</span><span class="sv" id="sum-ops">—</span></div>',
    '<div class="sline"><span class="sl">Machine Hours by Machine</span><span class="sv" id="sum-machine-hours">—</span></div>\n          <div class="sline"><span class="sl">Shift Coverage by Op</span><span class="sv" id="sum-shift-coverage">—</span></div>\n          <div class="sline"><span class="sl">Bottleneck Calendar Load</span><span class="sv o" id="sum-bn-days">—</span></div>\n          <div class="sline"><span class="sl">Operations</span><span class="sv" id="sum-ops">—</span></div>',
    "report shift rows",
)

html = replace_once(
    html,
    "function shiftsPerDay(){\n  return Math.max(1,parseInt(document.getElementById('shiftsPerDay').value)||1);\n}\nfunction opCycleMin(o){",
    "function shiftsPerDay(){\n  return Math.max(1,parseInt(document.getElementById('shiftsPerDay').value)||1);\n}\nfunction opShiftCount(o){\n  return Math.max(1,Math.min(2,parseInt(o?.shiftCount)||1));\n}\nfunction opShiftLabel(o){\n  const count=opShiftCount(o);\n  return count===2?'2 shifts':'1 shift';\n}\nfunction opCycleMin(o){",
    "op shift helpers",
)

old_capacity = '''function opCapacity(o,parts=1,includeSetup=true,availability=1){
  const cycle=opCycleMin(o), setup=includeSetup?opSetupMin(o):0, net=netShiftMinutes()*Math.max(0,Math.min(1,availability||1));
  if(cycle<=0||net<=0) return null;
  const totalMin=setup+(Math.max(0,parts)*cycle);
  const shifts=Math.ceil(totalMin/net);
  const firstShiftParts=Math.max(0,Math.floor((net-setup)/cycle));
  const normalShiftParts=Math.max(0,Math.floor(net/cycle));
  return {op:o,cycle,setup,totalMin,shifts,firstShiftParts,normalShiftParts,setupPlusFirst:setup+cycle,fitsFirstPart:setup+cycle<=net};
}
function jobCapacity(parts,includeSetup=true,availability=1){
  const caps=ops.map(o=>opCapacity(o,parts,includeSetup,availability)).filter(Boolean);
  if(!caps.length) return null;
  const bottleneck=caps.reduce((slow,c)=>!slow||c.shifts>slow.shifts||c.totalMin>slow.totalMin?c:slow,null);
  const maxShifts=Math.max(...caps.map(c=>c.shifts));
  const maxHours=Math.max(...caps.map(c=>c.totalMin/60));
  return {caps,bottleneck,maxShifts,maxHours};
}
function operationHourStats(parts){
  const qty=Math.max(0,parts||0);
  const byMachine={};
  let total=0,bottleneck=0,bottleneckOp=null;
  ops.forEach(o=>{
    const cycle=opCycleMin(o), setup=opSetupMin(o);
    if(cycle<=0&&setup<=0) return;
    const hrs=(setup+(qty*cycle))/60;
    total+=hrs;
    const machine=(o.machine||'Unassigned').trim()||'Unassigned';
    byMachine[machine]=(byMachine[machine]||0)+hrs;
    if(hrs>bottleneck){ bottleneck=hrs; bottleneckOp=o; }
  });
  return {total,bottleneck,bottleneckOp,byMachine};
}'''

new_capacity = '''function opCapacity(o,parts=1,includeSetup=true,availability=1){
  const cycle=opCycleMin(o), setup=includeSetup?opSetupMin(o):0, net=netShiftMinutes()*Math.max(0,Math.min(1,availability||1));
  if(cycle<=0||net<=0) return null;
  const totalMin=setup+(Math.max(0,parts)*cycle);
  const shifts=Math.ceil(totalMin/net);
  const shiftCount=opShiftCount(o);
  const days=totalMin/(net*shiftCount);
  const calendarDays=Math.ceil(days);
  const firstShiftParts=Math.max(0,Math.floor((net-setup)/cycle));
  const normalShiftParts=Math.max(0,Math.floor(net/cycle));
  return {op:o,cycle,setup,totalMin,shifts,shiftCount,days,calendarDays,firstShiftParts,normalShiftParts,setupPlusFirst:setup+cycle,fitsFirstPart:setup+cycle<=net};
}
function jobCapacity(parts,includeSetup=true,availability=1){
  const caps=ops.map(o=>opCapacity(o,parts,includeSetup,availability)).filter(Boolean);
  if(!caps.length) return null;
  const bottleneck=caps.reduce((slow,c)=>!slow||c.days>slow.days||c.totalMin>slow.totalMin?c:slow,null);
  const maxShifts=Math.max(...caps.map(c=>c.shifts));
  const maxDays=Math.max(...caps.map(c=>c.days));
  const maxCalendarDays=Math.max(...caps.map(c=>c.calendarDays));
  const maxHours=Math.max(...caps.map(c=>c.totalMin/60));
  return {caps,bottleneck,maxShifts,maxDays,maxCalendarDays,maxHours};
}
function operationHourStats(parts){
  const qty=Math.max(0,parts||0);
  const byMachine={};
  const shiftLoad=[];
  let total=0,bottleneck=0,bottleneckOp=null,bottleneckDays=0,bottleneckDayOp=null;
  ops.forEach(o=>{
    const cycle=opCycleMin(o), setup=opSetupMin(o);
    if(cycle<=0&&setup<=0) return;
    const hrs=(setup+(qty*cycle))/60;
    const shiftCount=opShiftCount(o);
    const days=netShiftMinutes()>0?hrs/(netShiftMinutes()/60)/shiftCount:0;
    total+=hrs;
    const machine=(o.machine||'Unassigned').trim()||'Unassigned';
    byMachine[machine]=(byMachine[machine]||0)+hrs;
    if(hrs>bottleneck){ bottleneck=hrs; bottleneckOp=o; }
    if(days>bottleneckDays){ bottleneckDays=days; bottleneckDayOp=o; }
    shiftLoad.push({op:o,hrs,shiftCount,days});
  });
  const shiftCoverageText=shiftLoad.length
    ? shiftLoad.map(x=>`OP ${x.op.num}: ${opShiftLabel(x.op)}, ${x.days.toFixed(1)} day(s)`).join(' · ')
    : '—';
  return {total,bottleneck,bottleneckOp,bottleneckDays,bottleneckDayOp,byMachine,shiftLoad,shiftCoverageText};
}'''

html = replace_once(html, old_capacity, new_capacity, "capacity and operation shift stats")

html = replace_once(
    html,
    "  const finishShifts=actualMin>0&&cap>0&&remaining>0?Math.ceil(remaining/cap):(plan?plan.maxShifts:0);\n  const finishDays=finishShifts?Math.ceil(finishShifts/shiftsPerDay()):0;",
    "  const finishShifts=actualMin>0&&cap>0&&remaining>0?Math.ceil(remaining/cap):(plan?plan.maxShifts:0);\n  const finishDays=actualMin>0&&finishShifts?Math.ceil(finishShifts/shiftsPerDay()):(plan?plan.maxCalendarDays:0);",
    "progress mixed shift finish days",
)

html = replace_once(
    html,
    "  const stats=operationHourStats(tp);\n  const bn=stats.bottleneckOp;\n  const machineHours=Object.entries(stats.byMachine).map(([m,h])=>`${m}: ${h.toFixed(1)}h`).join(' · ');",
    "  const stats=operationHourStats(tp);\n  const bn=stats.bottleneckOp;\n  const bnDayOp=stats.bottleneckDayOp;\n  const machineHours=Object.entries(stats.byMachine).map(([m,h])=>`${m}: ${h.toFixed(1)}h`).join(' · ');",
    "summary bottleneck day op",
)

html = replace_once(
    html,
    "  document.getElementById('sum-machine-hours').textContent=machineHours||'—';\n  document.getElementById('sum-ops').textContent=ops.length;",
    "  document.getElementById('sum-machine-hours').textContent=machineHours||'—';\n  document.getElementById('sum-shift-coverage').textContent=stats.shiftCoverageText||'—';\n  document.getElementById('sum-bn-days').textContent=bnDayOp?`OP ${bnDayOp.num}: ${stats.bottleneckDays.toFixed(1)} working day(s) @ ${opShiftLabel(bnDayOp)}`:'—';\n  document.getElementById('sum-ops').textContent=ops.length;",
    "summary mixed shift rows",
)

html = replace_once(
    html,
    "  ops.push({id:opC,num,desc:'',machine:'',cycle:'',setup:'',cycleUnit:'min',setupUnit:'min',moveQty:1,type:'sequential'});",
    "  ops.push({id:opC,num,desc:'',machine:'',cycle:'',setup:'',cycleUnit:'min',setupUnit:'min',moveQty:1,shiftCount:1,type:'sequential'});",
    "new op shift count",
)

html = replace_once(
    html,
    "    <td><input type=\"number\" value=\"${escHtml(o.moveQty||1)}\" min=\"1\" step=\"1\" oninput=\"opCh(${o.id},'moveQty',this.value)\" style=\"width:70px\"></td>\n    <td><select onchange=\"opCh(${o.id},'type',this.value)\"><option value=\"sequential\" ${o.type==='sequential'?'selected':''}>Sequential</option><option value=\"parallel\" ${o.type==='parallel'?'selected':''}>Parallel</option></select></td>",
    "    <td><input type=\"number\" value=\"${escHtml(o.moveQty||1)}\" min=\"1\" step=\"1\" oninput=\"opCh(${o.id},'moveQty',this.value)\" style=\"width:70px\"></td>\n    <td><select onchange=\"opCh(${o.id},'shiftCount',this.value)\" style=\"width:82px\"><option value=\"1\" ${opShiftCount(o)===1?'selected':''}>1 shift</option><option value=\"2\" ${opShiftCount(o)===2?'selected':''}>2 shifts</option></select></td>\n    <td><select onchange=\"opCh(${o.id},'type',this.value)\"><option value=\"sequential\" ${o.type==='sequential'?'selected':''}>Sequential</option><option value=\"parallel\" ${o.type==='parallel'?'selected':''}>Parallel</option></select></td>",
    "operation shift select",
)

html = replace_once(
    html,
    "    const maxParts=(Math.max(0,b.firstShiftParts)+(Math.max(0,queryShifts-1)*b.normalShiftParts));",
    "    const opWindowShifts=wd*b.shiftCount;\n    const maxParts=(Math.max(0,b.firstShiftParts)+(Math.max(0,opWindowShifts-1)*b.normalShiftParts));",
    "query op window shifts",
)

html = replace_once(
    html,
    "    Total machine time: <b>${totalHrs.toFixed(1)} hrs</b> &nbsp;(${plan?plan.maxShifts.toFixed(1):(totalHrs/(netShiftMinutes()/60)).toFixed(1)} net shift(s) @ ${(netShiftMinutes()/60).toFixed(2)}hr net/shift)",
    "    Total machine time: <b>${totalHrs.toFixed(1)} hrs</b> &nbsp;(${plan?plan.maxDays.toFixed(1):(totalHrs/(netShiftMinutes()/60)/shiftsPerDay()).toFixed(1)} working day(s) at assigned operation shifts)",
    "query mixed shift report line",
)

html = replace_once(
    html,
    "return `OP ${o.num}: ${o.desc||'unnamed'}, cycle=${o.cycle} ${o.cycleUnit||'min'}, one-time setup=${o.setup||0} ${o.setupUnit||'min'}, move qty=${o.moveQty||1}, first shift capacity=${cap?cap.firstShiftParts:'unknown'}, normal shift capacity=${cap?cap.normalShiftParts:'unknown'}, setup+first-part fits shift=${cap?cap.fitsFirstPart:'unknown'}`;",
    "return `OP ${o.num}: ${o.desc||'unnamed'}, cycle=${o.cycle} ${o.cycleUnit||'min'}, one-time setup=${o.setup||0} ${o.setupUnit||'min'}, move qty=${o.moveQty||1}, shift coverage=${opShiftLabel(o)}, calendar load=${cap?cap.days.toFixed(1)+' working days':'unknown'}, first shift capacity=${cap?cap.firstShiftParts:'unknown'}, normal shift capacity=${cap?cap.normalShiftParts:'unknown'}, setup+first-part fits shift=${cap?cap.fitsFirstPart:'unknown'}`;",
    "assistant op shift context",
)

sw = replace_once(sw, "cnc-cell-planner-v14-ready-queue-polish", "cnc-cell-planner-v15-operation-shifts", "service worker v15")

index_path.write_text(html, encoding="utf-8")
sw_path.write_text(sw, encoding="utf-8")

script_path.unlink(missing_ok=True)
workflow_path.unlink(missing_ok=True)
try:
    script_path.parent.rmdir()
except OSError:
    pass
