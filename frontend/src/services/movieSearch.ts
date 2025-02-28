import { API_URL } from "../config";

export async function searchMovies(query: string) {
    const response = await fetch(`${API_URL}/movies/search?query=${query}`);
    if (!response.ok) {
        throw new Error("Error al buscar películas");
    }
    return await response.json();
}
