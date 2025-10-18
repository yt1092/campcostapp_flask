function escapeHtml(s) {
  if (typeof s !== "string") return s;
  return s.replace(/[&<>"']/g, function(m){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; });
}

function buildMemberHTML(i, name = `メンバー${i+1}`, foodEx=false, transportEx=false, campEx=false) {
  return `
    <div class="member-card border p-2 mb-2 rounded" data-index="${i}">
      <label class="form-label mb-1">メンバー ${i+1} 名前</label>
      <input class="form-control mb-2" name="name_${i}" value="${escapeHtml(name)}">
      <div class="form-check form-check-inline">
        <input class="form-check-input food-visible" type="checkbox" data-index="${i}" ${foodEx ? 'checked' : ''}>
        <label class="form-check-label">食費免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input transport-visible" type="checkbox" data-index="${i}" ${transportEx ? 'checked' : ''}>
        <label class="form-check-label">交通免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input camp-visible" type="checkbox" data-index="${i}" ${campEx ? 'checked' : ''}>
        <label class="form-check-label">キャンプ免除</label>
      </div>
    </div>
  `;
}

function normalizeBool(v) {
  return v === true || v === "true" || v === 1 || v === "1";
}

function initMembers(n, names=[], foodEx=[], transportEx=[], campEx=[]) {
  const container = document.getElementById('members');
  container.innerHTML = '';
  n = Math.max(1, Math.min(100, parseInt(n || 1)));

  for (let i = 0; i < n; i++) {
    const nm = (Array.isArray(names) && typeof names[i] !== "undefined" && names[i] !== null) ? names[i] : `メンバー${i+1}`;
    const f = Array.isArray(foodEx) ? normalizeBool(foodEx[i]) : false;
    const t = Array.isArray(transportEx) ? normalizeBool(transportEx[i]) : false;
    const c = Array.isArray(campEx) ? normalizeBool(campEx[i]) : false;
    container.insertAdjacentHTML('beforeend', buildMemberHTML(i, nm, f, t, c));
  }
}

function getCurrentStates() {
  const container = document.getElementById('members');
  const names = [], foodEx = [], transportEx = [], campEx = [];
  container.querySelectorAll('.member-card').forEach((div, i) => {
    const nameInput = div.querySelector(`input[name="name_${i}"]`);
    names.push(nameInput ? nameInput.value : `メンバー${i+1}`);
    const fv = div.querySelector('.food-visible');
    const tv = div.querySelector('.transport-visible');
    const cv = div.querySelector('.camp-visible');
    foodEx.push(!!(fv && fv.checked));
    transportEx.push(!!(tv && tv.checked));
    campEx.push(!!(cv && cv.checked));
  });
  return { names, foodEx, transportEx, campEx };
}

function updateMembers(n) {
  const states = getCurrentStates();
  initMembers(n, states.names, states.foodEx, states.transportEx, states.campEx);
}

function prepareSubmission() {
  const form = document.getElementById('main-form');
  form.querySelectorAll('input._gen_hidden').forEach(el => el.remove());
  const states = getCurrentStates();
  const n = states.names.length;
  const peopleInput = document.getElementById('people');
  peopleInput.value = n;

  for (let i = 0; i < n; i++) {
    const hF = document.createElement('input');
    hF.type = 'hidden';
    hF.name = 'food_exempt';
    hF.value = states.foodEx[i] ? 'true' : 'false';
    hF.className = '_gen_hidden';
    form.appendChild(hF);

    const hT = document.createElement('input');
    hT.type = 'hidden';
    hT.name = 'transport_exempt';
    hT.value = states.transportEx[i] ? 'true' : 'false';
    hT.className = '_gen_hidden';
    form.appendChild(hT);

    const hC = document.createElement('input');
    hC.type = 'hidden';
    hC.name = 'camp_exempt';
    hC.value = states.campEx[i] ? 'true' : 'false';
    hC.className = '_gen_hidden';
    form.appendChild(hC);
  }

  ['food-input','transport-input','camp-input'].forEach(id => {
    const el = document.getElementById(id);
    if (el && typeof el.value === "string") {
      el.value = el.value.replace(/,/g, '').replace(/[^\d.-]/g,'') || '0';
    }
  });
}

function attachMoneyFormatter(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.addEventListener('input', () => {
    const pos = el.selectionStart;
    const raw = el.value.replace(/,/g, '').replace(/[^\d]/g,'');
    if (raw === '') { el.value = ''; return; }
    el.value = Number(raw).toLocaleString('en-US');
  });
  el.addEventListener('focus', () => { el.value = el.value.replace(/,/g, ''); });
  el.addEventListener('blur', () => {
    const raw =
