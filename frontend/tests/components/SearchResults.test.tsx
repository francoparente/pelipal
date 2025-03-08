// import React from "react";
import { render, screen } from "@testing-library/react";
import SearchResults from "@/components/SearchResults";

describe("SearchResults", () => {
  it("Show nothing if there are no results", () => {
    render(<SearchResults results={null} />);
    expect(screen.queryByText("La película ya está descargada en:")).not.toBeInTheDocument();
    expect(screen.queryByText("Resultados de YTS:")).not.toBeInTheDocument();
  });

  it("Displays a message if the movie is already downloaded", () => {
    const results = {
      source: "HDD" as const,
      path: ["/ruta/a/pelicula1", "/ruta/a/pelicula2"],
    };
    render(<SearchResults results={results} />);
    expect(screen.getByText("Movie was found in:")).toBeInTheDocument();
    expect(screen.getByText("/ruta/a/pelicula1")).toBeInTheDocument();
    expect(screen.getByText("/ruta/a/pelicula2")).toBeInTheDocument();
  });

  it("Show YTS results if the movie is not on HDD", () => {
    const results = {
      source: "YTS" as const,
      data: {
        data: {
          movies: [
            { id: 1, title: "Inception", year: 2010 },
            { id: 2, title: "Interstellar", year: 2014 },
          ],
        },
      },
    };
    render(<SearchResults results={results} />);
    expect(screen.getByText("YTS results:")).toBeInTheDocument();
    expect(screen.getByText("Inception (2010)")).toBeInTheDocument();
    expect(screen.getByText("Interstellar (2014)")).toBeInTheDocument();
  });
});
