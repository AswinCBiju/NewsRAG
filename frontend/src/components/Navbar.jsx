
export default function Navbar() {
  return (
    <nav className="flex justify-between items-center p-6 border-b border-gray-800">
      <h1 className="text-blue-400 font-bold text-xl">
        NewsRAG
      </h1>

      <div className="flex gap-8 text-gray-300">
        <a href="#">Home</a>
        <a href="#">Technology</a>
        <a href="#">Business</a>
        <a href="#">Sports</a>
        <a href="#">Politics</a>
      </div>
    </nav>
  );
}