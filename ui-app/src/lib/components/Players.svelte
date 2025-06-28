<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  import { BACKEND_BASE_URL } from "../index";

  function navigateToPlayer(playerId) {
    goto(`/players/${playerId}`);
  }
  console.log(BACKEND_BASE_URL);

  let currentPlayers = [];
  let paginatedPlayers = [];
  let allPlayers = [];
  let searchText = "";

  $: pageNumber = 1;
  let totalPages = 0;

  async function fetchAllPlayers() {
    try {
      const response = await fetch(`${BACKEND_BASE_URL}/players?page=-1`);
      if (!response.ok) {
        throw new Error(`HTTP Error Status!: ${response.status}`);
      }
      allPlayers = await response.json();
    } catch (err) {
      let errorMessage = err.message;
      console.log(`Error Message: ${errorMessage}`);
    }
  }

  async function fetchPlayers() {
    try {
      const response = await fetch(
        `${BACKEND_BASE_URL}/players?page=${pageNumber}`
      );
      if (!response.ok) {
        throw new Error(`HTTP Error Status!: ${response.status}`);
      }
      let playersData = await response.json();
      paginatedPlayers = playersData.data;
      currentPlayers = paginatedPlayers;
      totalPages = playersData.total_page_number;
    } catch (err) {
      let errorMessage = err.message;
      console.log(`Error Message: ${errorMessage}`);
    }
  }

  function searchPlayers() {
    if (searchText === "") {
      currentPlayers = paginatedPlayers;
    } else {
      currentPlayers = allPlayers.filter(
        (player) =>
          player.name.toLowerCase().includes(searchText.toLowerCase()) ||
          player.ioc.toLowerCase().includes(searchText.toLowerCase())
      );
    }
    console.log(searchText);
  }

  function changePage(newPage) {
    if (newPage >= 1 && newPage <= totalPages) {
      pageNumber = newPage;
      fetchPlayers();
    }
  }

  onMount(() => {
    fetchPlayers();
    fetchAllPlayers();
  });

  $: console.log(paginatedPlayers);
  $: console.log(totalPages);
  $: console.log(allPlayers);
</script>

<main>
  <nav class="top-nav">
    <a href="/prediction" class="nav-link">
      <svg
        class="nav-icon"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <circle cx="12" cy="12" r="10"></circle>
        <circle cx="12" cy="12" r="6"></circle>
        <circle cx="12" cy="12" r="2"></circle>
      </svg>
      <span class="nav-text">Prediction</span>
    </a>
  </nav>

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
          placeholder="Search players by name or country"
          class="search-input"
          bind:value={searchText}
          on:input={searchPlayers}
        />
      </div>
    </div>
    <div class="players-grid">
      {#each currentPlayers as player}
        <div class="player-card" on:click={() => navigateToPlayer(player.id)}>
          <div class="card-header">
            <div class="player-info">
              <h3 class="player-name">{player.name}</h3>
              <div class="player-country">{player.ioc}</div>
            </div>
            <div class="rank-badge">#{player.rank}</div>
          </div>
          <div class="stats-preview">
            <div class="stat">
              <span class="stat-value">{player.win_rate}%</span>
              <span class="stat-label">Win Rate</span>
            </div>
            <div class="stat">
              <span class="stat-value">{player.elo}</span>
              <span class="stat-label">ELO</span>
            </div>
            <div class="stat">
              <span class="stat-value">{player.rank_points}</span>
              <span class="stat-label">Points</span>
            </div>
          </div>
          <div class="additional-info">
            <span class="age">{player.age} years</span>
            <span class="matches">{player.total_match} matches</span>
          </div>
        </div>
      {/each}
    </div>

    {#if searchText === ""}
      <div class="pagination">
        <button
          class="page-btn"
          on:click={() => changePage(pageNumber - 1)}
          disabled={pageNumber === 1}
        >
          ‹
        </button>

        {#each Array(Math.min(5, totalPages)) as _, i}
          {@const page =
            Math.max(1, Math.min(totalPages - 4, pageNumber - 2)) + i}
          {#if page <= totalPages}
            <button
              class="page-btn"
              class:active={page === pageNumber}
              on:click={() => changePage(page)}
            >
              {page}
            </button>
          {/if}
        {/each}

        <button
          class="page-btn"
          on:click={() => changePage(pageNumber + 1)}
          disabled={pageNumber === totalPages}
        >
          ›
        </button>
      </div>
    {/if}
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
    padding-top: 3rem;
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
    margin-bottom: 3rem;
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
  .pagination {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    align-items: center;
  }
  .page-btn {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #182768;
    padding: 0.75rem 1rem;
    border-radius: 12px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
  }
  .page-btn:hover:not(:disabled) {
    background: #182768;
    color: white;
    transform: translateY(-2px);
  }
  .page-btn.active {
    background: #182768;
    color: white;
  }
  .page-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
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

  .top-nav {
    position: fixed;
    top: 2rem;
    right: 2rem;
    z-index: 1000;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #182768;
    text-decoration: none;
    padding: 0.75rem 1.25rem;
    border-radius: 50px;
    font-size: 0.875rem;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
  }

  .nav-link::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(24, 39, 104, 0.1),
      transparent
    );
    transition: left 0.6s ease;
  }

  .nav-link:hover::before {
    left: 100%;
  }

  .nav-link:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(24, 39, 104, 0.2);
    color: #764ba2;
  }

  .nav-icon {
    width: 18px;
    height: 18px;
    transition: transform 0.3s ease;
  }

  .nav-link:hover .nav-icon {
    transform: scale(1.1);
  }

  .nav-text {
    position: relative;
    z-index: 1;
  }

  .container {
    padding-top: 3rem;
  }

  @media (max-width: 768px) {
    .top-nav {
      top: 1rem;
      right: 1rem;
    }

    .nav-link {
      padding: 0.625rem 1rem;
      font-size: 0.8rem;
    }

    .nav-icon {
      width: 16px;
      height: 16px;
    }

    .container {
      padding-top: 4rem;
    }
  }

  @media (max-width: 480px) {
    .top-nav {
      position: relative;
      top: auto;
      right: auto;
      margin-bottom: 1rem;
      display: flex;
      justify-content: center;
    }

    .container {
      padding-top: 1rem;
    }
  }
</style>
