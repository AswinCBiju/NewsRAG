import { useState } from "react";

export default function SearchBar({ askAI }) {

    const [query, setQuery] = useState("");

    return (
        <div className="flex justify-center mt-10">

            <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="What is the latest news about AI?"
                className="w-[600px] bg-gray-900 p-4 rounded-l-xl outline-none"
            />

            <button
                onClick={() => askAI(query)}
                className="bg-blue-600 px-8 rounded-r-xl cursor-pointer hover:bg-blue-700 transition"
            >
                Ask →
            </button>

        </div>
    );
}