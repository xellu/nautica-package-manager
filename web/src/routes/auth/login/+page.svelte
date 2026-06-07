<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";
    import Page from "$lib/components/Page.svelte";
    import Embed from "$lib/components/Embed.svelte";

    import { Authenticate, LogIn } from "$lib/scripts/Auth";
    import { toaster } from "$lib/scripts/Toaster";

    let form = $state({
        username: "",
        password: "",
        rememberMe: false
    })

    let blockInput: boolean = $state(false);


</script>

<svelte:head>
    <Embed title = "Sign In | Nautica PR" />
</svelte:head>


<Navbar />
<Page className="my-16">
    <a href="/" class="font-mono">{'<--'} Home</a>

    <div class="mt-8 card preset-filled-surface-100-900 w-full p-3">
        <h1 class="h6">Log In</h1>

        <div class="flex gap-3 mt-5">
            <div class="w-1/2 max-md:w-full">
                <form class="flex flex-col gap-3">
                    <label>
                        <span class="text-xs uppercase font-bold">Username</span>
                        <input type="text" class="input" placeholder="Your Username" bind:value={form.username}>
                    </label>
                    
                    <label>
                        <span class="text-xs uppercase font-bold">Password</span>
                        <input type="password" class="input" placeholder="Your Password" bind:value={form.password}>
                    </label>


                    <label class="flex items-center space-x-2">
                        <input class="checkbox rounded-none" type="checkbox" bind:checked={form.rememberMe} />
                        <p class="select-none">Remember Me</p>
                    </label>

                    <div class="flex justify-between items-end">
                        <a href="/auth/register" class="underline">Don't have an account?</a>    
                        <button
                            class="btn preset-filled-primary-500 mt-3 w-44"
                            disabled={!form.username || !form.password}
                            
                            onclick={async() => {
                                blockInput = true;
                                const r = await LogIn(form.username, form.password, form.rememberMe);
                                
                                if (!r.loggedIn) {
                                    setTimeout(() => { blockInput = false; }, 1000)

                                    toaster.error({
                                        title: "Login Failed",
                                        description: r.error || "Unknown Error"
                                    })
                                } else {
                                    Authenticate().then(() => {
                                        window.location.href = "/dashboard";
                                    });
                                }
                            }}
                        >Continue</button>
                    </div>
                    
                </form>
            </div>

            <div class="w-1/2 flex items-center justify-center gap-3 -mt-6 select-none max-md:hidden">
                <img src="/icon.svg" alt="" class="h-12 {blockInput ? 'animate-spin' : ''}" draggable="false">
                <img src="/text.svg" alt="" class="h-6" draggable="false">
            </div>
        </div>
    </div>
</Page>
