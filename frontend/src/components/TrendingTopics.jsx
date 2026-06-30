export default function TrendingTopics({ askAI }) {

  const topics = [
    "Artificial Intelligence",
    "Cricket World Cup",
    "Semiconductors",
    "Electric Vehicles",
    "Space Exploration"
  ];

  return (
    <div className="mt-12">

      <h2 className="mb-5 text-gray-400">
        TRENDING TOPICS
      </h2>

      <div className="flex gap-4 flex-wrap">

        {topics.map((topic) => (
          <button
            key={topic}
            onClick={() => askAI(topic)}
            className="bg-gray-900 px-5 py-3 rounded-xl hover:bg-gray-800 transition cursor-pointer"
          >
            {topic}
          </button>
        ))}

      </div>

    </div>
  );
}