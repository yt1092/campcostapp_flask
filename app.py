function buildMemberHTML(i, name = `メンバー${i+1}`, foodEx=false, transportEx=false, campEx=false) {
  return `
    <div class="border p-2 mb-2 rounded">
      <label class="form-label">メンバー ${i+1} 名前</label>
      <input class="form-control mb-2" name="name_${i}" value="${name}">
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="food_exempt[${i}]" ${foodEx ? 'checked' : ''}>
        <label class="form-check-label">食費免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="transport_exempt[${i}]" ${transportEx ? 'checked' : ''}>
        <label class="form-check-label">交通免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="camp_exempt[${i}]" ${campEx ? 'checked' : ''}>
        <label class="form-check-label">キャンプ免除</label>
      </div>
    </div>
  `;
}

function normalizeBool(val) {
  return val === true || val === "true" || val === 1;
}

function initMembers(n, names=[], foodEx=[], transportEx=[], campEx=[]) {
  const container = document.getElementById('members');
  container.innerHTML = '';
  n = Math.max(1, Math.min(100, parseInt(n || 1)));

  for (let i = 0; i < n; i++) {
    const name = names[i] || `メンバー${i+1}`;
    const f = foodEx[i] !== undefined ? normalizeBool(foodEx[i]) : false;
    const t = transportEx[i] !== undefined ? normalizeBool(transportEx[i]) : false;
    const c = campEx[i] !== undefined ? normalizeBool(campEx[i]) : false;
    container.insertAdjacentHTML('beforeend', buildMemberHTML(i, name, f, t, c));
  }
}

function getCurrentStates() {
  const container = document.getElementById('members');
  const names = [], foodEx = [], transportEx = [], campEx = [];
  container.querySelectorAll('div.border').forEach((div, i) => {
    names.push(div.querySelector(`input[name="name_${i}"]`).value);
    foodEx.push(div.querySelector(`input[name="food_exempt[${i}]"]`).checked);
    transportEx.push(div.querySelector(`input[name="transport_exempt[${i}]"]`).checked);
    campEx.push(div.querySelector(`input[name="camp_exempt[${i}]"]`).checked);
  });
  return { names, foodEx, transportEx, campEx };
}

function updateMembers(n) {
  const states = getCurrentStates();
  initMembers(n, states.names, states.foodEx, states.transportEx, states.campEx);
}

document.addEventListener('DOMContentLoaded', () => {
  const d = window.initialData || {};
  initMembers(d.form_people, d.form_names, d.form_food_exempt, d.form_transport_exempt, d.form_camp_exempt);
});

document.getElementById('people').addEventListener('input', (e) => {
  updateMembers(parseInt(e.target.value) || 1);
});
document.getElementById('add-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  input.value = parseInt(input.value || "0") + 1;
  updateMembers(parseInt(input.value));
});
document.getElementById('remove-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  input.value = Math.max(1, parseInt(input.value || "0") - 1);
  updateMembers(parseInt(input.value));
});
