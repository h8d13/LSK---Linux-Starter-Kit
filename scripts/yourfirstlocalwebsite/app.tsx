'use client';
import { useEffect, useState } from 'react';
import Image from 'next/image';

export default function Home() {
  const [data, setData] = useState<{ message?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fetchTime, setFetchTime] = useState<number | null>(null);

  useEffect(() => {
    const startTime = performance.now();

    fetch('http://127.0.0.1:5000/api/data')
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Failed to fetch: ${res.status}`);
        }
        return res.json();
      })
      .then((data) => {
        const endTime = performance.now();
        setFetchTime(endTime - startTime);
        setData(data);
      })
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <main className="flex flex-col gap-8 row-start-2 items-center sm:items-start">
        <div className="flex items-center gap-4">
          <Image
            src="/pythonblack.png"
            alt="Python Logo"
            width={40}
            height={40}
            className="dark:invert"
          />
          <h1 className="text-2xl font-bold">Next.js + Python Backend</h1>
        </div>
        <div>
          {error ? (
            <p className="text-red-500">Error: {error}</p>
          ) : data && data.message ? (
            <div>
              <p>{data.message}</p>
              <p className="text-sm text-gray-500 mt-2">
                Fetch time: {fetchTime?.toFixed(2)}ms
              </p>
            </div>
          ) : (
            <p>Loading data from backend...</p>
          )}
        </div>
      </main>
    </div>
  );
}
