<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";

    import { Account, LogOut, AuthState, type AuthStateType } from "$lib/scripts/Auth";
    import { type Profile } from "$lib/types/User";

    let User: Profile | null = $state(null);
    let State: AuthStateType = $state({loading: true, loggedIn: false});
    Account.subscribe((value) => { User = value })
    AuthState.subscribe((value) => {
        if (!value.loading && !value.loggedIn) {
            window.location.href = "/auth/login"
        }
        State = value;
    })

    import { onMount } from "svelte";
    import { goto } from "$app/navigation";
  
    let { children } = $props();

    let url: string = $state("");
    onMount(() => {
        url = window.location.pathname;
    })

    let pages = [
        ["My Packages", "/dashboard"],
        ["My Account", "/dashboard/account"]
    ]

    function openPage(pageUrl: string) {
        url = pageUrl;
        goto(pageUrl);
    }
</script>

<Navbar className="fixed" />

<div class="flex w-screen h-screen">
    <div class="bg-surface-100-900/50 h-screen w-2/5 flex flex-col items-end justify-between p-3 pt-20">
        <div class="flex flex-col gap-1 w-64">
            
            {#each pages as p}
                <button onclick={() => { openPage(p[1]) }} class="btn {p[1] === url ? ' preset-filled-surface-200-800' : ' preset-tonal'}">
                    {p[0]}

                    <!-- <p>{p[1]} == {url}?</p> -->
                </button>
            {/each}

        </div>

        <div class="flex flex-col w-64">
            <div><span class="bg-error-500 p-0.5 px-2 text-surface-100-900">Logged in as {User?.username}</span></div>
            <button class="btn preset-outlined-error-500" onclick={() => { LogOut().then(() => {window.location.href = "/"}); }}>
                Sign Out
            </button>
        </div>
    </div>
    <div class="p-3 w-3/5 overflow-y-scroll pt-20">
        {#if State.loading}
            <div class="w-full h-full flex items-center justify-center">    
                <img src="/icon.svg" alt="" class="w-32 animate-spin">
            </div>
        {:else}
            {@render children()}
        {/if}
    </div>
</div>