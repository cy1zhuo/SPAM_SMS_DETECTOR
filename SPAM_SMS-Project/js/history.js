// History page script (new, improved)
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');
const filterAllBtn = document.getElementById('filterAll');
const filterSpamBtn = document.getElementById('filterSpam');
const filterHamBtn = document.getElementById('filterHam');
const searchInput = document.getElementById('searchInput');
const historyStats = document.getElementById('historyStats');
const downloadBtn = document.getElementById('downloadBtn');

let rawHistory = [];
let activeFilter = 'all';

function safeText(t){ return (t||'').toString(); }

async function fetchHistory(){
  if(!historyList) return;
  historyList.innerHTML = '<li class="meta">Loading history…</li>';
  try{
    // try same-origin first, then fallback to localhost:5000
    let res;
    try { res = await fetch('/history'); } catch(e) {
      res = await fetch('http://127.0.0.1:5000/history');
    }
    if(!res.ok){
      // try to show server error body
      let errBody = null;
      try { const j = await res.json(); errBody = j && (j.error || j.message) ? (j.error || j.message) : JSON.stringify(j); } catch(e) {}
      historyList.innerHTML = `<li class="meta">Could not load history (server error)${errBody ? ': ' + errBody : ''}.</li>`;
      if(historyStats) historyStats.textContent = 'Error';
      return;
    }
    const data = await res.json();
    rawHistory = data.history || [];
    renderHistory(rawHistory);
    updateStats(rawHistory);
  }catch(e){
    historyList.innerHTML = '<li class="meta">Could not load history (network).</li>';
    if(historyStats) historyStats.textContent = 'Offline';
    console.warn('Could not load history', e);
  }
}

function updateStats(hist){
  if(!historyStats) return;
  const total = hist.length;
  const spamCount = hist.filter(h=>String(h.label).toLowerCase()==='spam').length;
  const hamCount = total - spamCount;
  historyStats.textContent = `${total} items · ${spamCount} spam · ${hamCount} safe`;

  // overlay control
  const overlay = document.getElementById('phishingOverlay');
  if(overlay){
    overlay.style.opacity = (total>0 && spamCount/Math.max(1,total) > 0.4) ? '1' : '0';
  }
}

function renderHistory(hist){
  if(!historyList) return;
  const query = (searchInput?.value||'').toLowerCase().trim();
  let list = hist.slice();
  if(activeFilter==='spam') list = list.filter(i=>String(i.label).toLowerCase()==='spam');
  if(activeFilter==='ham') list = list.filter(i=>String(i.label).toLowerCase()!=='spam');
  if(query) list = list.filter(i=>safeText(i.text).toLowerCase().includes(query));

  if(!list || list.length === 0){
    historyList.innerHTML = '<li class="meta">No matching history.</li>';
    return;
  }

  historyList.innerHTML = '';
  list.forEach(item=>{
    const li = document.createElement('li');
    const txt = document.createElement('div');
    txt.textContent = item.text;
    txt.style.whiteSpace = 'pre-wrap';
    txt.style.fontSize = '13px';

    const meta = document.createElement('div');
    meta.className = 'meta';
    const time = item.timestamp ? new Date(item.timestamp).toLocaleString() : '';
    const prob = Math.round((item.probability||0)*100);
    meta.textContent = `${item.label} · ${prob}% · ${time}`;

    if(String(item.label).toLowerCase()==='spam'){
      li.style.borderLeft = '4px solid rgba(239,68,68,0.6)';
      li.style.background = 'rgba(239,68,68,0.02)';
    } else {
      li.style.borderLeft = '4px solid rgba(16,185,129,0.5)';
      li.style.background = 'rgba(16,185,129,0.02)';
    }

    li.appendChild(txt);
    li.appendChild(meta);
    historyList.appendChild(li);
  });
}

if(clearHistoryBtn){
  clearHistoryBtn.addEventListener('click', async ()=>{
    if(!confirm('Clear prediction history?')) return;
    try{
  // try relative endpoint first, then fallback
  let res;
  try { res = await fetch('/history', {method:'DELETE'}); }
  catch(e) { res = await fetch('http://127.0.0.1:5000/history', {method:'DELETE'}); }
      if(res.ok){
        rawHistory = [];
        renderHistory([]);
        updateStats([]);
      }else{
        alert('Failed to clear history');
      }
    }catch(e){
      alert('Error clearing history');
    }
  });
}

if(filterAllBtn) filterAllBtn.addEventListener('click', ()=>{ activeFilter='all'; renderHistory(rawHistory); });
if(filterSpamBtn) filterSpamBtn.addEventListener('click', ()=>{ activeFilter='spam'; renderHistory(rawHistory); });
if(filterHamBtn) filterHamBtn.addEventListener('click', ()=>{ activeFilter='ham'; renderHistory(rawHistory); });
if(searchInput) searchInput.addEventListener('input', ()=> renderHistory(rawHistory));

if(downloadBtn) downloadBtn.addEventListener('click', ()=>{
  if (rawHistory.length === 0) {
    alert('No history data to download');
    return;
  }
  
  // Define carrier columns in the same order as Predicted_SPAM_SMS.csv
  const carrierColumns = [
    'carrier_DITO',
    'carrier_Globe',
    'carrier_Globe PostPaid',
    'carrier_Globe/TM',
    'carrier_Smart',
    'carrier_Smart/Sun',
    'carrier_Smart/TNT',
    'carrier_Sun',
    'carrier_TNT'
  ];
  
  // Create CSV header row
  const headers = [
    'text',
    ...carrierColumns,
    'label',
    'predicted_label'
  ];
  
  const csvRows = [];
  
  // Add header row
  csvRows.push(headers.join(','));
  
  // Add data rows
  rawHistory.forEach(item => {
    // Initialize all carrier flags to false
    const carrierValues = carrierColumns.reduce((acc, curr) => {
      acc[curr] = 'False';
      return acc;
    }, {});
    
    // Set the detected carrier to true if available
    if (item.carrier) {
      const carrierKey = `carrier_${item.carrier}`;
      if (carrierValues.hasOwnProperty(carrierKey)) {
        carrierValues[carrierKey] = 'True';
      }
    }
    
    // Escape quotes in text and handle line breaks
    const escapedText = (item.text || '').replace(/"/g, '""').replace(/\n/g, ' ');
    
    const row = [
      `"${escapedText}"`,  // text
      ...carrierColumns.map(col => carrierValues[col]),  // carrier flags
      `"${item.label || ''}"`,  // label
      `"${item.label || ''}"`   // predicted_label (using label as fallback)
    ];
    
    csvRows.push(row.join(','));
  });
  
  const csvString = csvRows.join('\n');
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'Predicted_SPAM_SMS.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

// initialize
fetchHistory();
