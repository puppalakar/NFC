const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('high-score');
const overlay = document.getElementById('game-overlay');
const overlayTitle = document.getElementById('overlay-title');
const overlayText = document.getElementById('overlay-text');
const startBtn = document.getElementById('start-btn');

// Game Constants
const gridSize = 20;
const tileCount = canvas.width / gridSize;
const baseSpeed = 150; // ms per frame

// Game Variables
let snake = [];
let food = {};
let dx = 0;
let dy = 0;
let score = 0;
let highScore = localStorage.getItem('snackHighScore') || 0;
let gameLoop;
let isPaused = false;
let isGameOver = false;
let hasStarted = false;

highScoreElement.textContent = highScore;

function initGame() {
    snake = [
        { x: 10, y: 10 },
        { x: 10, y: 11 },
        { x: 10, y: 12 }
    ];
    dx = 0;
    dy = -1;
    score = 0;
    updateScore();
    placeFood();
    isGameOver = false;
    isPaused = false;
    hasStarted = true;
    overlay.classList.remove('visible');
    
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, baseSpeed);
}

function placeFood() {
    food = {
        x: Math.floor(Math.random() * tileCount),
        y: Math.floor(Math.random() * tileCount)
    };
    // Ensure food doesn't spawn on snake
    for (let segment of snake) {
        if (segment.x === food.x && segment.y === food.y) {
            placeFood();
            break;
        }
    }
}

function update() {
    if (isPaused || isGameOver) return;

    // Calculate new head position
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };

    // Wall Collision
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        gameOver();
        return;
    }

    // Self Collision
    for (let i = 0; i < snake.length; i++) {
        if (head.x === snake[i].x && head.y === snake[i].y) {
            gameOver();
            return;
        }
    }

    snake.unshift(head);

    // Food Collision
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        updateScore();
        placeFood();
        // Slightly increase speed
        clearInterval(gameLoop);
        const newSpeed = Math.max(50, baseSpeed - Math.floor(score / 2));
        gameLoop = setInterval(update, newSpeed);
    } else {
        snake.pop(); // Remove tail if no food eaten
    }

    draw();
}

function draw() {
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw Grid (subtle)
    ctx.strokeStyle = 'rgba(102, 252, 241, 0.05)';
    for(let i=0; i<tileCount; i++) {
        ctx.beginPath();
        ctx.moveTo(i*gridSize, 0);
        ctx.lineTo(i*gridSize, canvas.height);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(0, i*gridSize);
        ctx.lineTo(canvas.width, i*gridSize);
        ctx.stroke();
    }

    // Draw Food with glow
    ctx.shadowBlur = 15;
    ctx.shadowColor = '#ff007f';
    ctx.fillStyle = '#ff007f';
    ctx.beginPath();
    ctx.arc(food.x * gridSize + gridSize/2, food.y * gridSize + gridSize/2, gridSize/2 - 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.shadowBlur = 0; // Reset shadow

    // Draw Snake
    snake.forEach((segment, index) => {
        if (index === 0) {
            ctx.fillStyle = '#ffffff'; // Head is white
            ctx.shadowBlur = 10;
            ctx.shadowColor = '#66fcf1';
        } else {
            ctx.fillStyle = '#66fcf1'; // Body
            ctx.shadowBlur = index === snake.length -1 ? 5 : 0;
            ctx.shadowColor = '#66fcf1';
            
            // Gradient effect for body
            ctx.globalAlpha = 1 - (index / snake.length) * 0.6;
        }

        ctx.fillRect(segment.x * gridSize + 1, segment.y * gridSize + 1, gridSize - 2, gridSize - 2);
        ctx.globalAlpha = 1; // Reset alpha
        ctx.shadowBlur = 0; // Reset shadow
    });
}

function gameOver() {
    isGameOver = true;
    clearInterval(gameLoop);
    
    if (score > highScore) {
        highScore = score;
        localStorage.setItem('snackHighScore', highScore);
        highScoreElement.textContent = highScore;
    }

    overlayTitle.textContent = 'GAME OVER';
    overlayTitle.style.color = '#ff007f';
    overlayTitle.style.textShadow = '0 0 15px rgba(255, 0, 127, 0.8)';
    overlayText.textContent = `Final Score: ${score}`;
    startBtn.textContent = 'PLAY AGAIN';
    overlay.classList.add('visible');
}

function togglePause() {
    if (!hasStarted || isGameOver) return;
    
    isPaused = !isPaused;
    if (isPaused) {
        overlayTitle.textContent = 'PAUSED';
        overlayTitle.style.color = '#66fcf1';
        overlayTitle.style.textShadow = '0 0 15px rgba(102, 252, 241, 0.8)';
        overlayText.textContent = 'Press Space to Resume';
        startBtn.textContent = 'RESUME';
        overlay.classList.add('visible');
    } else {
        overlay.classList.remove('visible');
    }
}

function updateScore() {
    scoreElement.textContent = score;
    // Animate score pop
    scoreElement.style.transform = 'scale(1.3)';
    setTimeout(() => {
        scoreElement.style.transform = 'scale(1)';
    }, 150);
}

// Event Listeners
document.addEventListener('keydown', (e) => {
    // Prevent default scrolling for arrow keys and space
    if (['Space', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.code)) {
        e.preventDefault();
    }

    if (e.code === 'Space') {
        if (!hasStarted || isGameOver) {
            initGame();
        } else {
            togglePause();
        }
        return;
    }

    if (isPaused || isGameOver) return;

    switch(e.key) {
        case 'ArrowUp':
            if (dy !== 1) { dx = 0; dy = -1; }
            break;
        case 'ArrowDown':
            if (dy !== -1) { dx = 0; dy = 1; }
            break;
        case 'ArrowLeft':
            if (dx !== 1) { dx = -1; dy = 0; }
            break;
        case 'ArrowRight':
            if (dx !== -1) { dx = 1; dy = 0; }
            break;
    }
});

startBtn.addEventListener('click', () => {
    if (isPaused && !isGameOver) {
        togglePause();
    } else {
        initGame();
    }
});

// Initial draw (empty canvas)
draw();
