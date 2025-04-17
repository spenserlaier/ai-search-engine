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
</script>

<div class="results-list">
    {#each results as result}
        <SearchResult
            title={result.title}
            url={result.url}
            snippet={result.content}
            {BACKEND_URL}
            {query}
        />
    {/each}
</div>
