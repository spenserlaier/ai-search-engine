<script lang="ts">
    import SearchResult from "./SearchResult.svelte";
    import ResponseGeneration from "./ResponseGeneration.svelte";
    export let BACKEND_URL: string;
    export let query: string;
    export let results: Result[];
    //export let updateResultsCallback: () => Promise<void>;
    //export let updateListCallback: (results: Result[]) => void;
    export let updateResultsCallback: () => Promise<void> = async () => {};
    export let updateListCallback: (r: Result[]) => void;
    //let localResults = results;
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
        //localResults = [];
        //localResults = [...json];
        updateListCallback(json);
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
    <ResponseGeneration {BACKEND_URL} {query} />
    <div class="search-results">
        {#each results as result}
            <SearchResult {result} {BACKEND_URL} {query} />
        {/each}
    </div>
    <button on:click={updateResultsCallback}>Load More Results</button>
</div>

<style>
    .search-results {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
    }
</style>
