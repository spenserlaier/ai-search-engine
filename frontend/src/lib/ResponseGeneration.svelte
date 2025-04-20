<script lang="ts">
    export let query: string;
    export let BACKEND_URL: string;
    let generatedResponse = "";
    let responseExists = false;
    async function generateResponse(query: string) {
        let res = await fetch(BACKEND_URL + "generate-answer", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                query: query,
            }),
        });
        let json = await res.json();
        generatedResponse = json.response;
    }
    async function handleGenerateResponse(e: Event) {
        e.preventDefault();
        if (!responseExists) {
            await generateResponse(query);
            responseExists = true;
        }
    }
</script>

<div class="generated-response">
    <button on:click={handleGenerateResponse}>Generate Response With AI</button>
    <div>{responseExists ? generatedResponse : ""}</div>
</div>
