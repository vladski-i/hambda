<script>
	import {onMount} from 'svelte';
	import { CollapsibleCard } from 'svelte-collapsible';
    // export {default as Containers}

	let containers;
	let active_containers = [];
    
	onMount (async () => {
		containers = await fetch('http://pi.home:5000/dockerman/containers')
			.then(x => x.json())
		console.log(containers.containers)
		active_containers = containers.containers
	})
</script>

	<h2>Containers</h2>
	<div class = 'containers'>
		{#each active_containers as container}
		<div class='cards'>
			<CollapsibleCard open={false}>
				<h2 slot='header' class='header'>{container.name}</h2>
				<div slot='body' class='body'>
					<div>> Tags:{#each container.image_tags as tag}
						<div class = 'tag'>{tag.trim()}</div> 
					{/each}
					</div>
					> Status: <div class="{container.status === 'running' ? 'status-running' : 'status-other'}">{container.status}</div>
					

					<div>
						> ContainerID: {container.id}
					</div>
				</div>
			</CollapsibleCard>
		</div>
		{/each}
	</div>

<style>
	.containers {
		float: left;
	}

	.cards {
		width: 1000px auto;
        /* width: 100%; */
        /* max-width: 550px; */
        margin: 0 auto;
    }

    :global(.card) {
        margin-top: 1em;
        overflow: hidden;
        font-family: Arial, Helvetica, sans-serif;
    }


    .header {
        margin: 0;
        padding: 0.5em;
        border: 1px solid #aa3e00;
        border-radius: 10px;
        background: #222;
        transition: border-radius 0.5s step-end;
    }

    :global(.card.open) .header {
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        transition: border-radius 0.5s step-start;
    }

    .body {
        padding: 1em;
        border: 1px solid #aa2e00;
        margin-top: 0.25em;
        background: #222;
        /* display: flex; */
        border-radius: 10px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
    }

	.tag {
		background: #76a85e;
		border: 1px solid #229922;
		border-radius: 5px;
		margin: 5px;
		display: inline-block;
	}

	.status-running {
		color: #0f0;
		display: inline-block;
		margin: 5px;
	}

	.status-other {
		color: #f00;
		display: inline-block;
		margin: 5px;
	}


</style>