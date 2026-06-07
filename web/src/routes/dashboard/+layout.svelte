<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";
    import Page from "$lib/components/Page.svelte";

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
        // ["My Account", "/dashboard/account"]
    ]

    function openPage(pageUrl: string) {
        url = pageUrl;
        goto(pageUrl);
    }

    let navOpen: boolean = $state(false);
</script>

<Navbar className="fixed max-md:hidden" />

<div class=" bg-surface-100-900 p-3 w-full z-50 fixed">
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
        <button onclick={() => { navOpen = !navOpen}}>
            <span class="material-symbols-sharp">menu</span>
        </button>
    </Page>
</div>

<div class="flex w-screen h-screen justify-end">
    <div
        class="bg-surface-100-900/50 backdrop-blur-2xl md:bg-surface-100-900/50 h-screen flex flex-col items-end justify-between p-3 pt-20 max-xl:pt-28
                max-md:fixed md:w-2/5 z-20 max-md:h-screen {navOpen ? 'top-0 w-full' : '-top-full w-0 overflow-hidden'} duration-300"
    >
        <div class="flex flex-col gap-1 md:w-64 w-full">
            
            {#each pages as p}
                <button onclick={() => { openPage(p[1]) }} class="btn {p[1] === url ? 'preset-tonal md:preset-filled-surface-200-800' : ' md:preset-tonal'} max-md:text-lg">
                    {p[0]}
                </button>
            {/each}

        </div>

        <div class="flex flex-col md:w-64 w-full">
            <div><span class="bg-error-500 p-0.5 px-2 text-surface-100-900">Logged in as {User?.username}</span></div>
            <button class="btn preset-outlined-error-500" onclick={() => { LogOut().then(() => {window.location.href = "/"}); }}>
                Sign Out
            </button>
        </div>
    </div>
    <div class="p-3 w-full md:w-3/5 overflow-y-scroll pt-20 max-xl:pt-28">
        {#if State.loading}
            <div class="w-full h-full flex items-center justify-center">    
                <img src="/icon.svg" alt="" class="w-32 animate-spin">
            </div>

            <!-- <p>{State.loading}, {State.loggedIn}</p> -->
        {:else}
            {@render children()}
        {/if}
    </div>
</div>