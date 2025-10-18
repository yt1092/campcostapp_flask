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

// 現在の状態を取得
function getCurrentStates() {
  const names = [];
  const foodEx = [];
  const transportEx = [];
  const campEx = [];
  
  const members = document.querySelectorAll('#members > div');
  members.forEach((div, i) => {
    names.push(div.querySelector(`input[name="name_${i}"]`).value);
    foodEx.push(div.querySelector(`input[name="food_exempt[]"]`).checked);
    transportEx.push(div.querySelector(`input[name="transport_exempt[]"]`).checked);
    campEx.push(div.querySelector(`input[name="camp_exempt[]"]`).checked);
  });
  
  return {names, foodEx, transportEx, campEx};
}

// 人数入力直接変更
document.getElementById('people').addEventListener('input', (e) => {
  const current = getCurrentStates();
  initMembers(e.target.value, current.names, current.foodEx, current.transportEx, current.campEx);
});

// ＋ボタン
document.getElementById('add-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  const current = getCurrentStates();
  input.value = parseInt(input.value) + 1;
  initMembers(input.value, current.names, current.foodEx, current.transportEx, current.campEx);
});

// －ボタン
document.getElementById('remove-person').addEventListener('click', () => {
  const input = document.getElementById('people');
  const current = getCurrentStates();
  input.value = Math.max(1, parseInt(input.value) - 1);
  initMembers(input.value, current.names, current.foodEx, current.transportEx, current.campEx);
});
