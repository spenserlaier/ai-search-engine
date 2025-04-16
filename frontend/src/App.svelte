<script lang="ts">
    const BACKEND_URL = "http://localhost:9000/";
    import SearchResult from "./lib/SearchResult.svelte";
    let query = "";
    let submitted = false;
    type SearchResponse = {
        results: Result[];
    };
    type Result = {
        title: string;
        url: string;
        content: string;
        score: number;
    };
    let queryResponse: SearchResponse | undefined = undefined;

    function buildQueryURL(query: string) {
        const processedQuery = encodeURIComponent(query);
        const querySegment = `search?q=${processedQuery}`;
        return BACKEND_URL + querySegment;
    }
    async function handleSearch(e: Event) {
        e.preventDefault();
        if (query.trim() !== "") {
            submitted = true;
            // Trigger actual search logic here
            const queryURL = buildQueryURL(query);
            const results = await fetch(queryURL);
            const json = await results.json();
            console.log("retrieved web result: ", results);
            console.log("converted json: ", json);
            queryResponse = json;
        }
    }

    function updateQuery(newQuery: string) {
        query = newQuery;
        // Optionally re-run search
    }
</script>

{#if !submitted}
    <!-- Landing Page View -->
    <main class="landing">
        <form on:submit={handleSearch}>
            <input bind:value={query} placeholder="Search..." />
            <button type="submit">Search</button>
        </form>
    </main>
{:else}
    <!-- Results View -->
    <main class="results">
        <div class="search-bar">
            <input bind:value={query} on:input={() => updateQuery(query)} />
            <!-- Maybe re-trigger search on change or on submit -->
        </div>

        <div class="filters">
            <button>All</button>
            <button>News</button>
            <button>Images</button>
            <!-- More categories -->
        </div>

        <div class="results-list">
            <div class="results-list">
                {#if queryResponse !== undefined}
                    {#each queryResponse.results as result}
                        <SearchResult
                            title={result.title}
                            url={result.url}
                            snippet={result.content}
                        />
                    {/each}
                {/if}
            </div>
            <!-- Show your enhanced LLM + SearXNG results here -->
        </div>
    </main>
{/if}
