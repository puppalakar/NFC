let currentPlayer = 'X';
let board = ['', '', '', '', '', '', '', '', ''];
let gameActive = true;
let scores = { X: 0, O: 0, Ties: 0 };

const winConditions = [
  [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
  [0, 3, 6], [1, 4, 7], [2, 5, 8], // Columns
  [0, 4, 8], [2, 4, 6]             // Diagonals
];

const statusEl = document.getElementById('status');
const scoreXEl = document.getElementById('score-x');
const scoreTiesEl = document.getElementById('score-ties');
const scoreOEl = document.getElementById('score-o');
const cells = document.querySelectorAll('.cell');
const btnNext = document.getElementById('btn-next');
const btnReset = document.getElementById('btn-reset');

cells.forEach(cell => {
  cell.addEventListener('click', () => handleCellClick(cell));
});

btnNext.addEventListener('click', nextRound);
btnReset.addEventListener('click', resetAll);

function handleCellClick(cell) {
  const index = parseInt(cell.getAttribute('data-index'));

  if (board[index] !== '' || !gameActive) return;

  board[index] = currentPlayer;
  cell.textContent = currentPlayer;
  cell.classList.add('taken', currentPlayer.toLowerCase());

  checkResult();
}

function checkResult() {
  let roundWon = false;
  let winningCombo = [];

  for (let i = 0; i < winConditions.length; i++) {
    const [a, b, c] = winConditions[i];
    if (board[a] && board[a] === board[b] && board[a] === board[c]) {
      roundWon = true;
      winningCombo = [a, b, c];
      break;
    }
  }

  if (roundWon) {
    gameActive = false;
    scores[currentPlayer]++;
    updateScores();
    winningCombo.forEach(idx => {
      document.getElementById(`cell-${idx}`).classList.add('winning');
    });
    statusEl.textContent = `Player ${currentPlayer} Wins!`;
    statusEl.className = 'status-turn win-status';
    return;
  }

  if (!board.includes('')) {
    gameActive = false;
    scores.Ties++;
    updateScores();
    cells.forEach(cell => cell.classList.add('tie-cell'));
    statusEl.textContent = "It's a Tie!";
    statusEl.className = 'status-turn tie-status';
    return;
  }

  currentPlayer = currentPlayer === 'X' ? 'O' : 'X';
  statusEl.textContent = `Player ${currentPlayer}'s Turn`;
  statusEl.className = `status-turn ${currentPlayer.toLowerCase()}-turn`;
}

function updateScores() {
  scoreXEl.textContent = scores.X;
  scoreTiesEl.textContent = scores.Ties;
  scoreOEl.textContent = scores.O;
}

function nextRound() {
  board = ['', '', '', '', '', '', '', '', ''];
  gameActive = true;
  currentPlayer = 'X';
  statusEl.textContent = "Player X's Turn";
  statusEl.className = "status-turn x-turn";

  cells.forEach(cell => {
    cell.textContent = '';
    cell.className = 'cell';
  });
}

function resetAll() {
  scores = { X: 0, O: 0, Ties: 0 };
  updateScores();
  nextRound();
}
