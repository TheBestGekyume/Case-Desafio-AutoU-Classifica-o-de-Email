import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Form from "../../components/Classifier/Form/Form";
import Result from "../../components/Classifier/Result/Result";
import "./classifier.scss";

export default function Classifier() {
    const navigate = useNavigate();
    const [userEmail, setUserEmail] = useState<string | null>(null);

    useEffect(() => {
        const email = localStorage.getItem("userEmail");
        if (email) {
            setUserEmail(email);
        }
    }, []);

    return (
        <div id="classifier">
            <header className="user-info">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    className="bi bi-arrow-left-circle-fill"
                    viewBox="0 0 16 16"
                    onClick={()=> navigate("/")}
                >
                    <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z" />
                </svg>
                <h5>{userEmail}</h5>
            </header>

            <main className="classifier-content">
                <h1 className="fw-semibold">Classificador de Emails</h1>
                <div className="classifier-card">
                    <Form
                        onClassify={function (): void {
                            throw new Error("Function not implemented.");
                        }}
                    />
                    <Result category={null} confidence={null} response={null} />
                </div>
            </main>
        </div>
    );
}
