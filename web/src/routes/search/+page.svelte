<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";
    import Page from "$lib/components/Page.svelte";
    import Embed from "$lib/components/Embed.svelte";
  
    import { onMount } from "svelte";
    import { toaster } from "$lib/scripts/Toaster";
    import { API_URL } from "$lib/Config";  

    import type { Package } from "$lib/types/Package";
  import { emptyArr } from "$lib/scripts/Utils";

    let search: string = $state("");

    let results: {results: Package[], pageCount: number, resultCount: number} = $state({
        results: [],
        pageCount: 0,
        resultCount: 0
    });
    let loading: boolean = $state(true);
    let error: boolean = $state(false);

    onMount(async () => {
        const params = new URLSearchParams(window.location.search);
        if (!params.has("q")) {
            window.location.href = "/"
            return
        }

        const query = params.get("q") as string
        let page = params.has("page") ? parseInt(params.get("page") as string) : 1
        search = query;

        if (isNaN(page)) { page = 1; }

        const r = await fetch(`${API_URL}/package/search?query=${encodeURIComponent(query)}&page=${encodeURIComponent(page)}`)
        if (!r.ok) {
            toaster.error({title: "Unable to load results", description: r.statusText})
            error = true
            return
        }

        results = await r.json();
        setTimeout(() => {loading = false}, 500)
        // console.log(results)
    })
</script>

<Embed title = "Search | Nautica PR" />

<Navbar />
<Page className="mt-32">
    <div class="flex max-md:hidden">    
        <input type="text" class="input w-full" placeholder="Search for packages" bind:value={search} onkeypress={(e) => {
            if (!search) { return; }
            if (e.key == "Enter") { window.location.href = `/search?q=${encodeURIComponent(search)}`; }
        }}>
        
        <a href="/search?q={encodeURIComponent(search)}">
            <button class="btn preset-filled-primary-500 ">
                <span class="material-symbols-sharp">search</span>
            </button>
        </a>
    </div>

    {#if error}
        <div class="flex items-center flex-col mt-16">

            <p class="text-error-500 italic">Unable to load results</p>
            <div class="flex gap-3">
                <a href="{window.location.href}" class="underline">Retry?</a>
                <p>•</p>
                <a href="/" class="underline">Go home</a>
            </div>

        </div>
    {/if}

    {#if !loading}
        <div class="flex flex-col gap-5 mt-16">
            {#each results.results as p}
                <a href="/packages/{p.name}">
                    <div class="card preset-filled-surface-100-900 p-3">
                        <p class="font-semibold text-lg mr-2">{p.displayName}</p>
                        
                        <p class="italic text-surface-800-200">{p.brief || "No description"}</p>
                    </div>
                </a>
            {/each}
        </div>
    {:else}
        <div class="flex flex-col gap-5 mt-16">
            {#each emptyArr(3) as _}
                <div class="card preset-filled-surface-100-900 p-3 animate-shimmer select-none">
                    <p class="font-semibold text-lg mr-2 opacity-0">_</p>
                        
                    <p class="italic text-surface-800-200 opacity-0">_</p>
                </div>
            {/each}
        </div>
    {/if}

</Page>