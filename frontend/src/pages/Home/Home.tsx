import { useNavigate } from "react-router-dom";
import "./Home.scss";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div id="home" className="container-fluid d-flex flex-column min-vh-100 justify-content-center align-items-center text-center">
      <header className="mb-4">
        <img
          src="/src/assets/logo_autoU.png"
          alt="Logo"
          className="logo"
        />
      </header>
      <main>
        <h1 className="mb-3">Classificador de Emails Automático</h1>
        <p className="mb-4 text-secondary"> 
          Economize tempo automatizando a leitura e resposta de emails!
        </p>
        <button onClick={() => navigate("/classifier")}>
          Começar
        </button>
      </main>
    </div>
  );
}
