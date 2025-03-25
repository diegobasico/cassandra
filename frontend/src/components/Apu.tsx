import { useEffect, useState } from "react";
import axios from "axios";

function Apu() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [response, setResponse] = useState(null);
  const myData = {
    name: "Laptop",
    price: 999.99,
    quantity: 2,
  };

  useEffect(() => {
    axios
      .get("https://jsonplaceholder.typicode.com/todos/1")
      .then((response) => {
        setData(response.data);
        setLoading(false);
      })
      .catch((error) => console.error("Error:", error));
  }, []);

  async function sendData(data: { name: string; price: number; quantity: number }) {
    console.log(data);
    try {
      const postedData = await axios.post("http://127.0.0.1:8000/response", data, {
        headers: { "Content-Type": "application/json" },
      });
      setResponse(postedData.data);
    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <div className="p-4">
      <span className="text-3xl">Análisis de Precios Unitarios</span>
      {loading ? <p>Loading...</p> : <pre>{JSON.stringify(data, null, 2)}</pre>}
      <button onClick={() => sendData(myData)}> Click </button>
      {response && <pre>{JSON.stringify(response, null, 2)}</pre>}
    </div>
  );
}

export default Apu;
