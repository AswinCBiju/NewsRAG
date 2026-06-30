
export default function SourceCard({ source }) {

  return (
    <div className="bg-gray-900 p-5 rounded-xl">

      <p className="text-blue-400 text-sm">
        {source.source}
      </p>

      <h3 className="mt-3 font-semibold">
        {source.title}
      </h3>

      <a
        href={source.url}
        target="_blank"
        className="text-blue-500 mt-4 block"
      >
        Read Article →
      </a>

    </div>
  );
}