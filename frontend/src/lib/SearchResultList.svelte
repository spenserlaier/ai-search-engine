<script lang="ts">
    import SearchResult from "./SearchResult.svelte";
    export let BACKEND_URL: string;
    export let query: string;
    type Result = {
        title: string;
        url: string;
        content: string;
        score: number;
    };
    export let results: Result[];
    let localResults = results;
    let awaitingRerank = false;
    async function rerankResults(query: string, results: Result[]) {
        awaitingRerank = true;
        const res = await fetch(BACKEND_URL + "rank", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: query,
                search_results: results,
            }),
        });
        const json = await res.json();
        console.log("retrieved reranked results. printing...");
        console.log(json);
        localResults = [...json];
        awaitingRerank = false;
    }
</script>

<div class="results-list">
    <button
        disabled={awaitingRerank}
        on:click={() => rerankResults(query, results)}
    >
        {awaitingRerank
            ? "Reranking Queries..."
            : "Rerank Results Using AI"}</button
    >
    {#each localResults as result}
        <SearchResult
            title={result.title}
            url={result.url}
            snippet={result.content}
            {BACKEND_URL}
            {query}
        />
    {/each}
</div>
