<script context='module'>
    let editor = undefined;
    export function setContext(newCode, newLanguage) {
        let model = monaco.editor.createModel(newCode)
        monaco.editor.setModelLanguage(model,newLanguage)
        editor.setModel(model)
    }
    export function getCode() {
        return editor.getValue()
    }
</script>
<script>
    import 'monaco-editor/esm/vs/editor/browser/controller/coreCommands.js';
    import 'monaco-editor/esm/vs/editor/contrib/find/findController.js';
    import * as monaco from 'monaco-editor/esm/vs/editor/editor.api.js';
    import 'monaco-editor/esm/vs/basic-languages/python/python.contribution.js';
    import 'monaco-editor/esm/vs/basic-languages/java/java.contribution.js';
	import {onMount} from 'svelte';

    let container;
    let value = '';

    onMount(() => {
        self.MonacoEnvironment = {
        getWorkerUrl: function (moduleId, label) {
                // if (label === 'json') {
                // 	return './json.worker.bundle.js';
                // }
                // if (label === 'css' || label === 'scss' || label === 'less') {
                // 	return './css.worker.bundle.js';
                // }
                // if (label === 'html' || label === 'handlebars' || label === 'razor') {
                // 	return './html.worker.bundle.js';
                // }
                // if (label === 'typescript' || label === 'javascript') {
                // 	return './ts.worker.bundle.js';
                // }
                return './editor.worker.bundle.js';
            }
        };
        console.log(container)
        monaco.editor.setTheme('vs-dark');
        editor = monaco.editor.create(container, {
        value: value,
        language: 'python'
        });
        editor.setValue('def index():\n');
    });
</script>

<div id="editor-container" bind:this={container} style="height: 500px; text-align: left">
</div>