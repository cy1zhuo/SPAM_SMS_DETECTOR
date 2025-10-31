const smsText = document.getElementById('smsText');
const checkBtn = document.getElementById('checkBtn');
const loading = document.getElementById('loading');
const resultBox = document.getElementById('result');
const labelEl = document.getElementById('label');
const probEl = document.getElementById('prob');
const explainEl = document.getElementById('explain');
// history is now on a separate page (history.html)

function setLoading(on){
  loading.classList.toggle('hidden', !on);
  checkBtn.disabled = on;
}

function showResult(isSpam, prob, raw){
  resultBox.classList.remove('hidden');
  labelEl.textContent = isSpam ? 'Spam' : 'Not Spam';
  labelEl.className = 'label ' + (isSpam ? 'spam' : 'ham');
  probEl.textContent = `Confidence: ${Math.round(prob*100)}%`;
  explainEl.textContent = raw?.message ? raw.message : '';
}

async function checkSms(){
  const text = smsText.value.trim();
  if(!text){
    alert('Please enter an SMS message to check.');
    return;
  }

  setLoading(true);
  resultBox.classList.add('hidden');

  try{
    const res = await fetch('http://127.0.0.1:5000/predict', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({text})
    });

    if(!res.ok){
      const t = await res.text();
      throw new Error(t || 'Server error');
    }

    const data = await res.json();
    const isSpam = (data.label || '').toLowerCase() === 'spam' || data.label === 1 || data.label === '1';
    const prob = data.probability ?? (data.prob ?? 0);
    showResult(isSpam, prob, data);
  }catch(err){
    alert('Error: ' + err.message);
  }finally{
    setLoading(false);
  }
}

checkBtn.addEventListener('click', checkSms);

// Allow Ctrl+Enter to submit when focus is in textarea
smsText.addEventListener('keydown', (e)=>{
  if((e.ctrlKey || e.metaKey) && e.key === 'Enter') checkSms();
});

// --- history functions ---
// history page lives in history.html which imports history.js
