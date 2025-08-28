interface ResultProps {
  category: string | null;
  confidence: number | null;
  response: string | null;
}

export default function Result({ category, confidence, response }: ResultProps) {
  if (!category && !response) {
    return null; // não renderiza nada até ter resultado
  }

  return (
    <div className="result">
      {category && (
        <div className="category">
          Categoria: {category}
        </div>
      )}
      {confidence !== null && (
        <div className="confidence">
          Confiança: {(confidence * 100).toFixed(2)}%
        </div>
      )}
      {response && (
        <div className="response">
          Resposta sugerida: {response}
        </div>
      )}
    </div>
  );
}
