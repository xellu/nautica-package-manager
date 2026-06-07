<script lang="ts">
    import Page from "./Page.svelte";
    import { slide } from "svelte/transition";

    import { AuthState, type AuthStateType } from "$lib/scripts/Auth";

    let { className = "" } = $props();

    let State: AuthStateType = $state({loading: true, loggedIn: false})
    AuthState.subscribe((value) => { State = value; })

    let search: string = $state("");
</script>


<div class=" bg-surface-100-900 p-3 w-full z-50 {className}">
    <Page className="flex items-center justify-between">
        <!-- branding -->
        <a href="/" class="flex gap-3">
            <img src="/icon.svg" alt="" class="w-10 {State.loading ? 'animate-pulse' : ''}" draggable="false">
            <div class="text-tertiary-500">
                <img src="/text.svg" alt="Nautica" class="h-4 mt-1">
                <p class="text-xs">Package Registry</p>
            </div>
        </a>

        <div class="flex max-md:hidden">    
            <input type="text" class="input max-w-64" placeholder="Search for packages" bind:value={search}  onkeypress={(e) => {
                if (!search) { return; }
                if (e.key == "Enter") { window.location.href = `/search?q=${encodeURIComponent(search)}`; }
            }}>

            <a href="/search?q={encodeURIComponent(search)}">
                <button class="btn preset-filled-primary-500 ">
                    <span class="material-symbols-sharp">search</span>
                </button>
            </a>
        </div>

        <!-- links -->
        {#if !State.loading}

            {#if State.loggedIn}
            <a href="/dashboard" class="btn preset-filled-tertiary-500 max-sm:btn-sm" transition:slide={{axis: "y"}}>Dashboard</a>
            {:else}
            <div class="flex gap-3" transition:slide={{axis: "y"}}>
                <a href="/auth/register" class="btn hover:underline max-sm:hidden">Register</a>
                <a href="/auth/login" class="btn preset-filled-tertiary-500">Log In</a>
            </div>
            {/if}

        {:else}
            <div class="opacity-0">.</div>
        {/if}
    </Page>
</div>
