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
    <form onSubmit={handleSubmit}>
      <textarea
        placeholder="Cole o texto do e-mail aqui..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <input type="file" accept=".txt,.eml" onChange={handleFileChange} />
      <button type="submit">Classificar</button>
    </form>
  );
}
