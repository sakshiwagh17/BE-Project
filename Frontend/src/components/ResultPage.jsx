import React, { useRef, useMemo } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const reportRef = useRef();

  const type = location.state?.type || "General";
  const processingTime = location.state?.processingTime || 0;

  // ✅ Demo fallback
  const demoScores = {
    Openness: 0.72,
    Conscientiousness: 0.65,
    Extraversion: 0.58,
    Agreeableness: 0.8,
    Neuroticism: 0.4,
  };

  // ✅ FIXED: stable dependency
  const stateScores = location.state?.scores;

  const scores = useMemo(() => {
    return stateScores && Object.keys(stateScores).length > 0
      ? stateScores
      : demoScores;
  }, [stateScores]);

  // ✅ Derived data (no state)
  const traits = useMemo(() => {
    const traitNames = [
      "Openness",
      "Conscientiousness",
      "Extraversion",
      "Agreeableness",
      "Neuroticism",
    ];
    const colors = ["#9fe320", "#00BFA6", "#FF9800", "#4CAF50", "#F44336"];

    return traitNames.map((name, idx) => ({
      name,
      value: Math.round((scores[name] || 0.5) * 100),
      color: colors[idx],
    }));
  }, [scores]);

  const oceanInsights = {
    Openness: {
      label: "O - Openness",
      description: "Imagination & Curiosity",
      highDescription: "Creative, curious, and open to new experiences.",
      moderateDescription: "Balanced between creativity and practicality.",
      lowDescription: "Practical and prefers routine.",
      characteristics: {
        high: ["Creative", "Curious", "Adventurous"],
        moderate: ["Balanced", "Pragmatic"],
        low: ["Practical", "Consistent"],
      },
    },
    Conscientiousness: {
      label: "C - Conscientiousness",
      description: "Discipline & Organization",
      highDescription: "Highly organized and goal-oriented.",
      moderateDescription: "Balanced and adaptable.",
      lowDescription: "Spontaneous and flexible.",
      characteristics: {
        high: ["Organized", "Reliable"],
        moderate: ["Balanced"],
        low: ["Flexible", "Relaxed"],
      },
    },
    Extraversion: {
      label: "E - Extraversion",
      description: "Social Energy",
      highDescription: "Outgoing and energetic.",
      moderateDescription: "Balanced social energy.",
      lowDescription: "Reserved and introverted.",
      characteristics: {
        high: ["Outgoing", "Energetic"],
        moderate: ["Balanced"],
        low: ["Calm", "Focused"],
      },
    },
    Agreeableness: {
      label: "A - Agreeableness",
      description: "Compassion",
      highDescription: "Kind and cooperative.",
      moderateDescription: "Fair and diplomatic.",
      lowDescription: "Competitive and independent.",
      characteristics: {
        high: ["Kind", "Empathetic"],
        moderate: ["Balanced"],
        low: ["Direct", "Assertive"],
      },
    },
    Neuroticism: {
      label: "N - Neuroticism",
      description: "Emotional Stability",
      highDescription: "Emotionally sensitive.",
      moderateDescription: "Moderate emotional balance.",
      lowDescription: "Calm and resilient.",
      characteristics: {
        high: ["Sensitive"],
        moderate: ["Stable"],
        low: ["Calm", "Confident"],
      },
    },
  };

  const getLevel = (value) => {
    if (value >= 70) return "high";
    if (value >= 50) return "moderate";
    return "low";
  };

  const getTraitInsight = (trait) => {
    const level = getLevel(trait.value);
    const insight = oceanInsights[trait.name];

    return {
      description: insight[`${level}Description`],
      characteristics: insight.characteristics[level],
    };
  };

  const highestTrait = traits.reduce((max, t) =>
    t.value > max.value ? t : max
  );

  const handleDownloadPDF = async () => {
    const canvas = await html2canvas(reportRef.current, {
      scale: 2,
      backgroundColor: "#fff",
    });

    const imgData = canvas.toDataURL("image/png");
    const pdf = new jsPDF("landscape", "mm", "a4");

    const imgWidth = 297;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;

    pdf.addImage(imgData, "PNG", 0, 0, imgWidth, imgHeight);
    pdf.save("Personality_Report.pdf");
  };

  return (
    <div
      ref={reportRef}
      className="min-h-screen bg-slate-900 text-slate-200 px-4 py-10"
    >
      {/* HEADER */}
      <div className="flex justify-between items-center mb-10 max-w-6xl mx-auto">
        <div>
          <h3 className="text-xl font-bold">Personality Analysis Report</h3>
          <p className="text-gray-400 text-sm">
            {type} • {processingTime.toFixed(2)}s
          </p>
        </div>

        <button
          onClick={handleDownloadPDF}
          className="border px-4 py-2 rounded-lg hover:bg-white hover:text-black transition"
        >
          Download PDF
        </button>
      </div>

      {/* DOMINANT TRAIT */}
      <div className="flex justify-center mb-10">
        <div
          className="p-8 text-center rounded-2xl w-full max-w-xl"
          style={{
            background: "#1e293b",
            border: `2px solid ${highestTrait.color}`,
          }}
        >
          <h2 style={{ color: highestTrait.color }}>
            {oceanInsights[highestTrait.name].label}
          </h2>

          <h1 className="text-4xl">{highestTrait.value}%</h1>

          <p>{getTraitInsight(highestTrait).description}</p>
        </div>
      </div>

      {/* CHART */}
      <div className="max-w-4xl mx-auto mb-10">
        <div className="p-6 rounded-2xl bg-slate-800">
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={traits}>
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />

              <Bar dataKey="value">
                {traits.map((t) => (
                  <Cell key={t.name} fill={t.color} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* BACK */}
      <div className="text-center">
        <button
          onClick={() => navigate("/select")}
          className="border px-5 py-2 rounded-lg hover:bg-white hover:text-black"
        >
          Back
        </button>
      </div>
    </div>
  );
}

export default ResultPage;