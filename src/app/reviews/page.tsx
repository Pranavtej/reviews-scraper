"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "@/components/ui/pagination";

interface Review {
    reviewer_name: string;
    reviewer_info: string;
    company_info: string;
    usage_duration: string;
    review_title: string;
    rating: string;
    date: string;
    pros: string;
    cons: string;
}

export default function ProductReviews() {
    const searchParams = useSearchParams();
    const [reviews, setReviews] = useState<Review[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [productName, setProductName] = useState("");

    // Pagination
    const [page, setPage] = useState(1);
    const itemsPerPage = 5;
    const totalPages = Math.ceil(reviews.length / itemsPerPage);

    const productUrl = searchParams.get("url");
    const productNameParam = searchParams.get("name");

    useEffect(() => {
        if (productUrl && productNameParam) {
            setProductName(productNameParam);
            fetchReviews(productUrl);
        }
    }, [productUrl, productNameParam]);

    const fetchReviews = async (url: string) => {
        setLoading(true);
        setError("");

        try {
            const response = await fetch(
                `http://127.0.0.1:3200/get_product_reviews?product_url=${encodeURIComponent(url)}`,
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
            console.log("Fetched reviews:", data);
            setReviews(data);
        } catch (err) {
            console.error("Error fetching reviews:", err);
            setError("Failed to fetch reviews. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    // Get current page reviews
    const getCurrentPageReviews = () => {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;
        return reviews.slice(startIndex, endIndex);
    };

    // Generate star rating display
    const renderStars = (rating: string) => {
        const numRating = parseFloat(rating);
        if (isNaN(numRating)) return "☆☆☆☆☆";

        const fullStars = Math.floor(numRating);
        const stars = "★".repeat(fullStars) + "☆".repeat(5 - fullStars);
        return stars;
    };

    return (
        <div className="container mx-auto py-8 px-4">
            <Button
                onClick={() => window.history.back()}
                variant="outline"
                className="mb-4"
            >
                ← Back to Search Results
            </Button>

            <h1 className="text-3xl font-bold mb-2">
                {productName} Reviews
            </h1>

            {loading ? (
                <div className="flex justify-center my-10">
                    <div className="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent"></div>
                </div>
            ) : error ? (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded my-4">
                    {error}
                </div>
            ) : reviews.length === 0 ? (
                <div className="text-center py-10 text-gray-500">
                    No reviews found for this product.
                </div>
            ) : (
                <>
                    <p className="text-muted-foreground mb-6">
                        Found {reviews.length} reviews
                    </p>

                    <Table>
                        <TableCaption>Reviews for {productName}</TableCaption>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Reviewer</TableHead>
                                <TableHead>Review</TableHead>
                                <TableHead>Rating</TableHead>
                                <TableHead>Date</TableHead>

                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {getCurrentPageReviews().map((review, index) => (
                                <TableRow key={index}>
                                    <TableCell className="font-medium">
                                        <div>
                                            <div className="font-semibold">{review.reviewer_name}</div>
                                            <div className="text-xs text-muted-foreground">{review.reviewer_info}</div>
                                            <div className="text-xs text-muted-foreground mt-1">{review.company_info}</div>
                                            <div className="text-xs text-muted-foreground">{review.usage_duration}</div>
                                        </div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="font-semibold">{review.review_title}</div>
                                    </TableCell>
                                    <TableCell>
                                        <div className="text-amber-500 font-mono">{renderStars(review.rating)}</div>
                                        <div className="text-xs">{review.rating}/5.0</div>
                                    </TableCell>
                                    <TableCell>{review.date}</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>

                    {totalPages > 1 && (
                        <div className="mt-4 flex justify-center">
                            <Pagination>
                                <PaginationContent>
                                    <PaginationItem>
                                        <PaginationPrevious
                                            onClick={() => setPage(p => Math.max(1, p - 1))}
                                            className={page === 1 ? "pointer-events-none opacity-50" : ""}
                                        />
                                    </PaginationItem>

                                    {Array.from({ length: totalPages }).map((_, i) => (
                                        <PaginationItem key={i}>
                                            <PaginationLink
                                                onClick={() => setPage(i + 1)}
                                                isActive={page === i + 1}
                                            >
                                                {i + 1}
                                            </PaginationLink>
                                        </PaginationItem>
                                    ))}

                                    <PaginationItem>
                                        <PaginationNext
                                            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
                                            className={page === totalPages ? "pointer-events-none opacity-50" : ""}
                                        />
                                    </PaginationItem>
                                </PaginationContent>
                            </Pagination>
                        </div>
                    )}
                </>
            )}
        </div>
    );
}