<script lang="ts">
    export let title: string;
    export let url: string;
    export let snippet: string;
</script>

<article class="search-result">
    <h2 class="title">
        <a href={url} target="_blank" rel="noopener noreferrer">{title}</a>
    </h2>
    <p class="snippet">{snippet}</p>
    <small class="url">{url}</small>
</article>

<style>
    .search-result {
        margin-bottom: 1.5rem;
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
</style>
