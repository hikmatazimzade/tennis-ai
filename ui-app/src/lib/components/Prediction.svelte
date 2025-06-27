<script>
  import { onMount } from "svelte";

  let playersLookup = [];

  let player1InputName = "Novak Djokovic";
  let player2InputName = "Pete Sampras";

  let player1Id = 104925;
  let player2Id = 101948;

  let inputSurface = "hard";
  let inputTournamentLevel = "A";
  let inputDrawSize = 64;

  async function fetchPlayersLookup() {
    try {
      const response = await fetch("http://localhost:8000/players-lookup");
      if (!response.ok) {
        throw new Error(`HTTP Error Status!: ${response.status}`);
      }
      playersLookup = await response.json();
    } catch (err) {
      let errorMessage = err.message;
      console.log(`Error Message: ${errorMessage}`);
    }
  }

  onMount(() => {
    fetchPlayersLookup();
  });

  $: console.log(playersLookup);
</script>

<main>
  <div class="container">
    <div class="header">
      <h1>Tennis Match Predictor</h1>
      <p>AI-powered predictions for professional tennis matches</p>
    </div>
    <div class="prediction-section">
      <div class="input-card">
        <div class="players-input">
          <div class="player-input-section">
            <label class="player-label">Player 1</label>
            <input
              type="text"
              class="player-input"
              placeholder="Enter player name"
              value="Novak Djokovic"
            />
            <div class="entry-group">
              <label class="entry-label">Entry Type</label>
              <select class="entry-select">
                <option value="ALT" selected>Alternate (ALT)</option>
                <option value="Alt">Alternate (Alt)</option>
                <option value="LL">Lucky Loser (LL)</option>
                <option value="PR">Protected Ranking (PR)</option>
                <option value="Q">Qualifier (Q)</option>
                <option value="SE">Special Exempt (SE)</option>
                <option value="WC">Wild Card (WC)</option>
              </select>
            </div>
          </div>
          <div class="vs-divider">VS</div>
          <div class="player-input-section">
            <label class="player-label">Player 2</label>
            <input
              type="text"
              class="player-input"
              placeholder="Enter player name"
              value="Carlos Alcaraz"
            />
            <div class="entry-group">
              <label class="entry-label">Entry Type</label>
              <select class="entry-select">
                <option value="ALT" selected>Alternate (ALT)</option>
                <option value="Alt">Alternate (Alt)</option>
                <option value="LL">Lucky Loser (LL)</option>
                <option value="PR">Protected Ranking (PR)</option>
                <option value="Q">Qualifier (Q)</option>
                <option value="SE">Special Exempt (SE)</option>
                <option value="WC">Wild Card (WC)</option>
              </select>
            </div>
          </div>
        </div>
        <div class="match-details">
          <div class="input-group">
            <label class="input-label">Surface</label>
            <select class="select-input">
              <option value="hard" selected>Hard Court</option>
              <option value="clay">Clay Court</option>
              <option value="grass">Grass Court</option>
              <option value="carpet">Carpet</option>
            </select>
          </div>
          <div class="input-group">
            <label class="input-label">Tournament Level</label>
            <select class="select-input">
              <option value="A" selected>ATP Tour (A)</option>
              <option value="D">Davis Cup (D)</option>
              <option value="F">Tour Finals (F)</option>
              <option value="G">Grand Slam (G)</option>
              <option value="M">Masters (M)</option>
            </select>
          </div>
          <div class="input-group">
            <label class="input-label">Draw Size</label>
            <select class="select-input">
              <option value="128">128 Players</option>
              <option value="64" selected>64 Players</option>
              <option value="32">32 Players</option>
              <option value="16">16 Players</option>
            </select>
          </div>
        </div>
        <button class="predict-button">Predict Match</button>
      </div>
      <!-- Result Card -->
      <div class="result-card">
        <h2 class="result-title">Prediction Result</h2>
        <div class="winner-section">
          <div class="winner-label">Predicted Winner</div>
          <div class="winner-name">Carlos Alcaraz</div>
        </div>
        <div class="confidence-section">
          <div class="confidence-label">Confidence Score</div>
          <div class="confidence-score">87.3%</div>
          <div class="confidence-bar"><div class="confidence-fill"></div></div>
        </div>
        <div class="match-summary">
          <div class="summary-item">
            <div class="summary-value">Hard Court</div>
            <div class="summary-label">Surface</div>
          </div>
          <div class="summary-item">
            <div class="summary-value">ATP Tour</div>
            <div class="summary-label">Tournament</div>
          </div>
          <div class="summary-item">
            <div class="summary-value">64 Players</div>
            <div class="summary-label">Draw Size</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
    font-family:
      "Inter",
      -apple-system,
      BlinkMacSystemFont,
      "Segoe UI",
      Roboto,
      sans-serif;
    background: linear-gradient(135deg, #182768 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
  }
  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem;
  }
  .header {
    text-align: center;
    margin-bottom: 3rem;
  }
  .header h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }
  .header p {
    color: rgba(255, 255, 255, 0.8);
    font-size: 1.1rem;
  }
  .prediction-section {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
  }
  .input-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
  }
  .input-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #182768, #764ba2);
  }
  .players-input {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    margin-bottom: 2rem;
  }
  .player-input-section {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    width: 100%;
    max-width: 400px;
  }
  .player-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
  }
  .player-input {
    width: 100%;
    padding: 1.25rem;
    border: 2px solid #e2e8f0;
    border-radius: 16px;
    font-size: 1.1rem;
    background: #f8fafc;
    transition: all 0.3s ease;
    outline: none;
    text-align: center;
    font-weight: 600;
    box-sizing: border-box;
  }
  .player-input:focus {
    border-color: #182768;
    background: white;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(24, 39, 104, 0.1);
  }
  .entry-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-top: 0.5rem;
  }
  .entry-label {
    font-size: 0.75rem;
    font-weight: 500;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
  }
  .entry-select {
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 0.875rem;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
    outline: none;
    text-align: center;
  }
  .entry-select:focus {
    border-color: #182768;
    box-shadow: 0 0 0 3px rgba(24, 39, 104, 0.1);
  }
  .vs-divider {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 700;
    color: #182768;
    background: #f0f4ff;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    border: 3px solid #182768;
    margin: 0.5rem 0;
  }
  .match-details {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
  }
  .input-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .input-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: #4a5568;
  }
  .select-input {
    padding: 1rem;
    border: 2px solid #e2e8f0;
    border-radius: 12px;
    font-size: 1rem;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
    outline: none;
  }
  .select-input:focus {
    border-color: #182768;
    box-shadow: 0 0 0 3px rgba(24, 39, 104, 0.1);
  }
  .predict-button {
    background: linear-gradient(135deg, #182768, #764ba2);
    color: white;
    padding: 1.25rem 3rem;
    border: none;
    border-radius: 16px;
    font-size: 1.1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    margin: 0 auto;
    display: block;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  .predict-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(24, 39, 104, 0.3);
  }
  .predict-button:active {
    transform: translateY(0);
  }
  .result-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
    text-align: center;
  }
  .result-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #10b981, #3b82f6);
  }
  .result-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 2rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .winner-section {
    margin-bottom: 2rem;
  }
  .winner-label {
    font-size: 0.875rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
  }
  .winner-name {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #10b981, #3b82f6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
  }
  .confidence-section {
    background: #f8fafc;
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid #e2e8f0;
  }
  .confidence-label {
    font-size: 0.875rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
  }
  .confidence-score {
    font-size: 3rem;
    font-weight: 700;
    color: #182768;
    margin-bottom: 0.5rem;
  }
  .confidence-bar {
    width: 100%;
    height: 12px;
    background: #e2e8f0;
    border-radius: 6px;
    overflow: hidden;
    margin-top: 1rem;
  }
  .confidence-fill {
    height: 100%;
    background: linear-gradient(90deg, #3b82f6, #10b981);
    width: 87%;
    border-radius: 6px;
    transition: width 0.6s ease;
  }
  .match-summary {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
  }
  .summary-item {
    text-align: center;
  }
  .summary-value {
    font-size: 1rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.25rem;
  }
  .summary-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }
    .header h1 {
      font-size: 2rem;
    }
    .vs-divider {
      width: 50px;
      height: 50px;
      font-size: 1.25rem;
    }
    .match-details {
      grid-template-columns: 1fr;
    }
    .winner-name {
      font-size: 2rem;
    }
    .confidence-score {
      font-size: 2.5rem;
    }
  }
  @media (max-width: 480px) {
    .player-input-section {
      gap: 0.5rem;
    }
    .predict-button {
      padding: 1rem 2rem;
      font-size: 1rem;
    }
  }
</style>
