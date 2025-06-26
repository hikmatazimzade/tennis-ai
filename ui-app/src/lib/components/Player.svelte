<script>
  import { onMount } from "svelte";

  export let playerId;
  export let playerNames;

  let player = {};

  async function fetchPlayer(playerId) {
    try {
      const response = await fetch(`http://localhost:8000/players/${playerId}`);
      if (!response.ok) {
        throw new Error(`HTTP Error Status!: ${response.status}`);
      }
      player = await response.json();
    } catch (err) {
      let errorMessage = err.message;
      console.log(`Error Message: ${errorMessage}`);
    }
  }

  onMount(() => {
    fetchPlayer(playerId);
  });
  $: console.log(player);
</script>

<main>
  <div class="container">
    <div class="header">
      <h1>Tennis Player Profile</h1>
      <p>Professional player statistics and performance metrics</p>
    </div>
    <div class="player-card">
      <div class="player-header">
        <div class="player-name">{player.name}</div>
        <div class="player-country">{player.ioc}</div>
        <div class="rank-badge">Rank #{player.rank}</div>
        <div class="hand-indicator">✋ {player.hand}</div>
      </div>
      <div class="stats-section">
        <div class="stats-group">
          <div class="stats-title">Player Information</div>
          <div class="stat-item">
            <span class="stat-label">Player ID</span>
            <span class="stat-value">{playerId}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Age</span>
            <span class="stat-value">{player.age} years</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Height</span>
            <span class="stat-value">{player.height}m</span>
          </div>
        </div>
        <div class="stats-group">
          <div class="stats-title">Rankings & Points</div>
          <div class="stat-item">
            <span class="stat-label">Current Rank</span>
            <span class="stat-value">#{player.rank}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">Rank Points</span>
            <span class="stat-value">{player.rank_points}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">ELO Rating</span>
            <span class="stat-value">{player.elo}</span>
          </div>
        </div>
      </div>
      <div class="performance-highlight">
        <span class="win-ratio-value">{player.win_rate}%</span>
        <div class="win-ratio-label">Career Win Rate</div>
        <div class="match-breakdown">
          <div class="match-stat">
            <span class="match-number">{player.won_match}</span>
            <div class="match-label">Matches Won</div>
          </div>
          <div class="match-stat">
            <span class="match-number">{player.lost_match}</span>
            <div class="match-label">Matches Lost</div>
          </div>
        </div>
        <div class="total-matches">Total Matches: {player.total_match}</div>
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
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  .header {
    text-align: center;
    margin-bottom: 2rem;
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
  .player-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 24px;
    padding: 3rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
    animation: fadeIn 0.5s ease;
  }
  .player-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 6px;
    background: linear-gradient(90deg, #667eea, #764ba2);
  }
  .player-header {
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
  }
  .player-name {
    font-size: 3rem;
    font-weight: 700;
    color: #2d3748;
    margin-bottom: 1rem;
  }
  .player-country {
    display: inline-flex;
    align-items: center;
    background: #f7fafc;
    color: #4a5568;
    padding: 0.75rem 1.5rem;
    border-radius: 16px;
    font-size: 1.1rem;
    font-weight: 600;
    border: 2px solid #e2e8f0;
    margin-bottom: 1rem;
  }
  .rank-badge {
    background: linear-gradient(135deg, #667eea, #5c4572);
    color: white;
    padding: 1rem 2rem;
    border-radius: 20px;
    font-weight: 700;
    font-size: 2rem;
    display: inline-block;
    margin-bottom: 1rem;
  }
  .hand-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.75rem;
    background: #fef3c7;
    color: #92400e;
    padding: 0.75rem 1.25rem;
    border-radius: 16px;
    font-size: 1rem;
    font-weight: 500;
  }
  .stats-section {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 3rem;
  }
  .stats-group {
    background: #f8fafc;
    border-radius: 20px;
    padding: 2rem;
    border: 2px solid #e2e8f0;
  }
  .stats-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #374151;
    margin-bottom: 1.5rem;
    text-align: center;
  }
  .stat-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    border-bottom: 1px solid #e2e8f0;
  }
  .stat-item:last-child {
    border-bottom: none;
  }
  .stat-label {
    font-size: 1rem;
    color: #64748b;
    font-weight: 500;
  }
  .stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
  }
  .performance-highlight {
    background: linear-gradient(135deg, #063478, #059669);
    color: white;
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
  }
  .win-ratio-value {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    display: block;
  }
  .win-ratio-label {
    font-size: 1.25rem;
    opacity: 0.9;
  }
  .match-breakdown {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  .match-stat {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
  }
  .match-number {
    font-size: 1.5rem;
    font-weight: 700;
    display: block;
  }
  .match-label {
    font-size: 0.875rem;
    opacity: 0.8;
    margin-top: 0.25rem;
  }
  .total-matches {
    margin-top: 1rem;
    font-size: 1.1rem;
  }
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }
    .player-name {
      font-size: 2rem;
    }
    .rank-badge {
      font-size: 1.5rem;
      padding: 0.75rem 1.5rem;
    }
    .stats-section {
      grid-template-columns: 1fr;
    }
    .player-card {
      padding: 2rem;
    }
  }
</style>
