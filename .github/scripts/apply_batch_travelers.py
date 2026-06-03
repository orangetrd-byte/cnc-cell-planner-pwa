from pathlib import Path

index = Path('index.html')
text = index.read_text(encoding='utf-8')

if '.wo-bulk-grid' not in text:
    text = text.replace(
        '.holiday-row .field{min-width:140px}\n.holiday-row .btn{white-space:nowrap}',
        '.holiday-row .field{min-width:140px}\n.holiday-row .btn{white-space:nowrap}\n.wo-bulk{margin-bottom:12px}\n.wo-bulk-grid{display:grid;grid-template-columns:1.4fr 1fr .75fr .75fr .85fr auto;gap:8px;align-items:end}'
    )
    text = text.replace(
        '@media(max-width:600px){body{padding-bottom:70px}header{padding:11px 12px}.htitles h1{font-size:15px}.hright{gap:5px}.app-nav{position:fixed;top:auto;bottom:0;left:0;right:0;z-index:300;padding:8px 10px calc(8px + env(safe-area-inset-bottom));border-top:1px solid var(--border);border-bottom:none;background:rgba(255,255,255,.96);box-shadow:0 -2px 12px rgba(0,0,0,.08)}.nav-btn{padding:9px 10px;min-width:82px}.main{padding-bottom:20px}.stat-grid{grid-template-columns:1fr 1fr}.frow{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr}}',
        '@media(max-width:1100px){.wo-bulk-grid{grid-template-columns:1fr 1fr 1fr}.wo-bulk-grid .btn{width:100%;justify-content:center}}\n@media(max-width:600px){body{padding-bottom:70px}header{padding:11px 12px}.htitles h1{font-size:15px}.hright{gap:5px}.app-nav{position:fixed;top:auto;bottom:0;left:0;right:0;z-index:300;padding:8px 10px calc(8px + env(safe-area-inset-bottom));border-top:1px solid var(--border);border-bottom:none;background:rgba(255,255,255,.96);box-shadow:0 -2px 12px rgba(0,0,0,.08)}.nav-btn{padding:9px 10px;min-width:82px}.main{padding-bottom:20px}.stat-grid{grid-template-columns:1fr 1fr}.frow{grid-template-columns:1fr}.mini-grid{grid-template-columns:1fr}.wo-bulk-grid{grid-template-columns:1fr}}'
    )

if 'id="woBatchName"' not in text:
    text = text.replace(
        '      <p class="tip" style="margin-bottom:11px">Track traveler quantities and release status for phased flow through the shop.</p>\n      <div class="hchips" id="woSummary" style="margin-bottom:11px"></div>',
        '''      <p class="tip" style="margin-bottom:11px">Track traveler quantities and release status for phased flow through the shop.</p>
      <div class="qbox wo-bulk">
        <div class="wo-bulk-grid">
          <div class="field"><label>Part / Batch</label><input type="text" id="woBatchName" placeholder="e.g. Part A / Batch 1"></div>
          <div class="field"><label>WO Prefix</label><input type="text" id="woPrefix" placeholder="A-"></div>
          <div class="field"><label>Start #</label><input type="number" id="woStartNum" min="1" value="1"></div>
          <div class="field"><label>Travelers</label><input type="number" id="woBatchCount" min="1" value="1"></div>
          <div class="field"><label>Qty Each</label><input type="number" id="woQtyEach" min="1" placeholder="10"></div>
          <button class="btn btn-primary" onclick="createTravelerBatch()">Create Batch</button>
        </div>
      </div>
      <div class="hchips" id="woSummary" style="margin-bottom:11px"></div>'''
    )
    text = text.replace(
        '<table><thead><tr><th>WO #</th><th>Qty</th><th>Current Op</th><th>Done @ Op</th><th>Flow</th><th>Status</th><th>Advance</th><th></th></tr></thead>\n<tbody id="woBody"><tr class="empty-row"><td colspan="8">No work orders - click "+ Add WO" to begin</td></tr></tbody></table>',
        '<table><thead><tr><th>Batch / Part</th><th>WO #</th><th>Qty</th><th>Current Op</th><th>Done @ Op</th><th>Flow</th><th>Status</th><th>Advance</th><th></th></tr></thead>\n<tbody id="woBody"><tr class="empty-row"><td colspan="9">No work orders - create a batch or click "+ Add WO" to begin</td></tr></tbody></table>'
    )

if 'function workOrderBatchSummary()' not in text:
    text = text.replace(
        'function workOrderQty(){\n  return workOrders.reduce((sum,w)=>sum+(parseInt(w.qty)||0),0);\n}\n',
        '''function workOrderQty(){
  return workOrders.reduce((sum,w)=>sum+(parseInt(w.qty)||0),0);
}
function workOrderBatchSummary(){
  const batches={};
  workOrders.forEach(raw=>{
    const w=normalizeWO(raw);
    const batch=(w.batch||'Unbatched').trim()||'Unbatched';
    if(!batches[batch]) batches[batch]={count:0,qty:0};
    batches[batch].count++;
    batches[batch].qty+=parseInt(w.qty)||0;
  });
  return {
    count:Object.keys(batches).length,
    text:Object.entries(batches).map(([batch,b])=>`${batch}: ${b.count} traveler(s), ${b.qty} pcs`).join(' · ')
  };
}
'''
    )

if 'batch:w.batch' not in text:
    text = text.replace(
        "  const wo={\n    id:w.id,\n    num:w.num||'',",
        "  const wo={\n    id:w.id,\n    batch:w.batch||'',\n    num:w.num||'',"
    )

if 'const batches={};' not in text[text.find('function renderWOSummary()'):text.find('// WORK ORDERS')]:
    text = text.replace(
        '''  const route=routeOps();
  const counts={Complete:0};
  route.forEach(o=>counts['OP '+o.num]=0);
  workOrders.forEach(raw=>{
    const w=normalizeWO(raw);
    if(w.status==='Complete'||w.currentOp==='COMPLETE') counts.Complete++;
    else if(w.currentOp) counts['OP '+w.currentOp]=(counts['OP '+w.currentOp]||0)+1;
  });
  const chips=route.map(o=>`<div class="chip">OP ${o.num}: ${counts['OP '+o.num]||0}</div>`);
  chips.push(`<div class="chip">Complete: ${counts.Complete||0}</div>`);
  el.innerHTML=chips.join('');''',
        '''  const route=routeOps();
  const counts={Complete:0};
  const batches={};
  route.forEach(o=>counts['OP '+o.num]=0);
  workOrders.forEach(raw=>{
    const w=normalizeWO(raw);
    const batch=(w.batch||'Unbatched').trim()||'Unbatched';
    if(!batches[batch]) batches[batch]={count:0,qty:0};
    batches[batch].count++;
    batches[batch].qty+=parseInt(w.qty)||0;
    if(w.status==='Complete'||w.currentOp==='COMPLETE') counts.Complete++;
    else if(w.currentOp) counts['OP '+w.currentOp]=(counts['OP '+w.currentOp]||0)+1;
  });
  const chips=Object.entries(batches).map(([batch,b])=>`<div class="chip">${escHtml(batch)}: ${b.count} traveler(s), ${b.qty.toLocaleString()} pcs</div>`);
  route.forEach(o=>chips.push(`<div class="chip">OP ${o.num}: ${counts['OP '+o.num]||0}</div>`));
  chips.push(`<div class="chip">Complete: ${counts.Complete||0}</div>`);
  el.innerHTML=chips.join('');'''
    )

if 'function createTravelerBatch()' not in text:
    text = text.replace(
        "function addWO(){\n  woC++;\n  workOrders.push({id:woC,num:'',qty:'',currentOp:firstRouteOp(),status:'Not Started',completedOps:[],opProgress:{}});\n  renderWOs(); recalc();\n}\n",
        """function addWO(){
  woC++;
  workOrders.push({id:woC,batch:'',num:'',qty:'',currentOp:firstRouteOp(),status:'Not Started',completedOps:[],opProgress:{}});
  renderWOs(); recalc();
}
function createTravelerBatch(){
  const batch=(document.getElementById('woBatchName')?.value||document.getElementById('partNum')?.value||'Batch').trim()||'Batch';
  const prefix=(document.getElementById('woPrefix')?.value||batch.replace(/[^a-z0-9]+/gi,'-').replace(/^-+|-+$/g,'')+'-').trim();
  const start=Math.max(1,parseInt(document.getElementById('woStartNum')?.value)||1);
  const count=Math.max(1,parseInt(document.getElementById('woBatchCount')?.value)||1);
  const qty=parseInt(document.getElementById('woQtyEach')?.value)||0;
  if(qty<1){ alert('Enter Qty Each before creating the batch.'); return; }
  const width=Math.max(3,String(start+count-1).length);
  for(let i=0;i<count;i++){
    woC++;
    const n=String(start+i).padStart(width,'0');
    workOrders.push({id:woC,batch,num:`${prefix}${n}`,qty:String(qty),currentOp:firstRouteOp(),status:'Not Started',completedOps:[],opProgress:{}});
  }
  document.getElementById('woStartNum').value=String(start+count);
  renderWOs(); recalc();
}
"""
    )

text = text.replace("'<tr class=\"empty-row\"><td colspan=\"8\">No work orders - click \"+ Add WO\" to begin</td></tr>';", "'<tr class=\"empty-row\"><td colspan=\"9\">No work orders - create a batch or click \"+ Add WO\" to begin</td></tr>';" )

if "woCh(${w.id},'batch',this.value)" not in text:
    marker = '''      <tr>
        <td>
          <input type="text"
                 value="${escHtml(w.num)}"'''
    replacement = '''      <tr>
        <td>
          <input type="text"
                 value="${escHtml(w.batch)}"
                 placeholder="Part / batch"
                 oninput="woCh(${w.id},'batch',this.value)">
        </td>

        <td>
          <input type="text"
                 value="${escHtml(w.num)}"'''
    text = text.replace(marker, replacement)

if 'id="sum-batches"' not in text:
    text = text.replace(
        '          <div class="sline"><span class="sl">Closures</span><span class="sv" id="sum-closures">—</span></div>',
        '          <div class="sline"><span class="sl">Closures</span><span class="sv" id="sum-closures">—</span></div>\n          <div class="sline"><span class="sl">Part Batches</span><span class="sv" id="sum-batches">—</span></div>'
    )
if 'const batchSummary=workOrderBatchSummary();' not in text:
    text = text.replace('  const woQty=workOrderQty();\n  const completedStats=completedOperationStats();', '  const woQty=workOrderQty();\n  const batchSummary=workOrderBatchSummary();\n  const completedStats=completedOperationStats();')
if "sum-batches" in text and "batchSummary.count?batchSummary.text" not in text:
    text = text.replace("  document.getElementById('sum-closures').textContent=holidays.length+' day(s)';\n  document.getElementById('sum-wo-count').textContent=workOrders.length;", "  document.getElementById('sum-closures').textContent=holidays.length+' day(s)';\n  document.getElementById('sum-batches').textContent=batchSummary.count?batchSummary.text:'—';\n  document.getElementById('sum-wo-count').textContent=workOrders.length;")

text = text.replace(
    "return `${w.num||'unnumbered'} qty ${parseInt(w.qty)||0} current ${w.currentOp==='COMPLETE'?'COMPLETE':'OP '+w.currentOp} status ${w.status||'Not Started'} done ${completedOpsText(w)}`;",
    "return `${w.num||'unnumbered'} batch ${w.batch||'Unbatched'} qty ${parseInt(w.qty)||0} current ${w.currentOp==='COMPLETE'?'COMPLETE':'OP '+w.currentOp} status ${w.status||'Not Started'} done ${completedOpsText(w)}`;"
)
if 'Traveler Batches:' not in text:
    text = text.replace("  const toolsText=tools.length?tools.map(t=>{", "  const batchSummary=workOrderBatchSummary();\n  const toolsText=tools.length?tools.map(t=>{")
    text = text.replace('Work Orders / Travelers: ${woText}\nTotal WO Quantity: ${workOrderQty()}', 'Work Orders / Travelers: ${woText}\nTraveler Batches: ${batchSummary.text||\'None defined\'}\nTotal WO Quantity: ${workOrderQty()}')

index.write_text(text, encoding='utf-8')

sw = Path('sw.js')
sw_text = sw.read_text(encoding='utf-8')
sw_text = sw_text.replace('cnc-cell-planner-v11-report-completed-ops', 'cnc-cell-planner-v12-batch-travelers')
sw.write_text(sw_text, encoding='utf-8')

Path('.github/workflows/apply-batch-travelers.yml').unlink(missing_ok=True)
Path('.github/scripts/apply_batch_travelers.py').unlink(missing_ok=True)
try:
    Path('.github/scripts').rmdir()
except OSError:
    pass
