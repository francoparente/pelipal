import './App.css'
import SearchBar from "./components/SearchBar";

function App() {
  const handleSearch = (query: string) => {
    console.log("Buscar:", query);
  };

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Buscar Películas</h1>
      <SearchBar onSearch={handleSearch} />
    </div>
  );
}

export default App
