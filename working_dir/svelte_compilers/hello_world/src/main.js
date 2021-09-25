import App from './App.svelte';

const app = new App({
	target: document.body, // our target is body directly instead of wrapper elements
    // we dont need any props for this project
});

export default app;