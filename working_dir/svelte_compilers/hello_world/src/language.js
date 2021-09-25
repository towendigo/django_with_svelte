import { readable } from 'svelte/store';

// get data from django-template
export const lanJS = readable(JSON.parse(document.getElementById("values-json").textContent));