<script>
  import { page } from "$app/stores";
  import { playerNames } from "$lib/index";
  import PlayerStatisticsId from "$lib/components/PlayerStatisticsId.svelte";

  let playerId = $page.params.id;
</script>

<main>
  <PlayerStatisticsId {playerId} {playerNames} />
</main>
