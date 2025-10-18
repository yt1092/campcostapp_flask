function checkboxChecked(arr, i) {
  return Array.isArray(arr) && arr[i] === true;
}

function buildMemberHTML(i, name = `メンバー${i+1}`, foodEx=false, transportEx=false, campEx=false) {
  return `
    <div class="border p-2 mb-2 rounded">
      <label class="form-label">メンバー ${i+1} 名前</label>
      <input class="form-control mb-2" name="name_${i}" value="${name}">
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="food_exempt[]" ${foodEx ? 'checked' : ''}>
        <label class="form-check-label">食費免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="transport_exempt[]" ${transportEx ? 'checked' : ''}>
        <label class="form-check-label">交通免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" name="camp_exempt[]" ${campEx ? 'checked' : ''}>
        <label class="form-check-label">キャンプ免除</label>
      </div>
    </div>
  `;
}

function initMembers(n, names=[], foodEx=[], transportEx=[], campEx=[]) {
  const container = document.getElementById('members');
  container.innerHTML = '';
  n = Math.max(1, Math.min(100, parseInt(n || 1)));
  for (let i = 0; i < n; i++) {
    const name = names[i] || `メンバー${i+1}`;
    const f = !!foodEx[i];
    const t = !!transportEx[i];
    const c = !!campEx[i];
    container.insertAdjacentHTML('beforeend', buildMemberHTML(i, name, f, t, c));
  }
}

document.getElementById('people').addEventListener('input', (e) => {
  initMembers(parseInt(e.target.value) || 1);
});

document.getElementById('add-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  input.value = parseInt(input.value || "0") + 1;
  initMembers(parseInt(input.value));
});

document.getElementById('remove-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  input.value = Math.max(1, parseInt(input.value || "0") - 1);
  initMembers(parseInt(input.value));
});

document.getElementById('people').addEventListener('input', (e) => {
  initMembers(e.target.value);

});

