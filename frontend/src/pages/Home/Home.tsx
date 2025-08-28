import { useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import "./Home.scss";

export default function Home() {
    const navigate = useNavigate();
    const [userEmail, setUserEmail] = useState("");
    const [error, setError] = useState("");

    function validateEmail(email: string) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }

    function handleSaveUserEmail() {
        if (!userEmail) {
            setError("Por favor, insira seu email!");
            return;
        }

        if (!validateEmail(userEmail)) {
            setError("Por favor, insira um email válido!");
            return;
        }

        localStorage.setItem("userEmail", userEmail);
        navigate("/classifier");
    }

    function handleInputChange(e: ChangeEvent<HTMLInputElement>) {
        setUserEmail(e.target.value);
        if (error) setError("");
    }

    return (
        <div
            id="home"
            className="container-fluid d-flex flex-column min-vh-100 justify-content-center align-items-center text-center"
        >
            <header className="mb-3">
                <img
                    src="/src/assets/logo_autoU.png"
                    alt="Logo"
                    className="logo"
                />
            </header>
            <main>
                <h1 className="mb-3">Classificador de Emails Automático</h1>
                <p className="mb-4 fw-semibold">
                    Economize tempo automatizando a leitura e resposta de
                    emails!
                </p>

                <div className="mb-4">
                    <input
                        type="email"
                        className="emailInput mb-2"
                        placeholder="Digite seu email"
                        value={userEmail}
                        onChange={handleInputChange}
                        onKeyDown={(e) =>
                            e.key === "Enter" && handleSaveUserEmail()
                        }
                    />
                    {error && (
                        <div className="text-danger fw-bold d-block">{error}</div>
                    )}
                </div>

                <button
                    onClick={handleSaveUserEmail}
                >
                    Começar
                </button>
            </main>
        </div>
    );
}
