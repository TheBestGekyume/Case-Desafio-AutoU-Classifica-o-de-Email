import { useState } from "react";

export interface FormProps {
    onClassify: (
        data: File | { subject: string; message: string }
    ) => Promise<void>;
}

export default function Form({ onClassify }: FormProps) {
    const [activeTab, setActiveTab] = useState<"email" | "file">("email");
    const [subject, setSubject] = useState("");
    const [message, setMessage] = useState("");
    const [file, setFile] = useState<File | null>(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (activeTab === "email" && (!subject.trim() || !message.trim()))
            return;
        if (activeTab === "file" && !file) return;

        setLoading(true);
        try {
            if (activeTab === "file" && file) {
                await onClassify(file);
            } else {
                await onClassify({ subject, message });
            }

            setSubject("");
            setMessage("");
            setFile(null);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <form id="form" onSubmit={handleSubmit}>
            <div className="tabs d-flex justify-content-center gap-4 mb-1">
                <p
                    className={`tab m-0 ${
                        activeTab === "email" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("email")}
                >
                    Email
                </p>
                <p
                    className={`tab m-0 ${
                        activeTab === "file" ? "active" : ""
                    }`}
                    onClick={() => setActiveTab("file")}
                >
                    Arquivo
                </p>
            </div>

            <div
                className={`tab-content ${
                    activeTab === "email" ? "active" : ""
                }`}
            >
                <fieldset className="d-flex flex-column gap-1 mb-2">
                    <label htmlFor="subject">Assunto</label>
                    <input
                        id="subject"
                        type="text"
                        value={subject}
                        onChange={(e) => setSubject(e.target.value)}
                    />
                </fieldset>

                <fieldset className="d-flex flex-column gap-1 mb-2">
                    <label htmlFor="message">Mensagem</label>
                    <textarea
                        id="message"
                        placeholder="Digite o seu email aqui..."
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                    />
                </fieldset>
            </div>

            <div
                className={`tab-content ${
                    activeTab === "file" ? "active" : ""
                }`}
            >
                <fieldset className="d-flex flex-column gap-1 mb-2">
                    <label htmlFor="file">Anexar Arquivo</label>
                    <input
                        id="file"
                        type="file"
                        accept=".txt,.pdf,.eml"
                        onChange={(e) =>
                            setFile(e.target.files ? e.target.files[0] : null)
                        }
                    />
                </fieldset>
            </div>

            <button type="submit" disabled={loading}>
                {loading ? "Classificando..." : "Classificar"}
            </button>
        </form>
    );
}
