interface Emails {
    subject: string;
    message: string;
    category: string;
    response: string;
}

interface ResultProps {
    results: Emails[];
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
                    {results
                        .slice()
                        .reverse()
                        .map((res, index) => (
                            <tr key={index}>
                                <td>{res.subject}</td>
                                <td>{res.message}</td>
                                <td>
                                    <span
                                        className={`category ${
                                            res.category.toLowerCase() ===
                                            "produtivo"
                                                ? "produtivo"
                                                : "improdutivo"
                                        }`}
                                    >
                                        {res.category}
                                    </span>
                                </td>
                                <td>{res.response}</td>
                            </tr>
                        ))}
                </tbody>
            </table>
        </div>
    );
}
