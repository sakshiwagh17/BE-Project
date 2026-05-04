import { BrowserRouter, Routes, Route } from "react-router-dom";

import UploadVideo from "./components/UploadVideo";
import ResultPage from "./components/ResultPage";
import SelectionPage from "./components/SelectionPage";
import NavBar from "./components/NavBar";

function App() {
  return (
    <BrowserRouter>
    <NavBar />
      <Routes>
        
        <Route path="/" element={<SelectionPage />} />
        <Route path="/upload" element={<UploadVideo />} />
        <Route path="/result" element={<ResultPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;