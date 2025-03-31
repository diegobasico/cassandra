import { useRef } from "react";

import { atom, useAtom } from "jotai";
import axios from "axios";

import { registerAllModules } from "handsontable/registry";
import { HotTable, HotTableRef } from "@handsontable/react-wrapper";
import Handsontable from "handsontable";
import { HyperFormula } from "hyperformula";

registerAllModules();

const hotAtom = atom([
  ["1", "Obras Provisionales", "glb", 1, 2, 2],
  ["2", "Arquitectura", "m²", 1, 2, 2],
  ["3", "Estructuras", "m³", 1, 2, 2],
  ["4", "Instalaciones Sanitarias", "m", 1, 2, 2],
  ["5", "Instalaciones Eléctricas", "m", 1, 2, 2],
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

  function calcCols(table: Handsontable.CellValue[]) {
    return table.map((row, index) => {
      if (index < table.length - 1) {
        row[5] = `=D${index + 1}*E${index + 1}`;
      }
      return row;
    });
  }

  return (
    <div className="flex h-full w-full flex-col bg-green-400">
      <span className="p-4 text-3xl">Presupuesto</span>
      <div className="ht-theme-main-dark-auto overflow-y-auto">
        <HotTable
          ref={hotRef}
          formulas={{
            engine: hyperformulaInstance,
          }}
          afterChange={function (
            changes: Handsontable.CellChange[] | null,
            source: Handsontable.ChangeSource,
          ) {
            const hot = hotRef.current?.hotInstance;
            if (changes && source !== "loadData" && hot) {
              const newTable = calcCols(hot.getData());
              setTableData(newTable);
              sendTableData(newTable);
            }
          }}
          data={tableData}
          columns={[
            { col: "Item", className: "htLeft" },
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
          colHeaders={["Item", "Descripción", "Und", "Metrado", "Precio", "Parcial"]}
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
