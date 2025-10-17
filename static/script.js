function checkboxChecked(arr, i) {
  return Array.isArray(arr) && arr[i] === true;
}

function buildMemberHTML(i, name = `メンバー${i+1}`, foodEx=false, transportEx=false, campEx=false) {
  return `
    <div class="border p-2 mb-2 rounded">
      <label class="form-label">メンバー ${i+1} 名前</label>
      <input class="form-control mb-2" name="name_${i}" value="${name}">
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="foodExempt_${i}" name="foodExempt_${i}" ${foodEx ? 'checked' : ''}>
        <label class="form-check-label" for="foodExempt_${i}">食費免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="transportExempt_${i}" name="transportExempt_${i}" ${transportEx ? 'checked' : ''}>
        <label class="form-check-label" for="transportExempt_${i}">交通免除</label>
      </div>
      <div class="form-check form-check-inline">
        <input class="form-check-input" type="checkbox" id="campExempt_${i}" name="campExempt_${i}" ${campEx ? 'checked' : ''}>
        <label class="form-check-label" for="campExempt_${i}">キャンプ免除</label>
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
  initMembers(e.target.value);
});