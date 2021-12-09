<script>
    import {onMount} from 'svelte';
    import {default as Editor, setContext, getCode} from './elem/Editor.svelte';
    import {default as Button} from './elem/button/Button.svelte';
    import {materialBtn} from './elem/button/button.js';
    import { Jumper } from 'svelte-loading-spinners';
    import {default as ContainerLogs} from './ContainerLogs.svelte';
    const axios = require('axios').default


    let templates = [];
    let selected;
    let endpoint = '/test';
    let stage = 'code';
    let poller;
    let build_logs;
    let run_logs;
    let id;

    const intersperse = (arr, sep) => arr.reduce((a,v)=>[...a,v,sep],[]).slice(0,-1);

    onMount( () => {
        axios.get('http://192.168.100.43/dockerman/images/templates')
            .then((resp) => {
                templates = resp.data.templates
                console.log(templates)
                selected = templates[0]
                console.log(selected)
            })
    });

    let submitBuild = () =>{
        let code = getCode()
        let image_id;
        console.log(code)
        console.log("endpoint is %s",endpoint)
        let build = async () => axios.post('http://192.168.100.43/dockerman/build',{
            "endpoint": endpoint,
            "code": code
        })
        .then((resp) => {
            console.log("got response from build: %O",resp)
            console.log("got image id %s",image_id)
            return resp;
        })
        build().then((resp) => {
            console.log("build then %O",resp)
            image_id = resp.data.id
            console.log("set image_id to %s",resp.data.id)
            stage = 'build'
            console.log("setting up poller for %s",image_id)
            setupPoller(image_id)
            id = image_id
        })
    }

    let doPoll = (id) => {
        console.log("Polling for status for %s", id)
        if (!id){
            console.log("wrong id [%s]",id)
            clearInterval(poller)
        }
        axios.post('http://192.168.100.43/dockerman/images/status',{
            "id": id
        }).then((resp => {
            console.log(resp)
            switch(resp.data.status) {
                case 'BUILDING':
                    break;
                case 'FINISHED':
                    clearInterval(poller);
                    stage = 'finished';
                    build_logs = resp.data.logs;
                    console.log(build_logs)
                    break;
                case 'BUILD_FAILED':
                    clearInterval(poller);
                    stage = 'error'
                    build_logs = resp.data.logs;
                    break;
                default:
                    clearInterval(poller);
                    stage = 'error'

            }
        })).catch(err => clearInterval(poller))
    }

    let setupPoller = (id) => {
        console.log("setupPoller for %s",id)
        if(poller){
            clearInterval(poller)
        }
        poller = setInterval(() => {
            doPoll(id)
        }, 2000);
    }

    let submitRun = () => {
        console.log("submitting %s for run", id)
        stage= 'waiting'
        axios.post('http://192.168.100.43/dockerman/run', {
            id : id
        }).then((resp) => {
            run_logs = resp.data.logs
            stage = 'running'
        }).catch(err => {
            stage = 'error'
        })
    }
</script>


<div>
    {#if stage == 'code'}
    <div display=inline-block>
        <select bind:value={selected} on:change="{() => {setContext(selected.code, selected.language);console.log(selected)}}">
            {#each templates as template}
                <option value={template}>
                    {template.name}
                </option>
            {/each}
        </select>
        Endpoint:
        <input bind:value= {endpoint}>
        <Editor />
        <div class='submit-button'>
            <Button {...materialBtn} clickCallback ={submitBuild}>
                Submit for build
            </Button>
        </div>
    </div>
    {:else if stage == 'build'}
    <div class='center'>
        <div class='building'>Building... </div><br>
        <div class = 'spinner'>
            <Jumper size="60" color="#FF3E00" unit="px" duration="1s"></Jumper>
        </div>
    </div>
    {:else if stage == 'error'}
    <div class='center'>
        <div class='error'>Error :(</div>
        {#each build_logs as log}
            <ul>
                <li>{log}</li>
            </ul>
        {/each}
    </div>
    {:else if stage == 'finished'}
    <div class='center'>
        <div class='finished'>Finished</div>
        {#each build_logs as log}
            <ul>
                <li>{log}</li>
            </ul>
        {/each}
        <div class='submit-button'>
            <Button {...materialBtn} clickCallback ={submitRun}>
                Continue to run
            </Button>
        </div>
    </div>
    {:else if stage == 'waiting'}
    <div class='center'>
        <div class= 'spinner'>
            <Jumper size="60" color="#FF3E00" unit="px" duration="1s"></Jumper>
        </div>
    </div>
    {:else if stage == 'running'}
    <div class='center'>
        <ContainerLogs mongo_id = {id}/>
    </div>
    {/if}
</div>

<style>
    .submit-button {
        float: right;
        margin-top: 2em;
        margin-right: 2em;
    }
    ul {
        list-style-type: none; /* Remove bullets */
        padding: 0; /* Remove padding */
        margin: 0; /* Remove margins */
    }
    .center {
        margin: auto;
        width: 50%;
        padding: 10px;
    }
    .spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    .finished {
        color: #0f0;
		display: inline-block;
		margin: 5px;
        background: #76a85e;
		border: 1px solid #229922;
		border-radius: 5px;
		display: inline-block;
        font-size: large;
    }
    .building {
        color: #00f;
		display: inline-block;
		margin: 5px;
        background: #76a85e;
		border: 1px solid #229922;
		border-radius: 5px;
		display: inline-block;
        font-size: large;
    }
    .error {
        color: #f00;
		display: inline-block;
		margin: 5px;
        background: #76a85e;
		border: 1px solid #229922;
		border-radius: 5px;
		display: inline-block;
        font-size: large;
    }
</style>