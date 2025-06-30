<script lang="ts">
    //const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
    const BACKEND_URL =
        window.env?.VITE_BACKEND_URL || "http://localhost:5000/";
    import SearchResult from "./lib/SearchResult.svelte";
    import SearchResultList from "./lib/SearchResultList.svelte";
    let query = "";
    let submitted = false;
    let useOptimizedQueryResults = false;
    let selectedNewsCategory = "";
    let optimizedQueryResponse: SearchResponse | undefined = undefined;
    let queryResponse: SearchResponse | undefined = undefined;
    let priorQueryResponse: SearchResponse | undefined = undefined;
    let queryPage = 2;
    let optimizedQueryPage = 2;
    function rerankResultsCallback(listType: string) {
        if (listType == "ai-optimized") {
            return (results: Result[]) => {
                if (optimizedQueryResponse) {
                    optimizedQueryResponse = {
                        ...optimizedQueryResponse,
                        results: results,
                    };
                }
            };
            //} else if (listType === "default") {
        } else {
            return (results: Result[]) => {
                if (queryResponse) {
                    queryResponse = {
                        ...queryResponse,
                        results: results,
                    };
                }
            };
        }
    }

    async function loadMoreResults(listType: string) {
        console.log("attempting to load more results");
        if (listType === "ai-optimized") {
            if (optimizedQueryResponse !== undefined) {
                const body = buildQueryRequestBody(
                    optimizedQueryResponse.query,
                    optimizedQueryPage,
                );
                const searchResponse = await fetchSearchResults(body);
                if (searchResponse) {
                    const newResults = [
                        ...optimizedQueryResponse.results,
                        ...searchResponse.results,
                    ];
                    optimizedQueryResponse = {
                        ...searchResponse,
                        results: newResults,
                    };
                    optimizedQueryPage++;
                }
            }
        } else if (listType === "default") {
            if (queryResponse !== undefined) {
                const body = buildQueryRequestBody(
                    queryResponse.query,
                    queryPage,
                );
                const searchResponse = await fetchSearchResults(body);
                if (searchResponse) {
                    const newResults = [
                        ...queryResponse.results,
                        ...searchResponse.results,
                    ];
                    console.log(
                        "old length of results: ",
                        queryResponse.results.length,
                    );
                    queryResponse = {
                        ...searchResponse,
                        results: newResults,
                    };
                    console.log(
                        "new length of results: ",
                        queryResponse.results.length,
                    );
                    queryPage++;
                }
            }
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
    function buildQueryRequestBody(query: string, pageNumber = 1) {
        return {
            categories: selectedNewsCategory,
            //pageno: useOptimizedQueryResults ? optimizedQueryPage : queryPage,
            pageno: pageNumber,
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
    async function fetchSearchResults(
        body: ReturnType<typeof buildQueryRequestBody>,
    ): Promise<SearchResponse | undefined> {
        try {
            const results = await fetch(BACKEND_URL + "search", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body),
            });
            const json = await results.json();
            console.log("successfully retrieved search results: ", json);
            return json;
        } catch (e) {
            console.log("Error when fetching search results: ", e);
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
                const json = await fetchSearchResults(body);
                //console.log("retrieved web result: ", results);
                if (json) {
                    console.log("converted json: ", json);
                    queryResponse = { ...json };
                    useOptimizedQueryResults = false;
                    optimizedQueryResponse = undefined;
                }
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
                updateResultsCallback={async () => loadMoreResults("default")}
                updateListCallback={rerankResultsCallback("default")}
            />
        {:else if useOptimizedQueryResults && optimizedQueryResponse !== undefined}
            <h2>Optimized Query Results</h2>
            <h3>Optimized Query: {optimizedQueryResponse.query}</h3>
            <SearchResultList
                {BACKEND_URL}
                query={optimizedQueryResponse.query}
                results={optimizedQueryResponse.results}
                updateResultsCallback={async () =>
                    loadMoreResults("ai-optimized")}
                updateListCallback={rerankResultsCallback("ai-optimized")}
            />
        {:else if priorQueryResponse !== undefined}
            <SearchResultList
                {BACKEND_URL}
                {query}
                results={priorQueryResponse.results}
                updateResultsCallback={async () => loadMoreResults("default")}
                updateListCallback={rerankResultsCallback("default")}
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
