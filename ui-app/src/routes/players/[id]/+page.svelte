<script>
  import { page } from "$app/stores";
  import Player from "$lib/components/Player.svelte";

  let playerId = $page.params.id;
</script>

<main>
  <Player {playerId} />
</main>
