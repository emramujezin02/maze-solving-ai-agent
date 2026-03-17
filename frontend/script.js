const canvas = document.getElementById("mazeCanvas");
const ctx = canvas.getContext("2d");
const status = document.getElementById("status");

let maze, pos, goal, cell;
let playTimer = null;
let training = false;

const PLAY_DELAY = 80;

// ================= API =================
async function api(url, data = {}) {
    const r = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });
    return r.json();
}

// ================= DRAW =================
function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let r = 0; r < maze.length; r++) {
        for (let c = 0; c < maze[0].length; c++) {
            ctx.fillStyle = maze[r][c] ? "#000" : "#fff";
            ctx.fillRect(c * cell, r * cell, cell, cell);
        }
    }

    // goal
    ctx.fillStyle = "#00c853";
    ctx.fillRect(goal.col * cell, goal.row * cell, cell, cell);

    // agent
    ctx.fillStyle = "#d50000";
    ctx.beginPath();
    ctx.arc(
        pos.col * cell + cell / 2,
        pos.row * cell + cell / 2,
        cell / 3,
        0,
        Math.PI * 2
    );
    ctx.fill();
}

// ================= RESET =================
async function resetMaze() {
    if (playTimer) {
        clearInterval(playTimer);
        playTimer = null;
    }

    const d = await api("/api/reset");
    maze = d.maze;
    pos = d.state;
    goal = d.goal;

    const MAX_CANVAS_HEIGHT = window.innerHeight * 0.6; // 60% ekrana
    const rows = maze.length;
    const cols = maze[0].length;

    cell = Math.floor(MAX_CANVAS_HEIGHT / rows);
    if (cell < 4) cell = 4; 

    canvas.height = rows * cell;
    canvas.width  = cols * cell;

    draw();
    status.innerText = "New maze loaded";
}

// ================= PLAY (BFS PATH) =================
async function play() {
    if (training || playTimer) return;

    status.innerText = "Playing best path (BFS)...";

    const d = await api("/api/play_best");

    if (d.error) {
        alert(d.error);
        status.innerText = "No solution ❌";
        return;
    }

    const path = d.path;
    let i = 0;

    playTimer = setInterval(() => {
        if (i >= path.length) {
            clearInterval(playTimer);
            playTimer = null;
            status.innerText = "Goal reached 🎯";
            return;
        }

        const [r, c] = path[i];
        pos = { row: r, col: c };
        draw();
        i++;
    }, PLAY_DELAY);
}

// ================= TRAIN =================
document.getElementById("btnTrain").onclick = async () => {
    if (playTimer) {
        clearInterval(playTimer);
        playTimer = null;
    }

    training = true;
    status.innerText = "Training in progress...";

    try {
        const r = await api("/api/train_current");

        if (r.error) {
            alert("ERROR: " + r.error);
            status.innerText = "Training failed ❌";
        } else {
            alert(
                "Training complete!\n" 
            );
            status.innerText = "Training finished ✅";
        }
    } catch (e) {
        alert("Server error during training");
        status.innerText = "Server error ❌";
    }

    training = false;
};

// ================= BUTTONS =================
document.getElementById("btnReset").onclick = resetMaze;
document.getElementById("btnPlay").onclick = play;

// ================= INIT =================
resetMaze();
