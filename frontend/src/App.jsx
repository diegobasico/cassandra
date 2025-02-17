import { useState, useEffect } from "react";
import axios from "axios";
import { HotTable } from "@handsontable/react";
import "handsontable/dist/handsontable.full.css";

function App() {
  const [tableData, setTableData] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:8000/data")
      .then(response => {
        if (response.data.length > 0) {
          // Convert list of dictionaries to an array format Handsontable expects
          const headers = Object.keys(response.data[0]);
          const dataRows = response.data.map(row => headers.map(h => row[h]));
          setTableData([headers, ...dataRows]);  // Include headers as first row
        }
      })
      .catch(error => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      <h1>React + FastAPI + Polars + Handsontable</h1>
      <HotTable
        data={tableData}
        colHeaders={true}
        rowHeaders={true}
        width="600"
        height="300"
        licenseKey="non-commercial-and-evaluation"
      />
    </div>
  );
}

export default App;
