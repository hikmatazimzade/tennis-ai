<script>
  import { goto } from "$app/navigation";

  function navigateToPlayer(playerId) {
    goto(`/player_statistics/${playerId}`);
  }
</script>

<main>
  <div class="container">
    <div class="header">
      <h1>Tennis Player Search</h1>
      <p>Find and explore professional tennis player statistics</p>
    </div>
    <div class="search-section">
      <div class="search-container">
        <div class="search-icon">🔍</div>
        <input
          type="text"
          placeholder="Search players by name, country, or ranking..."
          class="search-input"
        />
      </div>
    </div>
    <div class="players-grid">
      <!-- Player Card 1 -->
      <div class="player-card" on:click={() => navigateToPlayer(1)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Novak Djokovic</h3>
            <div class="player-country">🇷🇸 SRB</div>
          </div>
          <div class="rank-badge">#1</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">82.5%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2435</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">9,945</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">36 years</span>
          <span class="matches">1,289 matches</span>
        </div>
      </div>
      <!-- Player Card 2 -->
      <div class="player-card" on:click={() => navigateToPlayer(2)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Carlos Alcaraz</h3>
            <div class="player-country">🇪🇸 ESP</div>
          </div>
          <div class="rank-badge">#2</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">82.1%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2401</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">8,855</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">21 years</span>
          <span class="matches">246 matches</span>
        </div>
      </div>
      <!-- Player Card 3 -->
      <div class="player-card" on:click={() => navigateToPlayer(3)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Jannik Sinner</h3>
            <div class="player-country">🇮🇹 ITA</div>
          </div>
          <div class="rank-badge">#3</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">83.7%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2367</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">8,270</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">23 years</span>
          <span class="matches">312 matches</span>
        </div>
      </div>
      <!-- Player Card 4 -->
      <div class="player-card" on:click={() => navigateToPlayer(4)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Daniil Medvedev</h3>
            <div class="player-country">🇷🇺 RUS</div>
          </div>
          <div class="rank-badge">#4</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">77.6%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2298</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">7,555</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">28 years</span>
          <span class="matches">478 matches</span>
        </div>
      </div>
      <!-- Player Card 5 -->
      <div class="player-card" on:click={() => navigateToPlayer(5)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Rafael Nadal</h3>
            <div class="player-country">🇪🇸 ESP</div>
          </div>
          <div class="rank-badge">#154</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">82.6%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2145</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">380</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">38 years</span>
          <span class="matches">1,308 matches</span>
        </div>
      </div>
      <!-- Player Card 6 -->
      <div class="player-card" on:click={() => navigateToPlayer(6)}>
        <div class="card-header">
          <div class="player-info">
            <h3 class="player-name">Coco Gauff</h3>
            <div class="player-country">🇺🇸 USA</div>
          </div>
          <div class="rank-badge">#3</div>
        </div>
        <div class="stats-preview">
          <div class="stat">
            <span class="stat-value">75.1%</span>
            <span class="stat-label">Win Rate</span>
          </div>
          <div class="stat">
            <span class="stat-value">2201</span>
            <span class="stat-label">ELO</span>
          </div>
          <div class="stat">
            <span class="stat-value">5,230</span>
            <span class="stat-label">Points</span>
          </div>
        </div>
        <div class="additional-info">
          <span class="age">20 years</span>
          <span class="matches">189 matches</span>
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
  .search-section {
    margin-bottom: 3rem;
    display: flex;
    justify-content: center;
  }
  .search-container {
    position: relative;
    width: 100%;
    max-width: 600px;
  }
  .search-icon {
    position: absolute;
    left: 1.25rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.25rem;
    color: #64748b;
    z-index: 1;
  }
  .search-input {
    width: 100%;
    padding: 1.25rem 1.25rem 1.25rem 3.5rem;
    border: none;
    border-radius: 20px;
    font-size: 1.1rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 2px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    outline: none;
  }
  .search-input:focus {
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border-color: #182768;
    transform: translateY(-2px);
  }
  .search-input::placeholder {
    color: #94a3b8;
  }
  .players-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: 2rem;
  }
  .player-card {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
  }
  .player-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #182768, #764ba2);
  }
  .player-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
    border-color: rgba(24, 39, 104, 0.3);
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.5rem;
  }
  .player-info {
    flex: 1;
  }
  .player-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: #2d3748;
    margin: 0 0 0.5rem 0;
  }
  .player-country {
    display: inline-flex;
    align-items: center;
    background: #f7fafc;
    color: #4a5568;
    padding: 0.375rem 0.875rem;
    border-radius: 12px;
    font-size: 0.875rem;
    font-weight: 600;
    border: 1px solid #e2e8f0;
  }
  .rank-badge {
    background: linear-gradient(135deg, #182768, #5c4572);
    color: white;
    padding: 0.75rem 1rem;
    border-radius: 16px;
    font-weight: 700;
    font-size: 1.25rem;
    text-align: center;
    min-width: 60px;
    flex-shrink: 0;
  }
  .stats-preview {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .stat {
    text-align: center;
    background: #f8fafc;
    border-radius: 12px;
    padding: 1rem 0.75rem;
    border: 1px solid #e2e8f0;
  }
  .stat-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: #182768;
    display: block;
    margin-bottom: 0.25rem;
  }
  .stat-label {
    font-size: 0.75rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .additional-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
    font-size: 0.875rem;
    color: #64748b;
  }
  .age,
  .matches {
    font-weight: 500;
  }
  @media (max-width: 768px) {
    .container {
      padding: 1rem;
    }
    .header h1 {
      font-size: 2rem;
    }
    .players-grid {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    .player-card {
      padding: 1.5rem;
    }
    .stats-preview {
      grid-template-columns: repeat(3, 1fr);
      gap: 0.75rem;
    }
    .stat {
      padding: 0.75rem 0.5rem;
    }
    .stat-value {
      font-size: 1rem;
    }
    .stat-label {
      font-size: 0.7rem;
    }
  }
  @media (max-width: 480px) {
    .card-header {
      flex-direction: column;
      gap: 1rem;
      align-items: stretch;
    }
    .rank-badge {
      align-self: flex-end;
      width: fit-content;
    }
  }
</style>
