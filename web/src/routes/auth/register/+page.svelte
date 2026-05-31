<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";
    import Page from "$lib/components/Page.svelte";

    import { API_URL } from "$lib/Config";
    import { Authenticate, Register, type AuthStateType } from "$lib/scripts/Auth";
    import { toaster } from "$lib/scripts/Toaster";

    import { AuthState } from "$lib/scripts/Auth";
    import { onMount } from "svelte";

    let form = $state({
        username: "",
        password: "",
        captchaSolution: "",
        rememberMe: false
    })
    let captcha: {image: string | null, id: string} = $state({
        image: null,
        id: ""
    })

    let State: AuthStateType = $state({loading: false, loggedIn: false})
    let blockInput: boolean = $state(false);

    AuthState.subscribe((value) => {
        State = value;
    })

    onMount(async () => {
        //fetch captcha
        blockInput = true
        const r = await fetch(`${API_URL}/auth/captcha`)
        if (!r.ok) {
            let data = await r.json()
            return toaster.error({
                title: "Captcha Error",
                description: data.error || "Unknown Error"
            })
        }

        const blob = await r.blob()

        captcha.id = r.headers.get("n-captcha-id") as string
        console.log(r.headers)
        captcha.image = URL.createObjectURL(blob)

        blockInput = false;
    })

</script>

<Navbar />
<Page className="my-16">
    <a href="/" class="font-mono">{'<--'} Home</a>

    <div class="mt-8 card preset-filled-surface-100-900 w-full p-3">
        <h1 class="h6">Register</h1>

        <div class="flex gap-3 mt-5">
            <div class="w-1/2">
                <form class="flex flex-col gap-3">
                    <label>
                        <span class="text-xs uppercase font-bold">Username</span>
                        <input type="text" class="input" placeholder="Your Username" bind:value={form.username}>
                    </label>
                    
                    <label>
                        <span class="text-xs uppercase font-bold">Password</span>
                        <input type="password" class="input" placeholder="Your Password" bind:value={form.password}>
                    </label>

                    <span class="text-xs uppercase font-bold mt-5">Captcha</span>
                    <div class="flex select-none">
                        <div class="card preset-outlined-surface-200-800 p-2">
                            {#if !captcha.image}
                                <p>Loading captcha</p>
                            {:else}
                                <img src="{captcha.image}" alt="" class="h-16" draggable="false" title="Captcha: {captcha.id}">
                            {/if}
                        </div>
                    </div>

                    <label>
                        <input type="text" class="input" placeholder="Solution" bind:value={form.captchaSolution}>
                    </label>

                    <label class="flex items-center space-x-2">
                        <input class="checkbox rounded-none" type="checkbox" bind:checked={form.rememberMe} />
                        <p class="select-none">Remember Me</p>
                    </label>

                    <div class="flex justify-between items-end">
                        <a href="/auth/login" class="underline">I already have an account</a>    
                        <button
                            class="btn preset-filled-primary-500 mt-3 w-44"
                            disabled={!form.username || !form.password || blockInput}
                            
                            onclick={async() => {
                                const r = await Register(form.username, form.password, form.rememberMe, captcha.id, form.captchaSolution);
                                if (!r.loggedIn) {
                                    toaster.error({
                                        title: "Login Failed",
                                        description: r.error || "Unknown Error"
                                    })
                                }
                                blockInput = true;
                                await Authenticate();
                                setTimeout(() => { blockInput = false}, 1000);
                            }}
                        >Continue</button>
                    </div>
                    
                </form>
            </div>

            <div class="w-1/2 flex items-center justify-center gap-3 -mt-6 select-none">
                <img src="/icon.svg" alt="" class="h-12 {blockInput ? 'animate-spin' : ''}" draggable="false">
                <img src="/text.svg" alt="" class="h-6" draggable="false">
            </div>
        </div>
    </div>
</Page>


