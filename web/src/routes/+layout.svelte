<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/Favicon.svg';

	import { Toast } from '@skeletonlabs/skeleton-svelte';
	import { onMount } from 'svelte';

	import { toaster } from '$lib/scripts/Toaster';
	import { AutoAuthenticate } from '$lib/scripts/Auth';


	let { children } = $props();

	onMount(async () => {
		let auth = await AutoAuthenticate();

		auth.state.loggedIn 
		? console.info(`Authenticated (${auth.state.auto})`) 
		: auth.state.error 
			? console.warn(`Auth error: ${auth.state.error}`)
			: console.warn("Not logged in")

        if (auth.state.error && !auth.state.loggedIn) { //show error message
			toaster.error({
				title: "Authentication Error",
				description: auth.state.error
			})
        }
	})

	const ICONS: string[] = [
		"search",
		"package_2",
		"check",
		
	].toSorted();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link
        rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names={ICONS}"
    />
</svelte:head>


<Toast.Group {toaster}>
	{#snippet children(toast)}
		<div class="w-full flex justify-end">	
		<Toast toast={toast}>
				<Toast.Message>
				<Toast.Title>{toast.title}</Toast.Title>
				<Toast.Description>{toast.description}</Toast.Description>
				</Toast.Message>
				<Toast.CloseTrigger />
			</Toast>
		</div>
	{/snippet}
</Toast.Group>


{@render children()}
