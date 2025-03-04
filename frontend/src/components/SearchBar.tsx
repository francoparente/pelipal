import { useState } from "react";
import api from "../lib/api";

interface SearchBarProps {
  onSearch: (results: any) => void;
}

const SearchBar = ({ onSearch }: SearchBarProps) => {
  const [query, setQuery] = useState<string>("");

  const handleSearch = async () => {
    try {
      const response = await api.get("/movies/search", {
        params: { movie_title: query },
      });
      console.log("Respuesta del backend:", response.data);
      onSearch(response.data);
    } catch (error) {
      console.error("Error searching movie:", error);
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Buscar película..."
        className="p-2 border rounded"
      />
      <button
        onClick={handleSearch}
        className="p-2 bg-blue-500 text-white rounded"
      >
        Buscar
      </button>
    </div>
  );
};

export default SearchBar;