<script>
  import { page } from "$app/stores";
  import { playerNames } from "$lib/index";
  import Player from "$lib/components/Player.svelte";

  let playerId = $page.params.id;
</script>

<main>
  <Player {playerId} {playerNames} />
</main>
