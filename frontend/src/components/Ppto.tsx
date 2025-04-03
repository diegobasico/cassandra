import { useRef } from "react";

import { atom, useAtom } from "jotai";
import axios from "axios";

import { registerAllModules } from "handsontable/registry";
import { HotTable, HotTableRef } from "@handsontable/react-wrapper";
import Handsontable from "handsontable";
import { HyperFormula } from "hyperformula";

registerAllModules();

const hotAtom = atom([
  [1, , , "Título 1", "glb", 1, 2, 2],
  [1, , , "Título 2", "m²", 1, 2, 2],
  [2, , , "Título 2.1", "m³", 1, 2, 2],
  [3, , , "Partida 2.1.1", "m", 1, 2, 2],
  [2, , , "Título 2.2", "m³", 1, 2, 2],
  [3, , , "Partida 2.2.1", "m", 1, 2, 2],
  [3, , , "Partida 2.2.2", "m", 1, 2, 2],
  [1, , , "Título 3", "m", 1, 2, 2],
  [2, , , "Partida 3.1", "m", 1, 2, 2],
  [2, , , "Partida 3.2", "m", 1, 2, 2],
]);

function Ppto() {
  const [tableData, setTableData] = useAtom(hotAtom);
  const hotRef = useRef<HotTableRef>(null);
  const hyperformulaInstance = HyperFormula.buildEmpty({
    licenseKey: "internal-use-in-handsontable",
  });

  async function sendTableData(data: Handsontable.CellValue[]) {
    try {
      await axios.post(
        "http://127.0.0.1:8000/ppto",
        { table: data },
        {
          headers: { "Content-Type": "application/json" },
        },
      );
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function calcSheet(table: Handsontable.CellValue[]) {
    return table.map((row, index) => {
      // level logic (fixed)
      if (row[0] === null && index < table.length - 1) {
        if (index === 0) {
          row[0] = 1;
        } else {
          row[0] = table[index - 1][0];
        }
      }
      // título/partida logic
      if (index === 0) {
        row[1] = "Título"; // first row is always título
      }
      if (index < table.length - 1 && index > 0) {
        if (table[index][0] >= table[index + 1][0]) {
          row[1] = "Partida";
        } else {
          row[1] = "Título";
        }
      }
      // calculates parcial column
      if (index < table.length - 1) {
        row[7] = `=F${index + 1}*G${index + 1}`;
      }
      return row;
    });
  }

  function calcItems(table: Handsontable.CellValue[]) {
    for (let row = 0; row < table.length - 1; row++) {}
  }

  return (
    <div className="flex h-full w-full flex-col bg-green-400">
      <span className="p-4 text-3xl">Presupuesto</span>
      {/* Hands On Table Component */}
      <div className="ht-theme-main-dark-auto overflow-y-auto">
        <HotTable
          ref={hotRef}
          formulas={{
            engine: hyperformulaInstance,
          }}
          // hot reloads the sheet with every change
          afterChange={function (
            changes: Handsontable.CellChange[] | null,
            source: Handsontable.ChangeSource,
          ) {
            const hot = hotRef.current?.hotInstance;
            if (changes && source !== "loadData" && hot) {
              let newTable = hot.getData();
              newTable = calcSheet(newTable);
              calcItems(newTable);
              setTableData(newTable);
              sendTableData(newTable);
            }
          }}
          data={tableData}
          columns={[
            { index: "Level", type: "numeric" },
            { index: "Tipo", type: "text" },
            { index: "Item", className: "htLeft" },
            { index: "Descripción", className: "htLeft", type: "text" },
            { index: "Und", className: "htCenter", type: "text" },
            {
              index: "Metrado",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
            {
              index: "Precio",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              readOnly: true,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
            {
              index: "Parcial",
              className: "htRight",
              type: "numeric",
              allowInvalid: false,
              readOnly: true,
              numericFormat: {
                pattern: "0,0.00",
              },
            },
          ]}
          rowHeaders={false}
          colHeaders={[
            "Level",
            "Tipo",
            "Item",
            "Descripción",
            "Und",
            "Metrado",
            "Precio",
            "Parcial",
          ]}
          autoWrapRow={true}
          autoWrapCol={true}
          licenseKey="non-commercial-and-evaluation"
          minSpareRows={1}
          stretchH="all"
          width="100%"
          height="auto"
          contextMenu={{
            items: {
              copy: {},
              cut: {},
              "---------": {},
              row_above: {},
              row_below: {},
              remove_row: {},
            },
          }}
          hiddenColumns={{
            columns: [],
            indicators: true,
            copyPasteEnabled: false,
          }}
          manualColumnMove={false}
          manualColumnFreeze={true}
          manualColumnResize={true}
          filters={false}
          hiddenRows={{
            rows: [],
            indicators: true,
            copyPasteEnabled: false,
          }}
          manualRowMove={true}
          manualRowResize={true}
          columnSorting={true}
          mergeCells={true}
        />
      </div>
    </div>
  );
}

export default Ppto;
