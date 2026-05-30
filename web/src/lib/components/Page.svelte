<svelte:options runes={false} />

<script lang="ts">
    export let debug: boolean = false;
    export let className: string = "";
</script>


<h1 class="opacity-0 absolute -top-96">Nautica Package Registry</h1>

<div class="w-full flex justify-center">
    <div class="max-w-6xl w-full {debug ? 'border' : ''} {className}">
        <slot></slot>  
    </div>
</div>