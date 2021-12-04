<script>
    export let container_id;
    export let mongo_id;
    export let name;
    let logs = [];
    let poller;

    $: {
        if (poller){
            clearInterval(poller)
        }
        setupPoller(container_id)
    }


    import {onMount, onDestroy} from 'svelte';
    const axios = require('axios').default

    let doPoll = container_id => {
        axios.post('http://[2a02:a58:8251:100:dea6:32ff:fec4:cb3c]:5000/dockerman/containers/logs', {
            'container_id' : container_id
        })
        .then(resp => {
            logs = resp.data.logs
        })
        .catch(err => {
            console.log(err)
            clearInterval(poller)
        })
    }

    onDestroy(() => {
        if (poller){
            clearInterval(poller)
        }
    })

    let setupPoller = (id) => {
        console.log("setupPoller for %s",id)
        if(poller){
            clearInterval(poller)
        }
        poller = setInterval(() => {
            doPoll(id)
        }, 2000);
    }
    
    onMount(() => {
        if (!container_id){
            axios.post('http://[2a02:a58:8251:100:dea6:32ff:fec4:cb3c]:5000/dockerman/containers/logs', {
                'id': mongo_id
            })
            .then(resp => {
                console.log('resp is %O',resp)
                container_id = resp.data.container_id
                setupPoller(container_id)
                logs = resp.data.logs
            }).catch(err => {
                console.log(err)
                logs = ""
            })
        }
    })

</script>

<div>
    <h2> Showing logs for {name || container_id || 'no container'}<br> </h2>
    <ul>
        {#each logs as log}
        <li>{log}</li>
        {/each}
    </ul>
</div>

<style>
    ul {
        list-style-type: none; /* Remove bullets */
        padding: 0; /* Remove padding */
        margin: 0; /* Remove margins */
    }
</style>