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
        <div class="image-wrapper">
            {#if imageVisible}
                <img
                    class="thumbnail"
                    src={result.thumbnail}
                    alt="thumbnail"
                    on:error={handleError}
                />
            {/if}
        </div>
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
        flex-direction: row;
        align-items: center;
        justify-content: center;
        flex-wrap: wrap;
        max-width: 80%;
        min-width: 80%;
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
        width: 20vw;
        min-height: 1px;
        display: flex;
        justify-content: center;
        align-items: center;
        flex: 0 0 auto;
    }
    .thumbnail {
        min-width: 50%;
        justify-content: center;
    }
    .result-info {
        /*max-width: 80%;*/
        max-width: calc(100% - 20vw); /* ensures alignment */
        text-align: left;
    }
    .image-wrapper:empty::before {
        content: "";
        display: block;
        width: 100%;
        height: 100%;
    }
</style>
