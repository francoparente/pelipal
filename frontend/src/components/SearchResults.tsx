interface Movie {
    id: number;
    title: string;
    year: number;
  }
  
  interface SearchResultsProps {
    results: {
      source: "HDD" | "YTS";
      path?: string[];
      data?: {
        data: {
          movies: Movie[];
        };
      };
    } | null;
    onSelect?: (movie: Movie) => void;
  }
  
  const SearchResults = ({ results, onSelect }: SearchResultsProps) => {
    if (!results) return null;
    
    if (results.source === "HDD") {
      return (
        <div className="mt-4 p-4 bg-green-100 rounded">
          <p>Movie was found in:</p>
          <ul>
            {results.path?.map((path, index) => (
              <li key={index}>{path}</li>
            ))}
          </ul>
        </div>
      );
    }
  
    if (results.source === "YTS") {
        return (
          <div className="mt-4">
            <h2 className="text-xl font-bold">YTS results:</h2>
            <ul className="space-y-2">
              {results.data?.data.movies.map((movie) => (
                <li
                  key={movie.id}
                  onClick={() => onSelect?.(movie)}
                  className="p-2 border rounded cursor-pointer hover:bg-gray-100"
                >
                  {movie.title} ({movie.year})
                </li>
              ))}
            </ul>
          </div>
        );
      }
      
    return null;
  };
  
  export default SearchResults;