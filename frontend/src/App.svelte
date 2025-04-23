<script lang="ts">
    const BACKEND_URL = "http://localhost:9000/";
    import SearchResult from "./lib/SearchResult.svelte";
    import SearchResultList from "./lib/SearchResultList.svelte";
    let query = "";
    let submitted = false;
    let useOptimizedQueryResults = false;
    let selectedNewsCategory = "";
    let optimizedQueryResponse: SearchResponse | undefined = undefined;
    let queryResponse: SearchResponse | undefined = undefined;
    let priorQueryResponse: SearchResponse | undefined = undefined;
    let queryPage = 1;
    let optimizedQueryPage = 1;
    async function loadMoreResults(listType: string) {
        if (listType === "ai-optimized") {
        } else if (listType === "default") {
        }
    }
    /*

    page number uses "pageno" as the query param 
    with a default value of 1

    */

    function buildQueryURL(query: string) {
        const processedQuery = encodeURIComponent(query);
        let newsCategoryParam = "";
        if (selectedNewsCategory !== "") {
            newsCategoryParam = `categories=${selectedNewsCategory}`;
        }
        const pageNumberParam = `page_number=${useOptimizedQueryResults ? optimizedQueryPage : queryPage}`;
        const queryParams = [newsCategoryParam, pageNumberParam]
            .filter((p) => p !== "")
            .join("&");
        const querySegment = `search?query=${processedQuery}&${queryParams}`;
        return BACKEND_URL + querySegment;
    }
    function buildQueryRequestBody(query: string) {
        return {
            categories: selectedNewsCategory,
            pageno: useOptimizedQueryResults ? optimizedQueryPage : queryPage,
            q: query,
            format: "json",
        };
    }

    async function getAiOptimizedResults(originalQuery: string) {
        try {
            const res = await fetch(BACKEND_URL + "smart-search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    query: originalQuery,
                }),
            });
            const json: SearchResponse = await res.json();
            console.log("got optimized query result: ", json);
            optimizedQueryResponse = json;
            optimizedQueryPage++;
        } catch {
            console.log(
                "Error when fetching/processing optimized query results",
            );
        }
    }

    async function toggleUseAiOptimizedResults(e: Event) {
        e.preventDefault();
        if (useOptimizedQueryResults === false && query !== "") {
            useOptimizedQueryResults = true;
            if (optimizedQueryResponse === undefined) {
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
            try {
                //const queryURL = buildQueryURL(query);
                const body = buildQueryRequestBody(query);
                console.log("prepared body: ", body);
                const results = await fetch(BACKEND_URL + "search", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(body),
                });
                const json = await results.json();
                console.log("retrieved web result: ", results);
                console.log("converted json: ", json);
                queryResponse = { ...json };
                useOptimizedQueryResults = false;
                optimizedQueryResponse = undefined;
            } catch {
                console.log("Encountered an error when attempting a search");
            }
        }
    }

    //TODO: after swapping to optimized query results, subsequent searches
    //no longer work. state management in general probably needs an overhaul

    function updateQuery(newQuery: string) {
        query = newQuery;
    }
    function updateSelectedCategory(e: Event, category: string) {
        selectedNewsCategory = category;
        handleSearch(e);
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
            <button on:click={(e) => updateSelectedCategory(e, "")}>All</button>
            <button on:click={(e) => updateSelectedCategory(e, "news")}
                >News</button
            >
            <button on:click={(e) => updateSelectedCategory(e, "images")}
                >Images</button
            >
            <!-- More categories -->
        </div>
        {#if !useOptimizedQueryResults && queryResponse !== undefined}
            <SearchResultList
                {BACKEND_URL}
                {query}
                results={queryResponse.results}
            />
        {:else if useOptimizedQueryResults && optimizedQueryResponse !== undefined}
            <h2>Optimized Query Results</h2>
            <h3>Optimized Query: {optimizedQueryResponse.query}</h3>
            <SearchResultList
                {BACKEND_URL}
                query={optimizedQueryResponse.query}
                results={optimizedQueryResponse.results}
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
