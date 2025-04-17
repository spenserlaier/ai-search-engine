<script lang="ts">
    const BACKEND_URL = "http://localhost:9000/";
    import SearchResult from "./lib/SearchResult.svelte";
    import SearchResultList from "./lib/SearchResultList.svelte";
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
        const querySegment = `search?query=${processedQuery}`;
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
        nothing submitted yet
    </main>
{:else}
    <!-- Results View -->
    <main class="results">
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
        {#if queryResponse !== undefined}
            <SearchResultList
                {BACKEND_URL}
                {query}
                results={queryResponse.results}
            />
        {:else}
            queryresponse is apparently undefined: {queryResponse}
        {/if}
    </main>
{/if}
