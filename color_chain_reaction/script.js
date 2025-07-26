const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const cols = 8;
const rows = 12;
const cellSize = 40;
const colors = ['#ff595e', '#8ac926', '#1982c4', '#ffca3a'];
let board = [];
let score = 0;
let level = 1;

function initBoard() {
    board = [];
    for (let r = 0; r < rows; r++) {
        const row = [];
        for (let c = 0; c < cols; c++) {
            row.push(randomColor());
        }
        board.push(row);
    }
}

function randomColor() {
    const idx = Math.floor(Math.random() * Math.min(colors.length, 2 + level));
    return colors[idx];
}

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const color = board[r][c];
            if (color) {
                ctx.fillStyle = color;
                ctx.beginPath();
                ctx.arc(c * cellSize + cellSize / 2, r * cellSize + cellSize / 2, cellSize / 2 - 2, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }
}

function floodFill(r, c, color, visited) {
    const key = `${r},${c}`;
    if (visited.has(key)) return [];
    visited.add(key);
    const cluster = [{ r, c }];
    const dirs = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1]
    ];
    for (const [dr, dc] of dirs) {
        const nr = r + dr;
        const nc = c + dc;
        if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && board[nr][nc] === color) {
            cluster.push(...floodFill(nr, nc, color, visited));
        }
    }
    return cluster;
}

function removeCluster(cluster) {
    if (cluster.length < 3) return false;
    score += cluster.length;
    document.getElementById('score-value').textContent = score;
    for (const { r, c } of cluster) {
        board[r][c] = null;
    }
    applyGravity();
    spawnNew();
    if (score >= level * 100 && level < colors.length) {
        level++;
    }
    return true;
}

function applyGravity() {
    for (let c = 0; c < cols; c++) {
        for (let r = rows - 1; r >= 0; r--) {
            if (!board[r][c]) {
                let above = r - 1;
                while (above >= 0 && !board[above][c]) above--;
                if (above >= 0) {
                    board[r][c] = board[above][c];
                    board[above][c] = null;
                }
            }
        }
    }
}

function spawnNew() {
    for (let c = 0; c < cols; c++) {
        for (let r = 0; r < rows; r++) {
            if (!board[r][c]) {
                board[r][c] = randomColor();
            }
        }
    }
}

canvas.addEventListener('click', (e) => {
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const c = Math.floor(x / cellSize);
    const r = Math.floor(y / cellSize);
    if (r >= 0 && r < rows && c >= 0 && c < cols) {
        const color = board[r][c];
        const cluster = floodFill(r, c, color, new Set());
        if (removeCluster(cluster)) {
            drawBoard();
        }
    }
});

initBoard();
drawBoard();
