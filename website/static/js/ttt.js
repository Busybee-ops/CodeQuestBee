document.addEventListener('DOMContentLoaded', function() {
    const resetButton = document.getElementById('reset');
    const easyButton = document.getElementById('easy');
    const mediumButton = document.getElementById('medium');
    const hardButton = document.getElementById('hard');

    if (resetButton) {
        resetButton.addEventListener('click', resetGame);
    } else {
        console.error('Element with ID "reset" not found.');
    }

    if (easyButton) {
        easyButton.addEventListener('click', () => setDifficulty('Easy'));
    } else {
        console.error('Element with ID "easy" not found.');
    }

    if (mediumButton) {
        mediumButton.addEventListener('click', () => setDifficulty('Medium'));
    } else {
        console.error('Element with ID "medium" not found.');
    }

    if (hardButton) {
        hardButton.addEventListener('click', () => setDifficulty('Hard'));
    } else {
        console.error('Element with ID "hard" not found.');
    }
});

let board = ["", "", "", "", "", "", "", "", ""];
let player = "X";
let gameOver = false;
let difficulty = "Medium";

async function computerMove() {
    try {
        const response = await fetch('/tictactoe/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                board: board,
                player: 'O',
                difficulty: difficulty
            })
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        board = data.board;
        player = data.player;
        gameOver = data.winner !== null;
        updateBoard();
        if (gameOver) {
            if (data.winner === 'Tie') {
                showMessage("It's a draw!");
            } else {
                highlightWinningCells(data.winningCombination);
                setTimeout(() => {
                    showMessage(`${data.winner} wins!`);
                }, 500); // Add a delay before showing the winning message
            }
        } else {
            updateMessage();
        }
    } catch (error) {
        console.error('Failed to fetch:', error);
    }
}

function handleMove(cell) {
    const cellIndex = parseInt(cell.id);
    if (board[cellIndex] === "" && !gameOver) {
        board[cellIndex] = player;
        cell.innerHTML = player;
        cell.classList.add("clicked");
        setTimeout(() => {
            cell.classList.remove("clicked");
        }, 300);
        checkGameOver();
        if (!gameOver) {
            player = player === "X" ? "O" : "X";
            updateMessage();
            if (player === "O") {
                setTimeout(computerMove, 500);
            }
        }
    }
}

function updateBoard() {
    for (let i = 0; i < 9; i++) {
        const cell = document.getElementById(i);
        cell.innerHTML = board[i];
        cell.style.backgroundColor = board[i] === "X" ? "#f8d7da" : board[i] === "O" ? "#d4edda" : "#f8f9fa";
    }
}

function checkGameOver() {
    const winner = checkWinner(player);
    if (winner) {
        highlightWinningCells(winner);
        setTimeout(() => {
            showMessage(player + " wins!");
        }, 500); // Add a delay before showing the winning message
        gameOver = true;
    } else if (isBoardFull()) {
        showMessage("It's a draw!");
        gameOver = true;
    }
}

function highlightWinningCells(winningCells) {
    console.log("Highlighting winning cells:", winningCells); // Debugging line
    winningCells.forEach(cellIndex => {
        const cell = document.getElementById(cellIndex);
        console.log(`Highlighting cell ${cellIndex}`); // Debugging line
        cell.classList.add("winning");
    });
}

function checkWinner(player) {
    const winningCombinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ];

    for (const combination of winningCombinations) {
        if (combination.every(index => board[index] === player)) {
            return combination;
        }
    }
    return null;
}

function isBoardFull() {
    return board.every(cell => cell !== "");
}

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    player = "X";
    gameOver = false;
    for (let i = 0; i < 9; i++) {
        const cell = document.getElementById(i);
        cell.innerHTML = "";
        cell.style.backgroundColor = "#f8f9fa";
        cell.style.transform = "scale(1)";
        cell.classList.remove("reset", "winning", "clicked");
    }
    hideMessage();
    updateMessage();
}

function setDifficulty(level) {
    difficulty = level;
    updateMessage();
    document.getElementById("easy").classList.remove("active");
    document.getElementById("medium").classList.remove("active");
    document.getElementById("hard").classList.remove("active");
    document.getElementById(level.toLowerCase()).classList.add("active");
}

function updateMessage() {
    document.getElementById("message").innerHTML = `Player ${player}'s turn`;
}

function showMessage(message) {
    const messageContainer = document.getElementById("message-container");
    const messageElement = document.getElementById("message");
    messageElement.innerHTML = message;
    messageContainer.style.display = "block";
}

function hideMessage() {
    const messageContainer = document.getElementById("message-container");
    messageContainer.style.display = "none";
    document.getElementById("message").innerHTML = "";
}