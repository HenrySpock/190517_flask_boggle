// set initial score and remaining time
let score = 0;
let remainingTime = 60;

// get form elements
const wordForm = document.getElementById('word-form');
const wordInput = document.getElementById('word-input');
const submitButton = document.getElementById('submit-guess');

// get result and score elements
const resultDiv = document.getElementById('result');
const scoreElement = document.getElementById('score');

// get game over element
const gameOverElement = document.getElementById('game-over');

// add submit event listener to form
wordForm.addEventListener('submit', (event) => {
  event.preventDefault();

  // check if time is up
  if (remainingTime <= 0) {
    return;
  }

  const word = wordInput.value.trim().toLowerCase();
  wordInput.value = '';
  resultDiv.textContent = '';

  axios.get('/checkword', {
    params: {
      word: word,
      board: '{{ board | tojson }}'
    }
  })
  .then((response) => {
    if (response.data.result === 'ok') {
      resultDiv.textContent = `${word} is a valid word!`;
      score += word.length;
      scoreElement.textContent = score;
    } else if (response.data.result === 'not-word') {
      resultDiv.textContent = `${word} is not a valid word.`;
    } else {
      resultDiv.textContent = `${word} is not on the board.`;
    }
  })
  .catch((error) => {
    console.log(error);
  });

  return false; // prevent the page from refreshing
});

// update remaining time every second
const timer = setInterval(() => {
  remainingTime--;
  const timeElement = document.getElementById('time');
  timeElement.textContent = remainingTime;
  
  if (remainingTime <= 0) {
    // stop timer and show game over message
    clearInterval(timer);
    gameOverElement.style.display = 'block';
    wordInput.disabled = true;
    submitButton.disabled = true;

    // AJAX request to check and store score
    axios.post('/game-over', {score: score})
      .then((response) => {
        const highScore = response.data.high_score;
        const numPlays = response.data.num_plays;

        // update high score and times played
        const highScoreElement = document.getElementById('high-score-count');
        const numPlaysElement = document.getElementById('times-played-count');
        highScoreElement.textContent = highScore;
        numPlaysElement.textContent = numPlays;
      })
      .catch((error) => {
        console.log(error);
      });

  }
}, 1000);

 