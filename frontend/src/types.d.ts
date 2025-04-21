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
    img_src: string;
};
type RankingRequest = {
    query: string;
    searchResults: Result[];
};
type Analysis = {
    analysis: string;
};
