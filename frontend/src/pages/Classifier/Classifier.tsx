import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Form from "../../components/Classifier/Form/Form";
import Result from "../../components/Classifier/Result/Result";
import "./classifier.scss";

interface EmailResult {
  subject: string;
  message: string;
  category: string;
  response: string;
}

export default function Classifier() {
  const navigate = useNavigate();
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [userName, setUserName] = useState<string | null>(null);
  const [results, setResults] = useState<EmailResult[]>([]);

  useEffect(() => {
    const email = localStorage.getItem("userEmail");
    const name = localStorage.getItem("userName");
    const storedResults = localStorage.getItem("emailResults");
    if (email) setUserEmail(email);
    if (name) setUserName(name);
    if (storedResults) setResults(JSON.parse(storedResults));
  }, []);

  const handleClassify = async (data: { subject: string; message: string } | File) => {
    try {
      const apiUrl = "http://127.0.0.1:8000/api/classify";
      const formData = new FormData();

      let subject = "";
      let message = "";

      if (data instanceof File) {
        subject = "Arquivo enviado";
        message = "Conteúdo enviado via arquivo";
        formData.append("subject", subject);
        formData.append("message", message);
        formData.append("file", data);
      } else {
        subject = data.subject;
        message = data.message;
        formData.append("subject", subject);
        formData.append("message", message);
      }

      if (userName) formData.append("sender", userName);

      const response = await fetch(apiUrl, { method: "POST", body: formData });
      if (!response.ok) throw new Error(`Erro: ${response.statusText}`);
      const json = await response.json();

      const newResult: EmailResult = {
        subject,
        message,
        category: json.category,
        response: json.response,
      };

      const updatedResults = [...results, newResult];
      setResults(updatedResults);
      localStorage.setItem("emailResults", JSON.stringify(updatedResults));
    } catch (err) {
      console.error("Erro ao classificar:", err);
    }
  };

  return (
    <div id="classifier">
      <header className="user-info">
        <div className="d-flex gap-2">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            className="bi bi-arrow-left-circle-fill"
            viewBox="0 0 16 16"
            onClick={() => navigate("/")}
          >
            <path d="M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0m3.5 7.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z" />
          </svg>

          <h5 className="fw-semibold">{userName}</h5>
        </div>
        <p>{userEmail}</p>
      </header>

      <main className="classifier-content">
        <h1 className="fw-semibold">Classificador de Emails</h1>
        <div className="classifier-card">
          <Form onClassify={handleClassify} />
        </div>

        <Result results={results} />
      </main>
    </div>
  );
}
