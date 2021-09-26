<script>
    import 'monaco-editor/esm/vs/editor/browser/controller/coreCommands.js';
    import 'monaco-editor/esm/vs/editor/contrib/find/findController.js';
    import * as monaco from 'monaco-editor/esm/vs/editor/editor.api.js';
    import 'monaco-editor/esm/vs/basic-languages/python/python.contribution.js';
	import {onMount} from 'svelte';

    let container;

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
        monaco.editor.create(container, {
        value: [
            'from banana import *',
            '',
            'class Monkey:',
            '	# Bananas the monkey can eat.',
            '	capacity = 10',
            '	def eat(self, N):',
            "		'''Make the monkey eat N bananas!'''",
            '		capacity = capacity - N*banana.size',
            '',
            '	def feeding_frenzy(self):',
            '		eat(9.25)',
            '		return "Yum yum"'
        ].join('\n'),
        language: 'python'
        });
    });

</script>

<div id="editor-container" bind:this={container} style="height: 500px; text-align: left">
</div>