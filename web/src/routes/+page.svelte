<script lang="ts">
    import Embed from "$lib/components/Embed.svelte";
    import Page from "$lib/components/Page.svelte";
    import Navbar from "$lib/components/Navbar.svelte";
</script>

<svelte:head>
    <Embed
        title = "Nautica Package Registry"
        description = "The official package registry for Nautica. Discover, publish and install services for your Nautica projects."
    />
</svelte:head>

<Navbar />
<Page className="mt-32">
    <input type="text" class="input" placeholder="Search for packages">
</Page>