<script lang="ts">
    import Embed from "$lib/components/Embed.svelte";
    import Page from "$lib/components/Page.svelte";
    import Navbar from "$lib/components/Navbar.svelte";

    import { API_URL } from "$lib/Config";

    import type { Package } from "$lib/types/Package";
    import { temp } from "$lib/scripts/Temp";
    import { toaster } from "$lib/scripts/Toaster";
    import { emptyArr } from "$lib/scripts/Utils";
    
    import { onMount } from "svelte";


    let search: string = $state("");
    let featured: Package[] = $state([]);

    onMount(async () => {
        const cached = temp.get("home.featured")
        // console.log(cached)

        if (cached != null) {
            featured = cached;
            return
        }

        let r;
        try {
            r = await fetch(`${API_URL}/package/featured`)
            if (!r.ok) {
                const data = await r.json()
                toaster.error({description: data.error || "Unknown Error"})
                return
            }
        } catch(e) {
            toaster.error({description: `${e}`})
            return
        }

        featured = await r.json();
        temp.set("home.featured", featured, 3*60*1000)
    })
</script>

<svelte:head>
    <Embed
        title = "Nautica Package Registry"
        description = "The official package registry for Nautica. Discover, publish and install services for your Nautica projects."
    />
</svelte:head>

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

    <h3 class="h3 mt-16 mb-5">Popular Packages</h3>

    {#if featured}
    <div class="grid grid-cols-5 gap-5">
        {#each featured as p}
            <a href="/packages/{p.name}">
                <div class="card preset-filled-surface-100-900 p-3 h-72 overflow-y-hidden group">
                    <div class="flex items-center justify-between gap-3">
                        <div class="flex gap-3 items-center group-hover:text-secondary-500 duration-300">
                            <span class="material-symbols-sharp">package_2</span>
                            <p class="font-semibold text-xl text-ellipsis overflow-hidden">{p.displayName}</p>
                        </div>

                        <span class="chip font-semibold preset-filled-tertiary-500 group-hover:preset-filled-secondary-500">v{p.versions[p.versions.length-1].id}</span>
                    </div>
                    <p class="text-surface-800-200 text-sm mb-3 italic">
                        {p.installs} Downloads • {p.versions.length} Releases
                    </p>
                    <p class="text-surface-900-100">{p.brief || 'No description'}</p>
                </div>
            </a>
        {/each}
    </div>
    {:else}
        <div class="grid grid-cols-5 gap-5 animate-pulse">
        {#each emptyArr(10) as p}
            <div class="card preset-filled-surface-100-900 p-3 h-72 animate-shimmer"></div>

        {/each}
        </div>
    {/if}
</Page>