<script>
	import {onMount} from 'svelte';
	import { CollapsibleCard } from 'svelte-collapsible';
	import { default as ContainerLogs} from './ContainerLogs.svelte'
    // export {default as Containers}

	let containers;
	let active_containers = [];
	let container_id;
	let name;
    
	onMount (async () => {
		containers = await fetch('http://[2a02:a58:8251:100:dea6:32ff:fec4:cb3c]:5000/dockerman/containers')
			.then(x => x.json())
		console.log(containers.containers)
		active_containers = containers.containers
	})
</script>

	<div class= 'flex-container'>
		<div class= 'flex-child cards'>
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
							<div>
								> <a href='/' on:click|preventDefault={() => {container_id = container.id; name = container.name}}>  Logs</a>
							</div>
						</div>
					</CollapsibleCard>
				</div>
				{/each}
			</div>
		</div>
		<div class= 'flex-child logs'>
			<ContainerLogs container_id= {container_id} name = {name}/>
		</div>
	</div>

<style>
	.flex-container {
		display: flex;
	}

	.flex-child {
		flex: 1;
		border: 2px solid #aa3e00;
		border-radius: 5px;
	}  

	.flex-child:first-child {
		flex: 0.5;
		margin-right: 20px;
	} 

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
        background: #20262d;
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