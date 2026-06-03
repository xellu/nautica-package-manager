<script lang="ts">
    import Navbar from '$lib/components/Navbar.svelte';
    import Page from '$lib/components/Page.svelte';
    import Markdown from '$lib/components/Markdown.svelte';
    
    import { API_URL } from '$lib/Config.js';
    import { scale } from 'svelte/transition';

    import type { Package } from '$lib/types/Package.js';
    import { toDate } from '$lib/scripts/Utils.js';
  
    let { data } = $props();
    let p: Package = $derived(data.package);

    let copied: boolean = $state(false);
</script>

<Navbar />
<Page className="flex mt-16 gap-16 items-start">
    <!-- about package -->
    <div class="card preset-outlined-surface-100-900 p-3 w-72">
        <!-- package hero -->
        <div class="flex gap-3 items-center">
            <span class="material-symbols-sharp">package_2</span>
            <p class="font-semibold text-xl text-ellipsis overflow-hidden">{p.displayName}</p>

            <span class="chip font-semibold preset-filled">v{p.versions[0].id}</span>
            <span class="chip font-semibold preset-filled-primary-500 -ml-3">Latest</span>
        </div>
        <p class="p-0.5 text-sm text-surface-700-300">Published by <span>@{p.ownerExpanded?.username || '(INACCESSIBLE)'}</span></p>

        <!-- description -->
        <div class="flex w-full mt-3">
            <span class="card preset-filled-surface-100-900 p-1 px-3 border border-surface-200-800/50 font-mono grow text-sm">napi install {p.name}</span>
            <button class="btn {copied ? 'preset-filled-primary-500' : 'bg-surface-200-800/70'} w-16"
                onclick={() => {
                    navigator.clipboard.writeText(`napi install ${p.name}`)
                    copied = true;
                    setTimeout(() => { copied = false }, 1000);
                }}
                title = "Copy Command"
            >
                {#if copied} <span class="material-symbols-sharp" in:scale>check</span>
                {:else} <span in:scale>Copy</span>
                {/if}
            </button>
        </div>
        <p class="mt-5 mb-10 italic">{p.brief || 'No description provided'}</p>

        <h3 class="uppercase font-bold text-sm text-surface-700-300">Maintainers</h3>
        <div class="flex flex-col">
            <p>@{p.ownerExpanded?.username} <span class="chip py-0 preset-filled font-semibold">Owner</span> </p>
            {#each (p.maintainersExpanded || []) as maintainer}
                <p>@{maintainer.username}</p>
            {/each}
        </div>

        <!-- releases -->
        <h3 class="uppercase font-bold text-sm text-surface-700-300 mt-10">Versions</h3>
        <div class="flex flex-col gap-1">
            {#each p.versions.reverse() as ver, i}
                <a href="/packages/{p.name}{i == 0 ? '' : `/${ver.id}`}" title="{ver.id}">
                    <button class="btn w-full font-mono {i == 0 ? 'preset-filled-surface-100-900' : 'hover:preset-filled-surface-100-900'}">
                        <div class="w-full flex items-center justify-between">
                            <span class="font-semibold">v{ver.id}</span>
                            <span class="text-sm italic">{toDate(new Date(ver.createdAt*1000))}</span>
                        </div>
                    </button>
                </a>
            {/each}
        </div>

    </div>

    <!-- readme -->
    <div class="pb-16 grow">
        <Markdown content={p.readMe || "No content"} />
    </div>
</Page>