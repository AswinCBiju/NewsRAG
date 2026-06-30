
export default function Hero() {
  return (
    <div className="text-center mt-16">

      <div className="inline-block bg-blue-900 px-4 py-2 rounded-full text-sm">
        Powered by Gemini + RAG
      </div>

      <h1 className="text-6xl font-bold mt-6">
        Ask anything about
        <span className="text-blue-400">
          {" "}today's news
        </span>
      </h1>

      <p className="text-gray-400 mt-6 text-lg">
        Get AI-generated answers backed by
        real articles from trusted sources.
      </p>

    </div>
  );
}