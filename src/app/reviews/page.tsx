"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Pagination, PaginationContent, PaginationItem, PaginationNext, PaginationPrevious } from "@/components/ui/pagination";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

interface Review {
    reviewer_name: string;
    reviewer_info: string;
    linkedin_verified: string;
    company_info: string;
    usage_duration: string;
    review_title: string;
    rating: string;
    date: string;
    pros: string;
    cons: string;
    review_id: string;
    source: string;
}

export default function ReviewsPage() {
    const searchParams = useSearchParams();
    const url = searchParams.get("url");
    const productName = searchParams.get("name");
    const source = searchParams.get("source") || "capterra";
    const startDate = searchParams.get("startDate");
    const endDate = searchParams.get("endDate");

    const [reviews, setReviews] = useState<Review[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [currentPage, setCurrentPage] = useState(1);
    const reviewsPerPage = 5; // Changed from 10 to 5 reviews per page

    useEffect(() => {
        const fetchReviews = async () => {
            if (!url) {
                setError("No product URL provided");
                setLoading(false);
                return;
            }

            setLoading(true);
            try {
                // Build query parameters
                const queryParams = new URLSearchParams();
                queryParams.append("product_url", url);
                if (source) queryParams.append("source", source);
                if (startDate) queryParams.append("start_date", startDate);
                if (endDate) queryParams.append("end_date", endDate);

                const response = await fetch(
                    `http://127.0.0.1:3200/get_product_reviews?${queryParams.toString()}`
                );

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                setReviews(data);
            } catch (err) {
                console.error("Error fetching reviews:", err);
                setError("Failed to fetch reviews. Please try again.");
            } finally {
                setLoading(false);
            }
        };

        fetchReviews();
    }, [url, source, startDate, endDate]);

    // Calculate pagination values
    const indexOfLastReview = currentPage * reviewsPerPage;
    const indexOfFirstReview = indexOfLastReview - reviewsPerPage;
    const currentReviews = reviews.slice(indexOfFirstReview, indexOfLastReview);
    const totalPages = Math.ceil(reviews.length / reviewsPerPage);

    // Create pagination array
    const pageNumbers = [];
    for (let i = 1; i <= totalPages; i++) {
        pageNumbers.push(i);
    }

    // Truncate text if too long
    const truncateText = (text: string, maxLength: number = 100) => {
        if (!text) return "";
        return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
    };

    return (
        <div className="p-10 max-w-8xl">
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h1 className="text-3xl font-bold mb-1">{productName || "Product"} Reviews</h1>
                    <p className="text-muted-foreground">
                        Source: {source === "g2" ? "G2" : "Capterra"}
                        {startDate && ` • From: ${startDate}`}
                        {endDate && ` • To: ${endDate}`}
                    </p>
                    <p className="text-muted-foreground">{reviews.length} reviews found</p>
                </div>
                <Button
                    variant="outline"
                    onClick={() => window.history.back()}
                >
                    Back to results
                </Button>
            </div>

            {loading ? (
                <div className="flex justify-center items-center h-64">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
                </div>
            ) : error ? (
                <div className="p-4 border border-red-300 bg-red-50 text-red-700 rounded-md">
                    {error}
                </div>
            ) : reviews.length === 0 ? (
                <div className="p-4 border bg-muted rounded-md text-center">
                    No reviews found for this product.
                </div>
            ) : (
                <>
                    <div className="border rounded-lg overflow-hidden">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="w-[180px]">Reviewer</TableHead>
                                    <TableHead className="w-[100px]">Rating</TableHead>
                                    <TableHead className="w-[120px]">Date</TableHead>
                                    <TableHead>Review</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {currentReviews.map((review, index) => (
                                    <TableRow key={review.review_id || index}>
                                        <TableCell className="align-top">
                                            <div>
                                                <div className="font-medium">{review.reviewer_name}</div>
                                                {review.linkedin_verified === "Yes" && (
                                                    <span className="inline-flex items-center text-xs text-blue-600">
                                                        <svg className="w-3 h-3 mr-1" viewBox="0 0 24 24" fill="currentColor">
                                                            <path d="M19 0h-14c-2.8 0-5 2.2-5 5v14c0 2.8 2.2 5 5 5h14c2.8 0 5-2.2 5-5v-14c0-2.8-2.2-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.3c-1 0-1.8-.8-1.8-1.7s.8-1.7 1.8-1.7 1.8.8 1.8 1.7-.8 1.7-1.8 1.7zm12.5 12.3h-3v-5.6c0-3.4-4-3.1-4 0v5.6h-3v-11h3v1.8c1.4-2.6 7-2.8 7 2.5v6.7z" />
                                                        </svg>
                                                        Verified
                                                    </span>
                                                )}
                                                {review.company_info && (
                                                    <p className="text-xs text-muted-foreground mt-1">{review.company_info}</p>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell className="align-top">
                                            <div className="flex items-center text-amber-500">
                                                <span className="font-bold">{review.rating}</span>
                                                <span className="ml-1">★</span>
                                            </div>
                                            {review.usage_duration && (
                                                <p className="text-xs text-muted-foreground mt-1">{review.usage_duration}</p>
                                            )}
                                        </TableCell>
                                        <TableCell className="align-top text-muted-foreground text-sm">
                                            {review.date}
                                        </TableCell>
                                        <TableCell>
                                            {review.review_title && (
                                                <h3 className="font-semibold mb-2">{review.review_title}</h3>
                                            )}

                                            {/* {review.pros && (
                                                <div className="mb-2">
                                                    <span className="text-sm font-semibold text-green-600">Pros:</span>
                                                    <p className="text-sm">{truncateText(review.pros, 150)}</p>
                                                </div>
                                            )}

                                            {review.cons && (
                                                <div>
                                                    <span className="text-sm font-semibold text-red-600">Cons:</span>
                                                    <p className="text-sm">{truncateText(review.cons, 150)}</p>
                                                </div>
                                            )} */}
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </div>

                    {totalPages > 1 && (
                        <Pagination className="mt-6">
                            <PaginationContent>
                                <PaginationItem>
                                    <PaginationPrevious
                                        onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                                        className={currentPage === 1 ? "pointer-events-none opacity-50" : "cursor-pointer"}
                                    />
                                </PaginationItem>

                                {/* Only show first page, current page-1, current page, current page+1, and last page */}
                                {pageNumbers.map(number => {
                                    // Always show first page, current page, and last page
                                    // For other pages, only show if they're adjacent to current page
                                    if (
                                        number === 1 ||
                                        number === totalPages ||
                                        number === currentPage ||
                                        number === currentPage - 1 ||
                                        number === currentPage + 1
                                    ) {
                                        return (
                                            <PaginationItem key={number}>
                                                <Button
                                                    variant={currentPage === number ? "default" : "outline"}
                                                    size="icon"
                                                    onClick={() => setCurrentPage(number)}
                                                    className="w-9 h-9"
                                                >
                                                    {number}
                                                </Button>
                                            </PaginationItem>
                                        );
                                    }

                                    // Add ellipsis (but only once)
                                    if (
                                        (number === 2 && currentPage > 3) ||
                                        (number === totalPages - 1 && currentPage < totalPages - 2)
                                    ) {
                                        return (
                                            <PaginationItem key={`ellipsis-${number}`}>
                                                <div className="px-2">...</div>
                                            </PaginationItem>
                                        );
                                    }

                                    return null;
                                })}

                                <PaginationItem>
                                    <PaginationNext
                                        onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                                        className={currentPage === totalPages ? "pointer-events-none opacity-50" : "cursor-pointer"}
                                    />
                                </PaginationItem>
                            </PaginationContent>
                        </Pagination>
                    )}
                </>
            )}
        </div>
    );
}