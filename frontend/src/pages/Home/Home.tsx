import { useState, type ChangeEvent } from "react";
import { useNavigate } from "react-router-dom";
import logoImg from "../../../public/logo_autoU.png"
import "./home.scss";

export default function Home() {
    const navigate = useNavigate();
    const [userName, setUserName] = useState("");
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
        localStorage.setItem("userName", userName);
        navigate("/classifier");
    }

    function handleEmailChange(e: ChangeEvent<HTMLInputElement>) {
        setUserEmail(e.target.value);
        if (error) setError("");
    }

    function handleNameChange(e: ChangeEvent<HTMLInputElement>) {
        setUserName(e.target.value);
    }

    return (
        <div
            id="home"
            className="container-fluid d-flex flex-column min-vh-100 justify-content-center align-items-center text-center"
        >
            <header className="mb-3">
                <img
                    src={logoImg}
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

                <form className="mb-4 d-flex flex-column flex-md-row justify-content-center align-items-center gap-3 w-100">
                    <div className="flex-fill">
                        <input
                            type="text"
                            className="form-control"
                            placeholder="Digite seu nome"
                            value={userName}
                            onChange={handleNameChange}
                            onKeyDown={(e) =>
                                e.key === "Enter" && handleSaveUserEmail()
                            }
                        />
                    </div>

                    <div className="flex-fill">
                        <input
                            type="email"
                            className="form-control"
                            placeholder="Digite seu email"
                            value={userEmail}
                            onChange={handleEmailChange}
                            onKeyDown={(e) =>
                                e.key === "Enter" && handleSaveUserEmail()
                            }
                        />
                        {error && (
                            <div className="text-danger fw-bold mt-1">
                                {error}
                            </div>
                        )}
                    </div>
                </form>

                <button type="button" onClick={handleSaveUserEmail}>
                    Começar
                </button>
            </main>
        </div>
    );
}
