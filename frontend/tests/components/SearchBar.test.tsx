// import React from "react";
import { render, screen, fireEvent, waitFor  } from "@testing-library/react";
import { vi } from 'vitest';
import SearchBar from "@/components/SearchBar";
import api from "@/lib/api";

describe("SearchBar", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("Renders correctly", () => {
    render(<SearchBar onSearch={() => {}} />);
    expect(screen.getByPlaceholderText("Search movie...")).toBeInTheDocument();
    expect(screen.getByText("Search")).toBeInTheDocument();
  });

  it("Allows the user to type in the search bar", () => {
    render(<SearchBar onSearch={() => {}} />);
    const input = screen.getByPlaceholderText("Search movie...");
    fireEvent.change(input, { target: { value: "Inception" } });
    expect(input).toHaveValue("Inception");
  });

  it("Calls the onSearch function when the button is clicked", async () => {
    const mockOnSearch = vi.fn();
    const mockApiResponse = { data: { results: [] } };
    
    vi.spyOn(api, "get").mockResolvedValue(mockApiResponse);

    render(<SearchBar onSearch={mockOnSearch} />);

    const input = screen.getByPlaceholderText("Search movie...");
    fireEvent.change(input, { target: { value: "Inception" } });

    const button = screen.getByText("Search");
    fireEvent.click(button);

    await waitFor(() => {
      expect(mockOnSearch).toHaveBeenCalledWith(mockApiResponse.data);
    });

    expect(api.get).toHaveBeenCalledWith("/movies/search", {
      params: { movie_title: "Inception" },
    });
  });
});
