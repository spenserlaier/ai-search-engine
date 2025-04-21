<script lang="ts">
    const BACKEND_URL = "http://localhost:9000/";
    import SearchResult from "./lib/SearchResult.svelte";
    import SearchResultList from "./lib/SearchResultList.svelte";
    let query = "";
    let submitted = false;
    let useOptimizedQueryResults = false;
    let optimizedQueryResult: SearchResponse | undefined = undefined;

    type SearchResponse = {
        query: string;
        results: Result[];
    };
    type Result = {
        title: string;
        url: string;
        content: string;
        score: number;
        thumbnail: string;
    };
    type RankingRequest = {
        query: string;
        searchResults: Result[];
    };
    let queryResponse: SearchResponse | undefined = undefined;
    let priorQueryResponse: SearchResponse | undefined = undefined;

    function buildQueryURL(query: string) {
        const processedQuery = encodeURIComponent(query);
        const querySegment = `search?query=${processedQuery}`;
        return BACKEND_URL + querySegment;
    }

    async function getAiOptimizedResults(originalQuery: string) {
        const res = await fetch(BACKEND_URL + "smart-search", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: originalQuery,
            }),
        });
        const json: SearchResponse = await res.json();
        console.log("got optimized query result: ", json);
        optimizedQueryResult = json;
    }

    async function toggleUseAiOptimizedResults(e: Event) {
        e.preventDefault();
        if (useOptimizedQueryResults === false && query !== "") {
            useOptimizedQueryResults = true;
            if (optimizedQueryResult === undefined) {
                getAiOptimizedResults(query);
            }
        } else {
            useOptimizedQueryResults = false;
        }
    }
    async function handleSearch(e: Event) {
        e.preventDefault();
        if (query.trim() !== "") {
            submitted = true;
            if (queryResponse !== undefined) {
                priorQueryResponse = { ...queryResponse };
            } else {
                priorQueryResponse = undefined;
            }
            queryResponse = undefined;
            // Trigger actual search logic here
            const queryURL = buildQueryURL(query);
            const results = await fetch(queryURL);
            const json = await results.json();
            console.log("retrieved web result: ", results);
            console.log("converted json: ", json);
            queryResponse = { ...json };
            useOptimizedQueryResults = false;
        }
    }

    //TODO: after swapping to optimized query results, subsequent searches
    //no longer work. state management in general probably needs an overhaul

    function updateQuery(newQuery: string) {
        query = newQuery;
    }
</script>

{#if !submitted}
    <main class="landing">
        <form class="search-form" on:submit={handleSearch}>
            <input
                bind:value={query}
                class="search-bar"
                placeholder="Search..."
            />
            <button type="submit">Search</button>
        </form>
    </main>
{:else}
    <!-- Results View -->
    <main class="results">
        <button on:click={toggleUseAiOptimizedResults}>
            {useOptimizedQueryResults
                ? "Use Default Results"
                : "Optimize Query With AI"}
        </button>
        <form class="search-form" on:submit={handleSearch}>
            <input
                class="search-bar"
                bind:value={query}
                on:input={() => updateQuery(query)}
            />
            <button type="submit">Search</button>
        </form>
        <!-- Maybe re-trigger search on change or on submit -->

        <div class="filters">
            <button>All</button>
            <button>News</button>
            <button>Images</button>
            <!-- More categories -->
        </div>
        {#if !useOptimizedQueryResults && queryResponse !== undefined}
            <SearchResultList
                {BACKEND_URL}
                {query}
                results={queryResponse.results}
            />
        {:else if useOptimizedQueryResults && optimizedQueryResult !== undefined}
            <h2>Optimized Query Results</h2>
            <h3>Optimized Query: {optimizedQueryResult.query}</h3>
            <SearchResultList
                {BACKEND_URL}
                query={optimizedQueryResult.query}
                results={optimizedQueryResult.results}
            />
        {:else if priorQueryResponse !== undefined}
            <SearchResultList
                {BACKEND_URL}
                {query}
                results={priorQueryResponse.results}
            />
        {:else if priorQueryResponse === undefined}
            Loading Results...
        {/if}
    </main>
{/if}

<style>
    .landing {
        background: red;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .search-form {
        min-width: 90%;
        background: purple;
    }
    .search-bar {
        min-width: 60%;
        color: purple;
    }
</style>
