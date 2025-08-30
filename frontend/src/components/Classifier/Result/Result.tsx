interface EmailResult {
  subject: string;
  message: string;
  category: string;
  response: string;
}

interface ResultProps {
  results: EmailResult[];
}

export default function Result({ results }: ResultProps) {
  if (!results || results.length === 0) return null;

  return (
    <div className="result-table mt-5 mb-4">
      <table>
        <thead>
          <tr>
            <th>Assunto</th>
            <th>Mensagem</th>
            <th>Categoria</th>
            <th>Resposta</th>
          </tr>
        </thead>
        <tbody>
          {results.map((res, index) => (
            <tr key={index}>
              <td>{res.subject}</td>
              <td>{res.message}</td>
              <td>{res.category}</td>
              <td>{res.response}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
