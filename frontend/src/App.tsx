import { useState } from "react";
import SearchBar from "./components/SearchBar";
import SearchResults from "./components/SearchResults";

interface SearchResult {
  source: "HDD" | "YTS";
  path?: string[];
  data?: {
    data: {
      movies: {
        id: number;
        title: string;
        year: number;
      }[];
    };
  };
}

function App() {
  const [searchResults, setSearchResults] = useState<SearchResult | null>(null);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Buscador de Películas</h1>
      <SearchBar onSearch={setSearchResults} />
      <SearchResults results={searchResults} />
    </div>
  );
}

export default App;
