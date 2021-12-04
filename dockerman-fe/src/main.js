import './global.css';

import App from './App.svelte';
export { default as Containers } from './Containers.svelte'
const app = new App({
	target: document.body
});

export default app;
