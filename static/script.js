// build member block: visible checkboxes DO NOT carry submission names.
// submission will be prepared on submit (hidden inputs arrays named food_exempt, etc.)
function buildMemberHTML(i, name = `メンバー${i+1}`, foodEx=false, transportEx=false, campEx=false) {
  return `
    <div class="member-card border p-2 mb-2 rounded">
      <label class="form-label">メンバー ${i+1} 名前</label>
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

function escapeHtml(s) {
  if (typeof s !== "string") return s;
  return s.replace(/[&<>"']/g, function(m){ return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[m]; });
}

function initMembers(n, names=[], foodEx=[], transportEx=[], campEx=[]) {
  const container = document.getElementById('members');
  container.innerHTML = '';
  n = Math.max(1, Math.min(100, parseInt(n || 1)));

  for (let i = 0; i < n; i++) {
    const name = (Array.isArray(names) && names[i]) ? names[i] : `メンバー${i+1}`;
    const f = foodEx && (foodEx[i] === true || foodEx[i] === "true" || foodEx[i] === 1);
    const t = transportEx && (transportEx[i] === true || transportEx[i] === "true" || transportEx[i] === 1);
    const c = campEx && (campEx[i] === true || campEx[i] === "true" || campEx[i] === 1);
    container.insertAdjacentHTML('beforeend', buildMemberHTML(i, name, f, t, c));
  }
}

function getCurrentStates() {
  const container = document.getElementById('members');
  const names = [], foodEx = [], transportEx = [], campEx = [];
  container.querySelectorAll('.member-card').forEach((div, i) => {
    const nameInput = div.querySelector(`input[name="name_${i}"]`);
    names.push(nameInput ? nameInput.value : `メンバー${i+1}`);
    const f = div.querySelector('.food-visible');
    const t = div.querySelector('.transport-visible');
    const c = div.querySelector('.camp-visible');
    foodEx.push(!!(f && f.checked));
    transportEx.push(!!(t && t.checked));
    campEx.push(!!(c && c.checked));
  });
  return { names, foodEx, transportEx, campEx };
}

function updateMembers(n) {
  const states = getCurrentStates();
  initMembers(n, states.names, states.foodEx, states.transportEx, states.campEx);
}

// helper: remove previously-inserted hidden arrays
function removeHiddenArrays(form, prefix) {
  const olds = form.querySelectorAll(`input[type="hidden"].${prefix}`);
  olds.forEach(o => o.remove());
}


function prepareSubmission(evt) {
  const form = document.getElementById('main-form');

  ['food_exempt','transport_exempt','camp_exempt'].forEach(cls => {
    removeHiddenArrays(form, cls + '-hidden');
  });

  const states = getCurrentStates();
  const n = states.names.length;

  for (let i = 0; i < n; i++) {
    const inpF = document.createElement('input');
    inpF.type = 'hidden';
    inpF.name = 'food_exempt';
    inpF.value = states.foodEx[i] ? 'true' : 'false';
    inpF.className = 'food_exempt-hidden';
    form.appendChild(inpF);

    const inpT = document.createElement('input');
    inpT.type = 'hidden';
    inpT.name = 'transport_exempt';
    inpT.value = states.transportEx[i] ? 'true' : 'false';
    inpT.className = 'transport_exempt-hidden';
    form.appendChild(inpT);

    const inpC = document.createElement('input');
    inpC.type = 'hidden';
    inpC.name = 'camp_exempt';
    inpC.value = states.campEx[i] ? 'true' : 'false';
    inpC.className = 'camp_exempt-hidden';
    form.appendChild(inpC);
  }

  const peopleInput = document.getElementById('people');
  peopleInput.value = n;
  
  ['food-input','transport-input','camp-input'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = (el.value || '').toString().replace(/,/g, '');
  });

}

function formatWithCommasInput(el) {
  if (!el) return;
  el.addEventListener('input', () => {
    const start = el.selectionStart;
    const val = el.value.replace(/,/g, '').replace(/[^\d]/g,'');
    if (val === '') { el.value = ''; return; }
    el.value = Number(val).toLocaleString('en-US');
  });
  el.addEventListener('focus', () => {
    el.value = (el.value || '').toString().replace(/,/g, '');
  });
  el.addEventListener('blur', () => {
    const val = el.value.replace(/,/g, '').replace(/[^\d]/g,'');
    el.value = val === '' ? '' : Number(val).toLocaleString('en-US');
  });
}

document.addEventListener('DOMContentLoaded', () => {
  // initialize members from server data
  const d = window.initialData || {};
  const people = d.form_people || 1;
  const names = d.form_names || [];
  const foodEx = d.form_food_exempt || [];
  const transportEx = d.form_transport_exempt || [];
  const campEx = d.form_camp_exempt || [];

  initMembers(people, names, foodEx, transportEx, campEx);

  // wire up controls
  const peopleInput = document.getElementById('people');
  const addBtn = document.getElementById('add-person');
  const removeBtn = document.getElementById('remove-person');
  const form = document.getElementById('main-form');

  peopleInput.addEventListener('input', (e) => {
    const n = Math.max(1, Math.min(100, parseInt(e.target.value || "1")));
    updateMembers(n);
  });

  addBtn.addEventListener('click', () => {
    const current = parseInt(peopleInput.value || "0") + 1;
    peopleInput.value = current;
    updateMembers(current);
  });

  removeBtn.addEventListener('click', () => {
    const current = Math.max(1, parseInt(peopleInput.value || "1") - 1);
    peopleInput.value = current;
    updateMembers(current);
  });

  formatWithCommasInput(document.getElementById('food-input'));
  formatWithCommasInput(document.getElementById('transport-input'));
  formatWithCommasInput(document.getElementById('camp-input'));

  form.addEventListener('submit', (evt) => {
    prepareSubmission(evt);
  });
});
