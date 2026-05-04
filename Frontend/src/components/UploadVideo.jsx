import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function UploadVideo() {
  const navigate = useNavigate();
  const location = useLocation();

  const type = location.state?.type || "Video";

  const [video, setVideo] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setVideo(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!video) return alert("Please select a video");

    const formData = new FormData();
    formData.append("video", video);

    try {
      setLoading(true);
      const start = Date.now();

      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      const end = Date.now();

      navigate("/result", {
        state: {
          scores: {
            Openness: data.openness,
            Conscientiousness: data.conscientiousness,
            Extraversion: data.extraversion,
            Agreeableness: data.agreeableness,
            Neuroticism: data.neuroticism,
          },
          processingTime: (end - start) / 1000,
          type,
        },
      });

    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-6">
      
      <div className="bg-gray-800 shadow-2xl rounded-2xl p-8 w-full max-w-xl text-gray-100 border border-gray-700">
        
        <h2 className="text-2xl font-bold text-center mb-2">
          {type} Analysis
        </h2>

        <p className="text-center text-gray-400 text-sm mb-6">
          Upload a video to analyze personality
        </p>

        {/* Upload */}
        <label className="block border-2 border-dashed border-gray-500 rounded-lg p-6 text-center cursor-pointer hover:border-blue-400 hover:bg-gray-700 transition">
          <input
            type="file"
            accept="video/*"
            onChange={handleFileChange}
            className="hidden"
          />
          <p className="text-gray-300">Click to upload video</p>
        </label>

        {/* Preview */}
        {preview && (
          <div className="mt-4">
            <video src={preview} controls className="w-full rounded-lg border border-gray-600" />
          </div>
        )}

        {/* Button */}
        <button
          onClick={handleUpload}
          disabled={loading}
          className="w-full mt-6 bg-gradient-to-r from-blue-500 to-cyan-500 hover:from-blue-600 hover:to-cyan-600 py-2 rounded-lg font-semibold shadow-lg disabled:opacity-50 transition"
        >
          {loading ? "Analyzing..." : "Start Analysis"}
        </button>
      </div>
    </div>
  );
}

export default UploadVideo;