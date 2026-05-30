<script lang="ts">
    import Embed from "$lib/components/Embed.svelte";
    import Page from "$lib/components/Page.svelte";
    import Navbar from "$lib/components/Navbar.svelte";
</script>

<svelte:head>
    <Embed
        title = "Nautica Package Registry"
    />
</svelte:head>

<Navbar />
<Page className="mt-32">
    <input type="text" class="input" placeholder="Search for packages">
</Page>