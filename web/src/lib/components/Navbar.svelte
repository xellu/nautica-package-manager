<script lang="ts">
    import Page from "./Page.svelte";
    import { slide } from "svelte/transition";

    import { AuthState, type AuthStateType } from "$lib/scripts/Auth";

    let State: AuthStateType = $state({loading: true, loggedIn: false})
    AuthState.subscribe((value) => { State = value; })
</script>


<div class=" bg-surface-100-900 p-3 w-full">
    <Page className="flex items-center justify-between">
        <!-- branding -->
        <a href="/" class="flex gap-3">
            <img src="/icon.svg" alt="" class="w-10 {State.loading ? 'animate-pulse' : ''}" draggable="false">
            <div class="text-tertiary-500">
                <img src="/text.svg" alt="Nautica" class="h-4 mt-1">
                <p class="text-xs">Package Registry</p>
            </div>
        </a>

        <!-- links -->
        {#if !State.loading}

            {#if State.loggedIn}
            <a href="/dashboard" class="btn preset-filled-tertiary-500" transition:slide={{axis: "y"}}>Dashboard</a>
            {:else}
            <div class="flex gap-3" transition:slide={{axis: "y"}}>
                <a href="/auth/register" class="btn hover:underline">Register</a>
                <a href="/auth/login" class="btn preset-filled-tertiary-500">Log In</a>
            </div>
            {/if}

        {/if}
    </Page>
</div>
