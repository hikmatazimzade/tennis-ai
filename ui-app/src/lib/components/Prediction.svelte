<script>
  import { onMount } from "svelte";

  let playersLookup = [];
  let player1Input = "Novak Djokovic";
  let player2Input = "Pete Sampras";

  let player1Id = 104925;
  let player2Id = 101948;

  let player1Suggestions = [];
  let player2Suggestions = [];

  let showPlayer1Dropdown = false;
  let showPlayer2Dropdown = false;

  let player1InputRef;
  let player2InputRef;

  let player1Entry = "ALT";
  let player2Entry = "ALT";

  let surface = "hard";
  let tournamentLevel = "A";
  let drawSize = "64";

  let predictionResult = null;
  let isLoading = false;
  let predictionError = null;

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

  function filterPlayers(query) {
    if (!query || query.length < 1) return [];

    const filtered = playersLookup
      .map((playerObj) => {
        const name = Object.keys(playerObj)[0];
        const id = Object.values(playerObj)[0];
        return { name, id };
      })
      .filter((player) =>
        player.name.toLowerCase().includes(query.toLowerCase())
      )
      .slice(0, 10);

    return filtered;
  }

  function handlePlayer1Input(event) {
    player1Input = event.target.value;
    player1Suggestions = filterPlayers(player1Input);
    showPlayer1Dropdown =
      player1Suggestions.length > 0 && player1Input.length > 0;

    const exactMatch = player1Suggestions.find(
      (p) => p.name.toLowerCase() === player1Input.toLowerCase()
    );
    player1Id = exactMatch ? exactMatch.id : null;
  }

  function handlePlayer2Input(event) {
    player2Input = event.target.value;
    player2Suggestions = filterPlayers(player2Input);
    showPlayer2Dropdown =
      player2Suggestions.length > 0 && player2Input.length > 0;

    const exactMatch = player2Suggestions.find(
      (p) => p.name.toLowerCase() === player2Input.toLowerCase()
    );
    player2Id = exactMatch ? exactMatch.id : null;
  }

  function selectPlayer1(player) {
    player1Input = player.name;
    player1Id = player.id;
    showPlayer1Dropdown = false;
    player1InputRef.blur();
  }

  function selectPlayer2(player) {
    player2Input = player.name;
    player2Id = player.id;
    showPlayer2Dropdown = false;
    player2InputRef.blur();
  }

  function handlePlayer1Blur() {
    setTimeout(() => {
      showPlayer1Dropdown = false;
    }, 200);
  }

  function handlePlayer2Blur() {
    setTimeout(() => {
      showPlayer2Dropdown = false;
    }, 200);
  }

  function handlePlayer1Focus() {
    if (player1Input.length > 0) {
      player1Suggestions = filterPlayers(player1Input);
      showPlayer1Dropdown = player1Suggestions.length > 0;
    }
  }

  function handlePlayer2Focus() {
    if (player2Input.length > 0) {
      player2Suggestions = filterPlayers(player2Input);
      showPlayer2Dropdown = player2Suggestions.length > 0;
    }
  }

  async function handlePredictMatch() {
    console.log("Match Configuration:");
    console.log("Player 1:", {
      name: player1Input,
      id: player1Id,
      entry: player1Entry,
    });

    console.log("Player 2:", {
      name: player2Input,
      id: player2Id,
      entry: player2Entry,
    });

    console.log("Surface:", surface);
    console.log("Tournament Level:", tournamentLevel);
    console.log("Draw Size:", drawSize);

    if (!player1Id || !player2Id) {
      alert("Please select valid players from the suggestions");
      return;
    }

    const matchData = {
      player_1_id: player1Id,
      player_2_id: player2Id,
      player_1_entry: player1Entry,
      player_2_entry: player2Entry,
      surface: surface,
      tourney_level: tournamentLevel,
      draw_size: parseInt(drawSize),
    };

    console.log("Match data that will be sent to backend:", matchData);

    predictionResult = null;
    predictionError = null;
    isLoading = true;

    try {
      const response = await fetch("http://127.0.0.1:8000/prediction", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(matchData),
      });

      if (!response.ok) {
        throw new Error(
          `HTTP Error: ${response.status} - ${response.statusText}`
        );
      }

      const result = await response.json();
      console.log("Prediction result:", result);

      predictionResult = {
        winner: result.winner_player,
        confidence: result.confidence,
      };
    } catch (error) {
      console.error("Error making prediction:", error);
      predictionError = error.message;
    } finally {
      isLoading = false;
    }
  }

  $: console.log("Players lookup loaded:", playersLookup.length);
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
            <div class="autocomplete-wrapper">
              <input
                bind:this={player1InputRef}
                type="text"
                class="player-input"
                placeholder="Enter player name"
                bind:value={player1Input}
                on:input={handlePlayer1Input}
                on:focus={handlePlayer1Focus}
                on:blur={handlePlayer1Blur}
                autocomplete="off"
              />
              {#if showPlayer1Dropdown}
                <div class="suggestions-dropdown">
                  {#each player1Suggestions.slice(0, 10) as player (player.id)}
                    <div
                      class="suggestion-item"
                      on:mousedown={(e) => {
                        e.preventDefault();
                        selectPlayer1(player);
                      }}
                      role="button"
                      tabindex="0"
                    >
                      {player.name}
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
            <div class="entry-group">
              <label class="entry-label">Entry Type</label>
              <select class="entry-select" bind:value={player1Entry}>
                <option value="ALT">Alternate (ALT)</option>
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
            <div class="autocomplete-wrapper">
              <input
                bind:this={player2InputRef}
                type="text"
                class="player-input"
                placeholder="Enter player name"
                bind:value={player2Input}
                on:input={handlePlayer2Input}
                on:focus={handlePlayer2Focus}
                on:blur={handlePlayer2Blur}
                autocomplete="off"
              />
              {#if showPlayer2Dropdown}
                <div class="suggestions-dropdown">
                  {#each player2Suggestions.slice(0, 10) as player (player.id)}
                    <div
                      class="suggestion-item"
                      on:mousedown={(e) => {
                        e.preventDefault();
                        selectPlayer2(player);
                      }}
                      role="button"
                      tabindex="0"
                    >
                      {player.name}
                    </div>
                  {/each}
                </div>
              {/if}
            </div>
            <div class="entry-group">
              <label class="entry-label">Entry Type</label>
              <select class="entry-select" bind:value={player2Entry}>
                <option value="ALT">Alternate (ALT)</option>
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
            <select class="select-input" bind:value={surface}>
              <option value="hard">Hard Court</option>
              <option value="clay">Clay Court</option>
              <option value="grass">Grass Court</option>
              <option value="carpet">Carpet</option>
            </select>
          </div>
          <div class="input-group">
            <label class="input-label">Tournament Level</label>
            <select class="select-input" bind:value={tournamentLevel}>
              <option value="A">ATP Tour (A)</option>
              <option value="D">Davis Cup (D)</option>
              <option value="F">Tour Finals (F)</option>
              <option value="G">Grand Slam (G)</option>
              <option value="M">Masters (M)</option>
            </select>
          </div>
          <div class="input-group">
            <label class="input-label">Draw Size</label>
            <select class="select-input" bind:value={drawSize}>
              <option value="128">128 Players</option>
              <option value="64">64 Players</option>
              <option value="32">32 Players</option>
              <option value="16">16 Players</option>
            </select>
          </div>
        </div>
        <button
          class="predict-button"
          on:click={handlePredictMatch}
          disabled={isLoading}
        >
          {#if isLoading}
            <span class="button-spinner"></span>
            Predicting...
          {:else}
            Predict Match
          {/if}
        </button>
      </div>
      <div class="result-card">
        <h2 class="result-title">Prediction Result</h2>

        {#if isLoading}
          <div class="loading-section">
            <div class="loading-spinner"></div>
            <p class="loading-text">Analyzing match data...</p>
          </div>
        {:else if predictionError}
          <div class="error-section">
            <div class="error-icon">⚠️</div>
            <p class="error-text">Error: {predictionError}</p>
            <button class="retry-button" on:click={handlePredictMatch}
              >Try Again</button
            >
          </div>
        {:else if predictionResult}
          <div class="winner-section">
            <div class="winner-label">Predicted Winner Number</div>
            <div class="winner-name">{predictionResult.winner}</div>
          </div>
          <div class="confidence-section">
            <div class="confidence-label">Confidence Score</div>
            <div class="confidence-score">{predictionResult.confidence}%</div>
            <div class="confidence-bar">
              <div
                class="confidence-fill"
                style="width: {predictionResult.confidence}%"
              ></div>
            </div>
          </div>
        {:else}
          <div class="no-prediction">
            <p class="no-prediction-text">
              Click "Predict Match" to see the prediction results
            </p>
          </div>
        {/if}

        <div class="match-summary">
          <div class="summary-item">
            <div class="summary-value">
              {surface === "hard"
                ? "Hard Court"
                : surface === "clay"
                  ? "Clay Court"
                  : surface === "grass"
                    ? "Grass Court"
                    : "Carpet"}
            </div>
            <div class="summary-label">Surface</div>
          </div>
          <div class="summary-item">
            <div class="summary-value">
              {tournamentLevel === "A"
                ? "ATP Tour"
                : tournamentLevel === "D"
                  ? "Davis Cup"
                  : tournamentLevel === "F"
                    ? "Tour Finals"
                    : tournamentLevel === "G"
                      ? "Grand Slam"
                      : "Masters"}
            </div>
            <div class="summary-label">Tournament</div>
          </div>
          <div class="summary-item">
            <div class="summary-value">{drawSize} Players</div>
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
    overflow: visible;
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

  .autocomplete-wrapper {
    position: relative;
    width: 100%;
  }

  .suggestions-dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: white;
    border: 2px solid #e2e8f0;
    border-top: none;
    border-radius: 0 0 12px 12px;
    max-height: 200px;
    overflow-y: auto;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .suggestion-item {
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
    border-bottom: 1px solid #f1f5f9;
    font-size: 1rem;
  }

  .suggestion-item:hover {
    background-color: #f8fafc;
  }

  .suggestion-item:last-child {
    border-bottom: none;
  }

  .suggestion-item:focus {
    outline: none;
    background-color: #f0f4ff;
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
    border-radius: 16px 16px 0 0;
  }

  .autocomplete-wrapper:has(.suggestions-dropdown) .player-input:focus {
    border-radius: 16px 16px 0 0;
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
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    min-width: 200px;
  }
  .predict-button:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(24, 39, 104, 0.3);
  }
  .predict-button:active:not(:disabled) {
    transform: translateY(0);
  }
  .predict-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .button-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-top: 2px solid white;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .loading-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    margin-bottom: 2rem;
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #e2e8f0;
    border-top: 4px solid #182768;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
  }

  .loading-text {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
  }

  .error-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 2rem;
    margin-bottom: 2rem;
  }

  .error-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .error-text {
    color: #ef4444;
    font-size: 1rem;
    margin-bottom: 1rem;
    text-align: center;
  }

  .retry-button {
    background: #ef4444;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .retry-button:hover {
    background: #dc2626;
    transform: translateY(-1px);
  }

  .no-prediction {
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
  }

  .no-prediction-text {
    color: #64748b;
    font-size: 1rem;
    margin: 0;
  }

  .winner-section {
    margin-bottom: 2rem;
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
    border-radius: 6px;
    transition: width 0.6s ease;
    min-width: 2%;
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
