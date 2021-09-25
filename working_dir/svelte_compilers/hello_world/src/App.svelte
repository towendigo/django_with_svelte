<script>
	import {lanJS} from './language'; // our data from django-template
	
	// parsing data
	let content = $lanJS.content.content;  // dollar sign is used to subscribe to store (our data from django-template)
	let colors = $lanJS.color;
	let message = $lanJS.message;
	// ------
</script>

<main>
	<h1>
		{content} <!-- hello world -->
		<span style="color:{colors.color1};"> ! </span> <!-- ! sign in color1 -->
		<span style="color:{colors.color2};"> ! </span> <!-- ! sign in color2 -->
		<span style="color:{colors.color3};"> ! </span> <!-- ! sign in color3 -->
	</h1> 

	{#if message} <!-- if there is a (warning) message show message in footer -->
	<footer>
		<p>
			{message} <!-- (warning) message -->
		</p>
	</footer>
	{/if}
</main>

<style> /* Styling */
	main{
		height: 100vh;
		width: 100vw;

		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;

		color: white;
		text-align: center;

		background-image: url("http://127.0.0.1:8000/static/media/worldmap.svg");
		background-repeat: no-repeat;
		background-size: contain;
		background-position: center;
	}
	h1{
		padding: 1em 2em;
		width: fit-content;
		
		background: #00000099;
		box-shadow: 0px 0px 1em 0.5em #00000099;
	}
	footer{
		position: absolute;
		bottom: 0px;
		left: 0px;
		width: 100%;
		height: fit-content;
		padding: 1em 2em;

		background: #00000099;
	}
</style>