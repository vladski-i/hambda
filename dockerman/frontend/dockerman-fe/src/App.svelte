<script>
	import {onMount} from 'svelte';
	import { default as Containers } from './Containers.svelte'
	// import { default as Editor} from './Editor.svelte'
	import {default as NewContainer} from './NewContainer.svelte';

	let menu = 'Containers'
</script>

<main>
	<h1><b>Lchp</b></h1>
	<ul id = 'menu'>
		<li><a href='/' on:click|preventDefault={() => (menu = 'Containers')}>Containers</a></li>
		<li><a href='/' on:click|preventDefault={() => (menu = 'New Container')}>New Container</a></li>
	</ul>
	
	{#if menu == 'Containers'}
	<Containers/>
	{:else if menu == 'New Container'}
	<NewContainer/>
	{:else}
		Not found
	{/if}
</main>

<style>
	main {
		text-align: left;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
		margin-left:1rem;
	}

	h1 {
		color: #ba000d;
		text-transform: uppercase;
		font-size: 2em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
	ul#menu li{
		display : inline;
	}

</style>