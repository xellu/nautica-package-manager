<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";

    import { page } from "$app/state";
</script>

<Navbar className="fixed" />

<div class="w-full h-screen flex items-center justify-center flex-col gap-5">
    <h2 class="h1 text-9xl text-warning-500">{page.status}</h2>
    <p class="uppercase font-bold text-sm">{page.error?.message}</p>
</div>