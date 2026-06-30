import { useState } from "react";

import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import SearchBar from "./components/SearchBar";
import AnswerCard from "./components/AnswerCard";
import SourceCard from "./components/SourceCard";
import TrendingTopics from "./components/TrendingTopics";

import api from "./services/api";

export default function App() {
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const askAI = async (question) => {
    try {
      const res = await api.post("/ask", {
        question,
        session_id: "default",
      });

      setAnswer(res.data.response);

      // Backend currently doesn't return sources
      setSources([]);
    } catch (err) {
      console.error(err);
      setAnswer("An error occurred while contacting the AI backend.");
    }
  };

  return (
    <div>
      <Navbar />

      <div className="max-w-6xl mx-auto">
        <Hero />

        <SearchBar askAI={askAI} />

        <AnswerCard answer={answer} />

        {sources.length > 0 && (
          <>
            <h2 className="mt-12 mb-5 text-gray-400">
              SOURCES
            </h2>

            <div className="grid md:grid-cols-3 gap-5">
              {sources.map((s, index) => (
                <SourceCard
                  key={index}
                  source={s}
                />
              ))}
            </div>
          </>
        )}

        <TrendingTopics askAI={askAI} />
      </div>
    </div>
  );
}