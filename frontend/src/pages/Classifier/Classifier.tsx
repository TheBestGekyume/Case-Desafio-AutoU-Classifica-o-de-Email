import Form from "../../components/Classifier/Form/Form";
import Result from "../../components/Classifier/Result/Result";
import "./classifier.scss";

export default function Classifier() {
  return (
    <div id="classifier">
      <h1>Classificador de Emails</h1>
      <div className="classifier-card">
        <Form onClassify={function (): void {
                  throw new Error("Function not implemented.");
              } } />
        <Result category={null} confidence={null} response={null} />
      </div>
    </div>
  );
}
