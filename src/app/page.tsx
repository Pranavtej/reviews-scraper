"use client";

import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

// Define interface for search results
interface SearchResult {
  product_name: string;
  company: string;
  href: string;
  full_url: string;
  rating: string;
  reviews_count: string;
  description: string;
  logo_url: string;
}

export default function Home() {
  const [companyName, setCompanyName] = useState("");
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchSearchResults = async () => {
    if (!companyName.trim()) {
      setError("Please enter a company name");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `http://127.0.0.1:3200/get_reviews?company_name=${encodeURIComponent(companyName)}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      setSearchResults(data);
    } catch (err) {
      console.error("Error fetching search results:", err);
      setError("Failed to fetch search results. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-8 gap-8 max-w-3xl mx-auto">
      <div className="flex items-center justify-center bg-muted/50 rounded-full px-4 py-1 text-sm">
        🎉 New App
      </div>

      <h1 className="text-5xl md:text-7xl font-bold tracking-tight text-center">
        Reviews Scraper
      </h1>

      <p className="text-xl text-muted-foreground max-w-2xl text-center">
        Enter a company name to search on Capterra
      </p>

      <div className="w-full max-w-xl relative mt-4">
        <Input
          type="text"
          placeholder="e.g. Microsoft, Slack, Zoom"
          className="pr-12 py-6 text-lg"
          value={companyName}
          onChange={(e) => setCompanyName(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && fetchSearchResults()}
        />
        <Button
          size="icon"
          className="absolute right-1 top-1 bottom-1 h-auto aspect-square"
          variant="ghost"
          onClick={() => setCompanyName("")}
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4"><polyline points="9 10 4 15 9 20"></polyline><path d="M20 4v7a4 4 0 0 1-4 4H4"></path></svg>
        </Button>
      </div>

      <Button
        size="lg"
        className="mt-4 py-6 px-8 text-lg rounded-full"
        onClick={fetchSearchResults}
        disabled={loading}
      >
        {loading ? "Searching..." : "Search"}
      </Button>

      {error && (
        <div className="text-red-500 mt-4">{error}</div>
      )}

      {searchResults.length > 0 ? (
        <div className="w-full mt-8">
          <h2 className="text-2xl font-bold mb-6 text-center">Search Results</h2>
          <div className="space-y-6">
            {searchResults.map((result, index) => (
              <div key={index} className="border p-5 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <div className="flex gap-4">
                  {result.logo_url && (
                    <div className="flex-shrink-0 w-16 h-16 relative rounded overflow-hidden border">
                      <img
                        src={result.logo_url}
                        alt={`${result.product_name} logo`}
                        className="object-contain"
                        width={64}
                        height={64}
                      />
                    </div>
                  )}
                  <div className="flex-1">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <h3 className="text-xl font-semibold">{result.product_name}</h3>
                      <div className="flex items-center gap-1 text-amber-500">
                        <span>★</span>
                        <span>{result.rating}</span>
                        <span className="text-gray-500 text-sm">({result.reviews_count})</span>
                      </div>
                    </div>
                    <p className="text-sm text-muted-foreground">by {result.company}</p>
                    <p className="mt-2 text-sm line-clamp-2">{result.description}</p>
                    <div className="mt-3 flex gap-3">
                      <a
                        href={result.full_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-600 hover:underline text-sm"
                      >
                        View on Capterra
                      </a>
                      <Link
                        href={`/reviews?url=${encodeURIComponent(result.full_url)}&name=${encodeURIComponent(result.product_name)}`}
                        className="text-green-600 hover:underline text-sm"
                      >
                        View Reviews →
                      </Link>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        !loading && companyName.trim() && (
          <div className="text-center text-muted-foreground mt-8">
            No results found. Try a different search term.
          </div>
        )
      )}
    </div>
  );
}
