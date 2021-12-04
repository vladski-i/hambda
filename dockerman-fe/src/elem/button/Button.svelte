<script>
	import { onMount } from 'svelte'
	import { tweened } from 'svelte/motion'
	import Ripple from './Ripple.svelte'	
	import { writable } from 'svelte/store'
	
	export let rippleBlur = 2,
						 speed = 500,
						 color = '#fff',
						 fontSize = '1rem',
						 bgColor = '93, 120, 255',
						 bgHover = bgColor,
						 bgActive = bgColor,
						 rippleColor = '#264169',
						 round = '0.5rem',
						 height = 60,
					 	 width = 250,
						 sizeIn = 20,
						 opacityIn = 0.2,
						 shadow = 'none',
						 shadowHover = 'none',
						 shadowActive = 'none';

    export let clickCallback = null;

    const click = () => {
        clickCallback()
    }
	
	let shadows = {
			none: 'none',
			1: '0 0 0 1px rgba(0, 0, 0, 0.05)',
			2: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
			3: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
			4: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
			5: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
			6: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
			7: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
		}, mouseX, mouseY


	function handleRipple() {
		const ripples = writable([]);

		return {
			subscribe: ripples.subscribe,

			add: item => {
				ripples.update( items => {
					return [...items, item]
				});
			},
			clear: () => {
				ripples.update( items => {
					return []
				});
			}
		}
	}

	export const ripples = handleRipple();
	
	let rect, rippleBtn, w, h, x, y, offsetX, offsetY, deltaX, deltaY, locationY, locationX, scale_ratio, timer
	
	let coords = { x: 50, y: 50 }
	
	$: offsetX = Math.abs( (w / 2) - coords.x ),
		 offsetY = Math.abs( (h / 2) - coords.y ),
		 deltaX = (w / 2) + offsetX,
     deltaY = (h / 2) + offsetY,
		 scale_ratio = Math.sqrt(Math.pow(deltaX, 2.2) + Math.pow(deltaY, 2.2))

	const debounce = () => {
		clearTimeout(timer);
		timer = setTimeout(() => {
			ripples.clear()
		}, speed + (speed * 2));
	}
	
	let touch
	
	function handleClick(e, type) {
		if (type == 'touch') {
			touch = true
			ripples.add({ x: e.pageX - locationX, y: e.pageY - locationY, size: scale_ratio })  
		} else {
			if (!touch) {
				ripples.add({ x: e.clientX - locationX, y: e.clientY - locationY, size: scale_ratio })
			}
			touch = false
		}
		debounce()
	}
	
	onMount(()=> {
		w = rippleBtn.offsetWidth
    h = rippleBtn.offsetHeight
		rect = rippleBtn.getBoundingClientRect()
		locationY = rect.y
		locationX = rect.x
	})
</script>

<button on:click style="--color: {color};--font-size: {fontSize};--bg-color: {bgColor};--bg-hover: {bgHover};--bg-active: {bgActive};--radius: {round};--ripple: {rippleColor};--height: {height}px;--width: {width}px;--shadow: {shadows[shadow]};--shadow-h: {shadows[shadowHover]};--shadow-a: {shadows[shadowActive]}" bind:this={rippleBtn} on:touchstart={e => handleClick(e.touches[0], 'touch')}  on:mousedown={e => {handleClick(e, 'click'); click()}}>
	<span>
		<slot></slot>
	</span>	
	<svg>
		{#each $ripples as ripple, index}
			<Ripple x="{ripple.x}" y="{ripple.y}" size={ripple.size} {speed} {sizeIn} {opacityIn} {rippleBlur}/>
		{/each}

	</svg>
</button>

<style>
	button {
		-webkit-appearance: none;
		-moz-appearance: none;
		appearance: none;
		border: none;
		font-weight: 500;
		color: var(--color);
		font-size: var(--font-size);
		height: var(--height);
		width: var(--width);
		max-width: 100%;
		margin: 0;
		padding: 0;
		position: relative;
		border-radius: var(--radius);
		cursor: pointer;
		-webkit-transition: 200ms all ease-out;
		transition: 200ms all ease-out;
		background-color: rgba(var(--bg-color), 1);
		overflow: hidden;
		font-family: Roboto, sans-serif;
		box-shadow: var(--shadow);
		-webkit-touch-callout: none;
    -webkit-user-select: none;
    -khtml-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
		-webkit-tap-highlight-color: transparent;
	}

	button:hover,
	button:focus {
		outline: none;
		background-color: rgba(var(--bg-hover), .8);
		box-shadow: var(--shadow-h)
	}
	button:active {
		outline: none;
		background-color: rgba(var(--bg-active), .7);
		box-shadow: var(--shadow-a)
	}
	span {
		position: relative;
		height: 100%;
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		margin: 0;
		padding: 0;
		z-index: 1;
	}
	svg {
		height: 100%;
    pointer-events: none;
    position: absolute;
    top: 0;
    left: 0;
    z-index: 0;
    width: 100%;
	}
</style>