import { useState } from "react";

interface FormProps {
    onClassify: (data: string | File) => void;
}

export default function Form({ onClassify }: FormProps) {
    const [text, setText] = useState("");

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (text.trim()) {
            onClassify(text);
            setText("");
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            onClassify(e.target.files[0]);
        }
    };

    return (
        <form id="form" onSubmit={handleSubmit}>
          
            <fieldset className="d-flex flex-column gap-1 mb-2">
                <label htmlFor="subject">Assunto</label>
                <input id="subject" type="text" />
            </fieldset>

            <fieldset className="d-flex flex-column gap-1 mb-2">
                <label htmlFor="message">Mensagem</label>
                <textarea
                    id="message"
                    name="message"
                    placeholder="Digite o seu email aqui..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                />
            </fieldset>

            <fieldset className="d-flex flex-column gap-1 mb-2">
              <label htmlFor="file">Anexar Arquivo</label>
                <input
                    id="file"
                    type="file"
                    accept=".txt,.eml"
                    onChange={handleFileChange}
                />
            </fieldset>

            <button type="submit">Classificar</button>
        </form>
    );
}
