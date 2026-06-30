
export default function AnswerCard({ answer }) {

  if(!answer) return null;

  return (
    <div className="bg-gray-900 border border-blue-500 rounded-2xl p-8 mt-14">

      <h2 className="text-blue-400 mb-4">
        AI ANSWER
      </h2>

      <p className="text-gray-200 leading-8">
        {answer}
      </p>

    </div>
  );
}