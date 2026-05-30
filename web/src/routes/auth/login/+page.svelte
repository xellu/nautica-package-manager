<script lang="ts">
    import Navbar from "$lib/components/Navbar.svelte";
    import Page from "$lib/components/Page.svelte";
</script>

<Navbar />
<Page className="my-16">
    <a href="/" class="font-mono">{'<--'} Home</a>

    <div class="mt-8 card preset-filled-surface-100-900 w-full p-3">
        <h1 class="h6">Log In</h1>

        <div class="flex gap-3 mt-5">
            <div class="w-1/2">
                <form class="flex flex-col gap-3">
                    <label>
                        <span class="text-xs uppercase font-bold">Username</span>
                        <input type="text" class="input" placeholder="Your Username">
                    </label>
                    
                    <label>
                        <span class="text-xs uppercase font-bold">Password</span>
                        <input type="password" class="input" placeholder="Your Password">
                    </label>

                    <div class="flex justify-end">    
                        <button class="btn preset-filled-primary-500 mt-3 w-44">Continue</button>
                    </div>
                    
                </form>
            </div>

            <div class="w-1/2">
                <p>hello world</p>
            </div>
        </div>
    </div>
</Page>
