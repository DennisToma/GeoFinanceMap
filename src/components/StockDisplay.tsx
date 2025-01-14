import React, { useEffect, useState } from 'react';
import * as d3 from 'd3';

interface Stock {
    ticker: string;
    name: string;
    sector: string;
    industry: string;
    country: string;
    city: string;
}

interface ApiResponse<T> {
    status: string;
    data: T;
}

interface SectorsResponse {
    status: string;
    sectors: string[];
}

const StockDisplay = () => {
    const [stocks, setStocks] = useState<Stock[]>([]);
    const [sectors, setSectors] = useState<string[]>([]);
    const [selectedSector, setSelectedSector] = useState<string>('');
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Fetch sectors for the filter
        const fetchSectors = async () => {
            try {
                const response = await fetch('http://localhost:8000/api/sectors');
                const data: SectorsResponse = await response.json();
                if (data.status === 'success') {
                    setSectors(data.sectors);
                }
            } catch (err) {
                console.error('Error fetching sectors:', err);
                setError('Failed to fetch sectors');
            }
        };

        fetchSectors();
    }, []);

    useEffect(() => {
        const fetchStocks = async () => {
            setLoading(true);
            try {
                const url = selectedSector 
                    ? `http://localhost:8000/api/stocks?sector=${encodeURIComponent(selectedSector)}`
                    : 'http://localhost:8000/api/stocks';
                
                const response = await fetch(url);
                const data: ApiResponse<Stock[]> = await response.json();
                
                if (data.status === 'success') {
                    setStocks(data.data);
                    setError(null);
                } else {
                    setError('Failed to fetch stocks data');
                }
            } catch (err) {
                console.error('Error fetching stocks:', err);
                setError('Failed to fetch stocks data');
            } finally {
                setLoading(false);
            }
        };

        fetchStocks();
    }, [selectedSector]);

    if (loading) {
        return <div className="flex justify-center items-center h-64">Loading...</div>;
    }

    if (error) {
        return <div className="text-red-500 text-center p-4">{error}</div>;
    }

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-6">Stock Market Data</h1>
            
            {/* Sector Filter */}
            <div className="mb-6">
                <select 
                    className="border p-2 rounded"
                    value={selectedSector}
                    onChange={(e) => setSelectedSector(e.target.value)}
                >
                    <option value="">All Sectors</option>
                    {sectors.map((sector) => (
                        <option key={sector} value={sector}>
                            {sector}
                        </option>
                    ))}
                </select>
            </div>

            {/* Stocks Table */}
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 border-b text-left">Ticker</th>
                            <th className="px-6 py-3 border-b text-left">Name</th>
                            <th className="px-6 py-3 border-b text-left">Sector</th>
                            <th className="px-6 py-3 border-b text-left">Industry</th>
                            <th className="px-6 py-3 border-b text-left">Country</th>
                            <th className="px-6 py-3 border-b text-left">City</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stocks.map((stock) => (
                            <tr 
                                key={stock.ticker} 
                                className="hover:bg-gray-50"
                            >
                                <td className="px-6 py-4 border-b font-medium">{stock.ticker}</td>
                                <td className="px-6 py-4 border-b">{stock.name}</td>
                                <td className="px-6 py-4 border-b">{stock.sector}</td>
                                <td className="px-6 py-4 border-b">{stock.industry}</td>
                                <td className="px-6 py-4 border-b">{stock.country}</td>
                                <td className="px-6 py-4 border-b">{stock.city}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {stocks.length === 0 && (
                <div className="text-center py-4 text-gray-500">
                    No stocks found
                </div>
            )}
        </div>
    );
};

export default StockDisplay;