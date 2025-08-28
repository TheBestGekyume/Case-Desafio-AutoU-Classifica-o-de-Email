import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home/Home";
import Classifier from "./pages/Classifier/Classifier";
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/global.css';



function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/classifier" element={<Classifier />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
