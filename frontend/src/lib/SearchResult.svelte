<script lang="ts">
    export let title: string;
    export let url: string;
    export let query: string;
    export let snippet: string;
    export let BACKEND_URL: string;
    let analyzing = false;
    type Analysis = {
        analysis: string;
    };
    export let analysis: string | null = null;
    async function analyze() {
        analyzing = true;
        const res = await fetch(BACKEND_URL + "analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: encodeURI(url),
                query: query,
            }),
        });
        const json: Analysis = await res.json();
        analysis = json.analysis;
        console.log(analysis);
    }
</script>

<article class="search-result">
    <h2 class="title">
        <a href={url} target="_blank" rel="noopener noreferrer">{title}</a>
    </h2>
    <p class="snippet">{snippet}</p>
    <small class="url">{url}</small>
    <button on:click={analyze} disabled={analyzing}
        >{analyzing ? "Generating Analysis..." : "Analyze Relevance"}</button
    >
    {#if analysis}
        <div class="analysis">
            {analysis}
        </div>
    {/if}
</article>

<style>
    .search-result {
        margin-bottom: 1.5rem;
    }
    .title a {
        font-size: 1.25rem;
        color: #0070f3;
        text-decoration: none;
    }
    .title a:hover {
        text-decoration: underline;
    }
    .snippet {
        margin-top: 0.25rem;
        color: #333;
    }
    .url {
        color: #666;
        font-size: 0.8rem;
    }
</style>
