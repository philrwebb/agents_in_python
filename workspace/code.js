// Space Invaders Game
// Player controls, enemy AI, shooting, collision detection

const canvas = document.getElementById('game-canvas');
const ctx = canvas.getContext('2d');
const scoreDisplay = document.getElementById('score-display');
const gameOverScreen = document.getElementById('game-over');
const victoryScreen = document.getElementById('victory');
const startScreen = document.getElementById('start-screen');
const restartBtns = document.querySelectorAll('.restart-btn');
const startBtn = document.getElementById('start-btn');

// Game state
let gameRunning = false;
let score = 0;
let animationId = null;
let gameInterval = null;

// Player
const player = {
    x: 0,
    y: 0,
    width: 30,
    height: 30,
    color: '#00ff00',
    speed: 5,
    dx: 0,
    canShoot: true,
    lastShot: 0
};

// Bullet
let bullets = [];
let enemyBullets = [];
let lastEnemyShot = 0;
const enemyShotInterval = 800;

// Enemies
let enemies = [];
let enemySpeed = 2;
let enemyDropY = 0;

// Asteroids/Ships destroyed
let shipsDestroyed = 0;
const rows = 4;
const cols = 8;

// Input handling
let keys = {};

// Initialize player position
function initPlayer() {
    player.x = canvas.width / 2 - player.width / 2;
    player.y = canvas.height - player.height - 20;
    player.dx = 0;
    player.canShoot = true;
    player.lastShot = 0;
    shipsDestroyed = 0;
    bullets = [];
    enemyBullets = [];
    lastEnemyShot = Date.now();
    enemies = [];
    score = 0;
    scoreDisplay.textContent = 'Score: ' + score;
}

// Initialize game
function initGame() {
    keys = {};
    initPlayer();
    
    // Spawn enemies
    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
            const type = (r + c) % 3;
            const typeIndex = type === 0 ? 0 : type === 1 ? 1 : 2;
            enemies.push({
                x: 50 + c * 50,
                y: 50 + r * 40,
                width: 25,
                height: 25,
                color: getEnemyColor(type),
                type: type,
                column: c,
                dx: enemySpeed + (r / rows),
                dy: 0,
                active: true
            });
        }
    }
    
    gameRunning = true;
    startScreen.classList.add('hidden');
    gameOverScreen.classList.add('hidden');
    victoryScreen.classList.add('hidden');
    
    if (animationId) cancelAnimationFrame(animationId);
    animationId = requestAnimationFrame(update);
}

// Draw retro style rectangles for different alien types
function getEnemyColor(type) {
    const colors = ['#ff0000', '#00ff00', '#0000ff'];
    return colors[type];
}

// Draw player ship
function drawPlayer() {
    ctx.fillStyle = player.color;
    
    ctx.fillRect(player.x, player.y + 20, player.width, 10);
    ctx.fillRect(player.x + 5, player.y + 12, 20, 10);
    ctx.fillStyle = '#00cc00';
    ctx.fillRect(player.x + 12, player.y, 6, 15);
}

// Draw bullet
function drawBullets() {
    ctx.fillStyle = '#ffff00';
    for (let i = 0; i < bullets.length; i++) {
        ctx.fillRect(bullets[i].x, bullets[i].y, 3, 10);
    }
}

// Draw enemies
function drawEnemies() {
    for (let i = 0; i < enemies.length; i++) {
        const e = enemies[i];
        if (!e.active) continue;
        
        ctx.fillStyle = e.color;
        
        // Draw enemy shape (different based on type)
        const cx = e.x + e.width / 2;
        const cy = e.y + e.height / 2;
        
        // Common shape
        ctx.fillRect(e.x + 5, e.y + e.height - 5, 15, 5);
        ctx.fillRect(e.x, e.y + e.height - 10, 5, 5);
        ctx.fillRect(e.x + e.width - 5, e.y + e.height - 10, 5, 5);
        
        // Body
        ctx.fillRect(e.x + 5, e.y, 15, 10);
        
        // Eyes
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(e.x + 8, e.y + 10, 3, 3);
        ctx.fillRect(e.x + 14, e.y + 10, 3, 3);
        
        // Legs
        ctx.fillStyle = e.color;
        ctx.fillRect(e.x + 6, e.y + e.height - 5, 2, 3);
        ctx.fillRect(e.x + 17, e.y + e.height - 5, 2, 3);
    }
}

// Draw asteroids (simple retro style)
function drawAsteroids() {
    // Asteroids spawn
    if (Math.random() < 0.02) {
        const asteroids = Math.floor(Math.random() * 5) + 1;
        for (let a = 0; a < asteroids; a++) {
            const ax = Math.random() * (canvas.width - 40) + 20;
            const ay = Math.random() * (canvas.height / 2 - 40) + 20;
            const size = 5 + Math.random() * 10;
            
            // Draw jagged asteroid
            for (let i = 0; i < 6; i++) {
                ctx.beginPath();
                ctx.arc(ax + (Math.random() - 0.5) * 10, ay + (Math.random() - 0.5) * 10, 2 + Math.random() * 5, 0, Math.PI * 2);
                ctx.fill();
            }
        }
    }
}

// Draw score
function drawScore() {
    ctx.fillStyle = '#00ff00';
    ctx.font = '20px Courier New';
    ctx.fillText('SCORE: ' + score, 10, 30);
    ctx.font = '16px Courier New';
    ctx.fillText('SHIPS DESTROYED: ' + shipsDestroyed, 10, 50);
}

// Draw game border
function drawBorder() {
    ctx.strokeStyle = '#00ff00';
    ctx.lineWidth = 2;
    ctx.strokeRect(10, 10, canvas.width - 20, canvas.height - 20);

}

// Fire from a surviving alien at the front of a column.
function updateEnemyBullets() {
    const now = Date.now();
    if (now - lastEnemyShot >= enemyShotInterval) {
        const frontAliens = new Map();
        enemies.filter(e => e.active).forEach(e => {
            const front = frontAliens.get(e.column);
            if (!front || e.y > front.y) frontAliens.set(e.column, e);
        });
        const shooters = [...frontAliens.values()];
        if (shooters.length) {
            const shooter = shooters[Math.floor(Math.random() * shooters.length)];
            enemyBullets.push({
                x: shooter.x + shooter.width / 2 - 2,
                y: shooter.y + shooter.height,
                width: 4,
                height: 12,
                speed: 4
            });
        }
        lastEnemyShot = now;
    }

    ctx.fillStyle = '#ff6688';
    enemyBullets.forEach(b => {
        b.y += b.speed;
        ctx.fillRect(b.x, b.y, b.width, b.height);
        if (b.x < player.x + player.width && b.x + b.width > player.x &&
            b.y < player.y + player.height && b.y + b.height > player.y) {
            gameRunning = false;
            gameOverScreen.querySelector('p').textContent = 'Final Score: ' + score;
            gameOverScreen.classList.remove('hidden');
        }
    });
    enemyBullets = enemyBullets.filter(b => b.y < canvas.height);
}

// Update game state
function update() {
    if (!gameRunning) return;
    
    // Clear canvas
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    drawBorder();
    drawAsteroids();
    
    // Move player
    player.dx = ((keys.ArrowRight || keys.KeyD ? 1 : 0) -
        (keys.ArrowLeft || keys.KeyA ? 1 : 0)) * player.speed;
    if (keys.Space) shoot();
    player.x += player.dx;
    if (player.x < 10) player.x = 10;
    if (player.x > canvas.width - player.width - 10) player.x = canvas.width - player.width - 10;
    
    drawPlayer();
    
    // Update bullets
    bullets.forEach(b => { b.y -= b.speed; });
    bullets = bullets.filter(b => b.y + 10 >= 0);
    
    // Draw bullets
    drawBullets();
    
    // Update enemies
    const hitEdge = enemies.some(e => e.active &&
        (e.x + e.dx + e.width >= canvas.width - 10 || e.x + e.dx <= 10));
    enemies.forEach(e => {
        if (!e.active) return;
        if (hitEdge) {
            e.dx = -e.dx;
            e.y += 10;
        }
        e.x += e.dx;
    });
    
    drawEnemies();
    drawScore();
    
    // Collision detection
    for (let i = bullets.length - 1; i >= 0; i--) {
        for (let j = 0; j < enemies.length; j++) {
            const b = bullets[i];
            const e = enemies[j];
            if (!e.active) continue;
            
            if (b.x < e.x + e.width &&
                b.x + 3 > e.x &&
                b.y < e.y + e.height &&
                b.y + 10 > e.y) {
                
                // Hit enemy
                e.active = false;
                bullets.splice(i, 1);
                score += 10;
                shipsDestroyed += 1;
                scoreDisplay.textContent = 'Score: ' + score;
                
                // Check victory
                if (enemies.every(e => !e.active)) {
                    gameRunning = false;
                    victoryScreen.querySelector('p').textContent = 'Final Score: ' + score;
                    victoryScreen.classList.remove('hidden');
                }
                break;
            }
        }
    }
    
    // Check player collision with enemies
    for (let j = 0; j < enemies.length; j++) {
        const e = enemies[j];
        if (!e.active) continue;
        
        if (e.y + e.height >= player.y) {
            e.active = false;
            bullets.forEach(b => b.y = -100);
            gameRunning = false;
            gameOverScreen.querySelector('p').textContent = 'Final Score: ' + score;
            gameOverScreen.classList.remove('hidden');
        }
    }
    
    // Remove inactive enemies
    enemies = enemies.filter(e => e.active);
    
    if (gameRunning) updateEnemyBullets();

    if (gameRunning) {
        animationId = requestAnimationFrame(update);
    }
}

// Shoot
function shoot() {
    const now = Date.now();
    if (gameRunning && now - player.lastShot >= 400) {
        bullets.push({
            x: player.x + player.width / 2 - 1.5,
            y: player.y,
            speed: 7
        });
        player.lastShot = now;
    }
}

// Event listeners
document.addEventListener('keydown', (e) => {
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Space'].includes(e.code) && gameRunning) {
        e.preventDefault();
    }
    keys[e.code] = true;
});

document.addEventListener('keyup', (e) => {
    keys[e.code] = false;
});

window.addEventListener('blur', () => { keys = {}; });
canvas.addEventListener('mousedown', shoot);

// Both end screens can restart the game.
restartBtns.forEach(button => button.addEventListener('click', initGame));

startBtn.addEventListener('click', () => {
    initGame();
});

// Initial render
initPlayer();
