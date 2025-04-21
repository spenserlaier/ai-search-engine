<script lang="ts">
    export let query: string;
    export let result: Result;
    export let BACKEND_URL: string;
    let analyzing = false;
    export let analysis: string | null = null;
    async function analyze() {
        analyzing = true;
        const res = await fetch(BACKEND_URL + "analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                url: encodeURI(result.url),
                query: query,
            }),
        });
        const json: Analysis = await res.json();
        analysis = json.analysis;
        console.log(analysis);
    }
    let imageVisible =
        (result.thumbnail !== "" && result.thumbnail !== null) ||
        result.img_src !== null;
    function handleError() {
        imageVisible = false;
        console.log("had an image error");
    }
    // TODO: if img_src exists as a property, then the search result is an image result and not a regualr text result,
    // which means we need to handle it differently
</script>

<article class="search-result">
    {#if result.img_src === ""}
        {#if imageVisible}
            <div class="image-wrapper">
                <img
                    class="thumbnail"
                    src={result.thumbnail}
                    alt="thumbnail"
                    on:error={handleError}
                />
            </div>
        {/if}
        <div class="result-info">
            <h2 class="title">
                <a href={result.url} target="_blank" rel="noopener noreferrer"
                    >{result.title}</a
                >
            </h2>
            <small class="url">{result.url}</small>
            <p class="snippet">{result.content}</p>
            <button
                class="analysis-button"
                style="visibility: {analysis ? 'hidden' : 'visible'}"
                on:click={analyze}
                disabled={analyzing}
                >{analyzing
                    ? "Generating Analysis..."
                    : "Analyze Relevance"}</button
            >
            {#if analysis}
                <div class="analysis">
                    {analysis}
                </div>
            {/if}
        </div>
    {:else if imageVisible}
        <div class="image-search-result">
            <img
                class="image-result"
                src={result.img_src}
                alt="search result"
                on:error={handleError}
            />
            <div class="image-information">
                <a href={result.url} rel="noopener noreferrer">
                    {result.title}</a
                >
                <small> {result.parsed_url[1]}</small>
            </div>
        </div>
    {/if}
</article>

<style>
    .search-result {
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
    }
    .image-search-result {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .image-information {
        display: flex;
        flex-direction: column;
    }
    .image-result {
        max-width: 20vw;
        height: auto;
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
    .image-wrapper {
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 0 0 auto;
    }
    .thumbnail {
        min-width: 50%;
    }
    .result-info {
        max-width: 80%;
    }
    /* Mobile: stack vertically */
    @media (max-width: 1400px) {
        .thumbnail {
            min-width: 5%;
        }
        .search-result {
            flex-direction: column;
            align-items: center;
        }

        .image-wrapper {
            width: 100%;
            margin-bottom: 1rem;
            justify-content: center;
        }

        .thumbnail {
            width: auto;
            max-width: 100%;
        }
    }
</style>
