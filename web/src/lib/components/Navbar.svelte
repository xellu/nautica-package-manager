<svelte:options runes={false} />

<script lang="ts">
    import Page from "./Page.svelte";
</script>


<div class=" bg-surface-100-900 p-3 w-full">
    <Page className="flex items-center justify-between">
        <!-- branding -->
        <a href="/" class="flex gap-3">
            <img src="/icon.svg" alt="" class="w-10" draggable="false">
            <div class="text-tertiary-500">
                <p class="text-xl font-bold">Nautica</p>
                <p class="text-xs -mt-1">Package Registry</p>
            </div>
        </a>

        <!-- links -->
        <div class="flex gap-3">
            <a href="/auth/register" class="btn hover:underline">Register</a>
            <a href="/auth/login" class="btn preset-filled-tertiary-500">Log In</a>
        </div>
    </Page>
</div>
