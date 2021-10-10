<script>
    import {onMount} from 'svelte';
    import {default as Editor, setContext, getCode} from './elem/Editor.svelte';
    import {default as Button} from './elem/button/Button.svelte';
    import {materialBtn} from './elem/button/button.js';
    const axios = require('axios').default


    let templates = [];
    let selected;
    let endpoint = '/test';

    onMount( () => {
        axios.get('http://pi.home:5000/dockerman/images/templates')
            .then((resp) => {
                templates = resp.data.templates
                console.log(templates)
                selected = templates[0]
                console.log(selected)
            })
    });

    let submitBuild = () =>{
        let code = getCode()
        console.log(code)
        axios.post('http://pi.home:5000/dockerman/build',{
            "endpoint": endpoint,
            "code": code
        })
        .then((resp) => {
            console.log(resp)
        })
    }
</script>


<div>
    <div display=inline-block>
        <select bind:value={selected} on:change="{() => {setContext(selected.code, selected.language);console.log(selected)}}">
            {#each templates as template}
                <option value={template}>
                    {template.name}
                </option>
            {/each}
        </select>
        Endpoint:
        <input value= {endpoint}>
        <Editor />
        <div class='submit-button'>
            <Button {...materialBtn} clickCallback ={submitBuild}>
                Submit for build
            </Button>
        </div>
    </div>
</div>

<style>
    .submit-button {
        float: right;
        margin-top: 2em;
        margin-right: 2em;
    }
</style>