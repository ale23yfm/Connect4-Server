const statusEl = document.getElementById('status');
const boardEl = document.getElementById('board');
const controls = document.getElementById('controls');

const ws = new WebSocket((location.protocol === 'https:' ? 'wss://' : 'ws://') + location.host);

const youEl = document.getElementById('you');

function choosePiece(p) {
  send(p);
  const beige = p === 'X';
  youEl.innerHTML =
    '<span class="dot" style="background:' + (beige ? 'var(--sand)' : 'var(--red)') + '"></span>' +
    'You are the ' + (beige ? 'beige' : 'red');
}

function send(t) { if (ws.readyState === 1) ws.send(t); }

function setButtons(items) {
  controls.innerHTML = '';
  items.forEach(([label, value, fn]) => {
    const b = document.createElement('button');
    b.textContent = label;
    b.onclick = fn || (() => send(value));
    controls.appendChild(b);
  });
}

function drawBoard(rows) {
  boardEl.innerHTML = '';
  rows.forEach(r => [...r].forEach(ch => {
    const c = document.createElement('div');
    const u = ch.toUpperCase();
    c.className = 'cell' + (u === 'X' ? ' x' : u === 'O' ? ' o' : '');
    boardEl.appendChild(c);
  }));
}

ws.onmessage = e => {
  const text = e.data;
  const rows = [], info = [];
  text.split('\n').forEach(line => {
    const t = line.replace(/[|\s]/g, '');
    if (!t) return;
    if (/^[1-7]+$/.test(t)) return;          // header "1 2 3 4 5 6 7"
    if (t.length === 7) rows.push(t);        // board row
    else info.push(line.trim());
  });
  if (rows.length >= 4) drawBoard(rows);
  statusEl.textContent = info.join('\n') || text;

  if (text.includes('Choose mode')) {
    setButtons([['Play with algorithm', 'ALGORITHM'], ['Play with AI', 'AI']]);
  } else if (text.includes('Choose a piece')) {
    setButtons([['Play beige', null, () => choosePiece('X')],
            ['Play red', null, () => choosePiece('O')]]);
  } else if (text.includes('Game over')) {
    setButtons([['Play again', null, () => location.reload()]]);
  } else if (text.includes('Choose a column')) {
    setButtons([1,2,3,4,5,6,7].map(i => [String(i), String(i)]));
  }
};

ws.onclose = () => {
  statusEl.textContent += '\n\nDisconnected.';
  setButtons([['Reconnect', null, () => location.reload()]]);
};