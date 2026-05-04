import React from "react";
import { useNavigate } from "react-router-dom";
import { FaUserAlt, FaMicrophone, FaVideo } from "react-icons/fa";

function SelectionPage() {
  const navigate = useNavigate();

  const cards = [
    {
      title: "Facial",
      icon: <FaUserAlt size={42} />,
      gradient: "from-green-400 to-teal-500",
      description: "Analyze facial expressions using AI",
    },
    {
      title: "Audio",
      icon: <FaMicrophone size={42} />,
      gradient: "from-blue-400 to-cyan-500",
      description: "Analyze voice tone & speech patterns",
    },
    {
      title: "Video",
      icon: <FaVideo size={42} />,
      gradient: "from-orange-400 to-amber-500",
      description: "Fusion of facial + voice analysis",
    },
  ];

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-900 text-white px-6">
      <h2 className="text-3xl font-bold mb-2">Select Analysis Mode</h2>
      <p className="text-gray-300 mb-10 text-center max-w-lg">
        Choose how you want to analyze personality using AI.
      </p>

      <div className="grid md:grid-cols-3 gap-6 w-full max-w-5xl">
        {cards.map((card, index) => (
          <div
            key={index}
            onClick={() => navigate("/upload", { state: { type: card.title } })}
            className="bg-gray-800 rounded-2xl overflow-hidden cursor-pointer hover:scale-105 transition shadow-lg border border-gray-700 hover:border-gray-500"
          >
            <div className={`h-32 flex items-center justify-center bg-gradient-to-r ${card.gradient}`}>
              {card.icon}
            </div>

            <div className="p-4">
              <h4 className="font-semibold text-lg">{card.title}</h4>
              <p className="text-gray-400 text-sm mt-2">{card.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SelectionPage;