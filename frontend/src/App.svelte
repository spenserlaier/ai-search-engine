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
    };
    type RankingRequest = {
        query: string;
        searchResults: Result[];
    };
    let queryResponse: SearchResponse | undefined = undefined;

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
        if (
            useOptimizedQueryResults === false &&
            optimizedQueryResult === undefined &&
            query !== ""
        ) {
            useOptimizedQueryResults = true;
            getAiOptimizedResults(query);
        } else {
            useOptimizedQueryResults = false;
        }
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
        nothing submitted yet
    </main>
{:else}
    <!-- Results View -->
    <main class="results">
        <button on:click={toggleUseAiOptimizedResults}>
            {useOptimizedQueryResults
                ? "Use Default Results"
                : "Optimize Query With AI"}
        </button>
        <div class="search-bar">
            <form on:submit={handleSearch}>
                <input bind:value={query} on:input={() => updateQuery(query)} />
                <button type="submit">Search</button>
            </form>
            <!-- Maybe re-trigger search on change or on submit -->
        </div>

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
        {:else}
            Loading Results...
        {/if}
    </main>
{/if}
