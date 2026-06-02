<script lang="ts">
    import { toaster } from "$lib/scripts/Toaster";

    import type { Package } from "$lib/types/Package";
    import { onMount } from "svelte";

    import { Account, type AccountType } from "$lib/scripts/Auth.js";

    let User: AccountType | null = $state(null);
    Account.subscribe((value) => { User = value })

    let { data } = $props();
    let packages: Package[] = $derived(
        [...data.packages].sort((a, b) => {
            const latestA = Math.max(...a.versions.map(v => v.createdAt), 0);
            const latestB = Math.max(...b.versions.map(v => v.createdAt), 0);
            return latestB - latestA;
        })
    );
    let error: any = $derived(data.error);

    onMount(async () => {
        if (error != null) {
            toaster.error({description: error})
        }

        // console.log(packages)
    })
</script>

<div class="flex flex-col gap-5">
    {#each packages as p}
        <div class="card preset-filled-surface-100-900 p-3">
            <div class="flex justify-between">
                <div class="flex items-center gap-1">
                    <p class="font-semibold text-lg mr-2">{p.displayName}</p>
                    <span class="chip font-semibold preset-filled">v{p.versions[p.versions.length-1].id}</span>
                    <span class="chip font-semibold {p.owner == User?.userId ? 'preset-filled-secondary-500' : 'preset-filled-tertiary-500'}">{p.owner == User?.userId ? 'Owner' : 'Maintainer'}</span>
                </div>

                
                <div class="flex items-center">
                    <a href="/packages/{p.name}"><button class="btn preset-outlined-primary-500 py-1">View</button></a>
                    <a href="/packages/{p.name}/edit"><button class="btn preset-filled-primary-500 py-1.25">Edit</button></a>
                </div>

            </div>
            <p class="mt-1 mb-5 text-xs opacity-75 font-mono">{p.versions.length} releases • {p.maintainers.length+1} maintainers</p>

            {#if p.brief}
                <p class="italic text-surface-800-200">{p.brief}</p>
            {:else}
                <a href="/packages/{p.name}/edit" class="font-mono underline">Add a description to help others find your package {'->'}</a>
            {/if}

        </div>
    {/each}
</div>
